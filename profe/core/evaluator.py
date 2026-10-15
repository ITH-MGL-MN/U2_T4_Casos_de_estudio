# -*- coding: utf-8 -*-
"""
profe/core/evaluator.py — Calificación (simplificada) y retroalimentación.

A diferencia de U2_T3B, la calificación automática de U2_T4 se reduce a UNA
sola cosa: que el equipo haya SELECCIONADO al menos los métodos correctos de
su caso (los `metodos_sugeridos`) y al menos un contraejemplo. El resto
(interpretación de las gráficas, informe y exposición) se revisa a mano.
"""
import numpy as np

from .catalogo import _norm, familia, metodos_sugeridos_para, es_sistema, UMBRAL_EXITO


def _config_seleccion():
    """Regla de selección desde config.yaml (con valores por omisión)."""
    from profe.config import obtener_configuracion
    cfg, _ = obtener_configuracion()
    sel = cfg.get('seleccion', {})
    return {
        'requiere_todos_sugeridos': sel.get('requiere_todos_sugeridos', True),
        'min_contraejemplos': sel.get('min_contraejemplos', 1),
    }


def calificar(tema, seleccionados, resultado=None):
    """Autocalificación por SELECCIÓN de métodos.

    `tema`         : id del caso (p. ej. 'T1').
    `seleccionados`: lista de nombres de métodos elegidos por el equipo.
    `resultado`    : (opcional) salida de evaluar_tema, para enriquecer el desglose.

    Devuelve (nota_0_100, desglose). La nota es binaria: 100 si aprueba, 0 si no.
    """
    regla = _config_seleccion()
    sugeridos = metodos_sugeridos_para(tema)
    seleccion = [_norm(m) for m in seleccionados]

    faltantes = [m for m in sugeridos if m not in seleccion]
    contraejemplos = [m for m in seleccion if m not in sugeridos]

    # El contraejemplo solo se exige en casos ESCALARES: en los de SISTEMA las
    # opciones del cuaderno son dos y ambas son sugeridas, así que exigirlo los
    # haría reprobar siempre.
    requiere_contra = (not es_sistema(tema)) and regla['min_contraejemplos'] > 0

    ok_sugeridos = (len(faltantes) == 0) if regla['requiere_todos_sugeridos'] else (len(faltantes) < len(sugeridos))
    ok_contraejemplos = (not requiere_contra) or len(contraejemplos) >= regla['min_contraejemplos']

    fams = {familia(m) for m in seleccion} - {'desconocida'}

    aprueba = bool(ok_sugeridos and ok_contraejemplos)
    nota = 100.0 if aprueba else 0.0

    desglose = {
        'tema': tema,
        'seleccion': seleccion,
        'sugeridos': sugeridos,
        'faltantes': faltantes,
        'contraejemplos': contraejemplos,
        'familias': sorted(fams),
        'requiere_contraejemplo': requiere_contra,
        'ok_sugeridos': ok_sugeridos,
        'ok_contraejemplos': ok_contraejemplos,
        'aprueba': aprueba,
    }
    if resultado is not None:
        # Enriquecer con el desempeño real de cada método (para el informe).
        desglose['desempeno'] = {
            m: {'pct_exito': 100 * resultado['metodos'][m]['pct_exito'],
                'cuenta': resultado['metodos'][m]['cuenta']}
            for m in resultado['metodos'] if m in seleccion
        }
    return nota, desglose


def consejos(resultado):
    """Retroalimentación automática por reglas sobre las métricas (no juicios)."""
    msgs = []
    mets = resultado['metodos']
    polinomico = resultado.get('polinomico')

    for m, d in sorted(mets.items(), key=lambda kv: -kv[1]['pct_diverge']):
        pd = d['pct_diverge']
        if d.get('sospechoso'):
            msgs.append('%s: mediana de solo %.0f iteraciones — parece un envoltorio trivial, no una implementación propia. No cuenta.'
                        % (m, np.nanmedian(d['n_iter'])))
        if pd <= 0.05:
            continue
        # El motivo dominante explica POR QUE fallo: no es lo mismo no arrancar
        # que divergir o que llegar a otra raiz.
        fallos = {k: v for k, v in (d.get('motivos') or {}).items() if k != 'ok'}
        k = max(fallos, key=lambda kk: fallos[kk]) if fallos else None
        pct = 100 * max(fallos.values()) / max(1, d['n_iter'].size) if fallos else 100 * pd
        if k == 'sin_cambio_signo':
            msgs.append('%s: %.0f%% de las muestras no pudieron ni arrancar (el intervalo no encerraba la '
                        'raíz). No es que el método diverja: es el aislamiento. Fija MIS_INTERVALOS con un '
                        'intervalo que sí encierre la raíz y verás que no falla.' % (m, pct))
        elif k == 'complejo':
            msgs.append('%s: %.0f%% de las muestras se fueron al plano complejo (es un método abierto: con un '
                        'arranque lejano se sale del eje real y no vuelve a la raíz física). Fija MIS_ARRANQUES '
                        'con un arranque CERCA de la raíz y verás que no falla.' % (m, pct))
        elif k == 'otra_raiz':
            msgs.append('%s: %.0f%% de las muestras convergieron a OTRA raíz, no a la física. El residuo es ~0, '
                        'así que el método "acertó" a una raíz equivocada: revisa el aislamiento y, si es un '
                        'método abierto, el arranque (MIS_ARRANQUES).' % (m, pct))
        elif k == 'divergente':
            msgs.append('%s: %.0f%% de las muestras divergieron (la iteración crece sin límite). Con un despeje '
                        'cuyo |g\'(x)| >= 1 el punto fijo NO puede converger: no es cuestión de ajustar el arranque.' % (m, pct))
        elif k == 'estancado':
            msgs.append('%s: %.0f%% de las muestras se estancaron (derivada o denominador nulo). Es propio de la '
                        'zona del arranque, no del intervalo.' % (m, pct))
        elif k == 'no_converge':
            msgs.append('%s: %.0f%% de las muestras agotaron las iteraciones sin converger. Revisa el criterio de '
                        'paro o el arranque.' % (m, pct))
        elif k == 'no_aplica':
            msgs.append('%s: no se puede aplicar a este caso (necesita los coeficientes del polinomio). Míralo como '
                        'CONTRAEJEMPLO en tu informe.' % m)
        else:
            msgs.append('%s: %.0f%% de las muestras no llegaron a la raíz. Míralo como posible CONTRAEJEMPLO en tu '
                        'informe.' % (m, 100 * pd))

    if resultado.get('intervalo') is not None:
        _cerr = [m for m, d in mets.items() if d['familia'] in ('cerrado', 'hibrido')]
        _malos = [m for m in _cerr if mets[m]['pct_diverge'] > 0.05]
        if _malos:
            msgs.append('Fijaste MIS_INTERVALOS, así que %s usan el mismo par de valores en las 1000 '
                        'muestras, pero siguen sin arrancar: el intervalo no cubre el rango en el que '
                        'se MUEVE la raíz. Debe encerrarla en TODAS las muestras, no sólo en la nominal.'
                        % ', '.join(_malos))
        elif _cerr:
            msgs.append('Con el intervalo que fijaste en MIS_INTERVALOS, los métodos que necesitan '
                        'paréntesis (cerrado/híbrido) lo usan tal cual: por eso ahí no fallan.')

    if resultado.get('arranques') is not None:
        _abiertos = [m for m, d in mets.items() if d.get('usa_arranque')]
        _malos = [m for m in _abiertos if mets[m]['pct_diverge'] > 0.05]
        if _malos:
            msgs.append('Con MIS_ARRANQUES fijaste el arranque de %s, pero siguen fallando: el arranque '
                        'debe quedar CERCA de la raíz (y si el caso tiene varias raíces, puede llevarlos '
                        'a otra).' % ', '.join(_malos))
        elif _abiertos:
            msgs.append('Con el arranque que fijaste en MIS_ARRANQUES, los métodos abiertos y polinómicos '
                        'parten de ahí en las 1000 muestras: si está cerca de la raíz, tampoco fallan.')

    ok = [m for m, d in mets.items() if d['cuenta']]
    if polinomico and not any(mets[m]['familia'] == 'polinomios' for m in ok):
        msgs.append('Este es un tema polinómico: necesitas Müller o Bairstow para la base completa.')

    lentos = sorted([m for m in ok], key=lambda m: np.nanmedian(mets[m]['n_iter']))
    if len(lentos) >= 2:
        msgs.append('Más rápido en tu corrida: %s (mediana %d iter). Más lento: %s (mediana %d iter).'
                    % (lentos[0], np.nanmedian(mets[lentos[0]]['n_iter']),
                       lentos[-1], np.nanmedian(mets[lentos[-1]]['n_iter'])))
    return msgs


def preguntas_criterio():
    """Preguntas conceptuales de criterio (desde config/preguntas.yaml).

    Ya NO se autocalifican: son parte del INFORME y de la EXPOSICIÓN.
    """
    from profe.config import obtener_configuracion
    _, preguntas = obtener_configuracion()
    banco = preguntas.get('criterio', {})
    return [{'id': k, 'texto': v['pregunta'], 'opciones': v['opciones'],
             'correcta': v.get('correcta', 0)} for k, v in sorted(banco.items())]


def enviar_resultado(NC, tema, metodos, calificacion, correo='', alcance='equipo', debug=False):
    """Envía Metodos + Calificacion a Apps Script (acción proyecto_resultado)."""
    import requests
    from profe.config import obtener_configuracion
    cfg, _ = obtener_configuracion()
    payload = {
        'accion': 'proyecto_resultado', 'token': cfg['evaluacion']['webhook_token'],
        'NC': str(NC), 'correo': correo, 'tema': tema,
        'metodos': list(metodos), 'calificacion': float(calificacion),
        'alcance': alcance,
    }
    if debug:
        print('POST', payload)
    r = requests.post(cfg['evaluacion']['apps_script_url'], json=payload, timeout=20)
    return r.json()
