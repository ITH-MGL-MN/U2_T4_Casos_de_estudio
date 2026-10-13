# -*- coding: utf-8 -*-
"""
probador.py — Herramienta local para inspeccionar un caso de estudio.

    python probador.py          # lista todos los temas (T1–T19)
    python probador.py T4       # detalle del caso T4 + raíz de referencia

Muestra el catálogo del caso, los métodos CORRECTOS (sugeridos) que la
autocalificación exige seleccionar, y la raíz de referencia con los valores
nominales (lo que el oráculo usa para comparar).
"""
import sys

from profe.core import (CATALOGO, _modelo, oraculo_escalar_todas,
                        oraculo_sistema, metodos_sugeridos_para, familia)


def _nominales(info):
    return {n: (s[1] if s[0] == 'n' else 0.5 * (s[1] + s[2]))
            for n, s in info['params'].items()}


def listar_temas():
    print('Temas disponibles (%d):\n' % len(CATALOGO))
    for t in CATALOGO:
        info = CATALOGO[t]
        tipo = 'sistema' if info.get('sistema') else 'ecuación'
        print('  %-4s [%-8s] %s' % (t, tipo, info['titulo']))
    print('\nUso: python probador.py <TEMA>   (ej. python probador.py T4)')


def detalle(tema):
    info = CATALOGO[tema]
    mod = _modelo(tema)
    nom = _nominales(info)
    es_sis = mod['sistema']

    print('=' * 72)
    print(' %s · %s' % (tema, info['titulo']))
    print('=' * 72)
    print('Incógnita : %s [%s]' % (info['incognita'], info['unidad']))
    print('Ecuación  : %s' % info['ecuacion'])
    if info.get('sistema'):
        print('Variables : %s' % ', '.join(info['vars']))
        print('x0        : %s' % info['x0'])
    else:
        print('Intervalo : %s' % (info['intervalo'],))
    print('Parámetros (nominal, incertidumbre):')
    for p, spec in info['params'].items():
        if spec[0] == 'u':
            print('   %-10s uniforme en [%.4g, %.4g]' % (p, spec[1], spec[2]))
        else:
            print('   %-10s %.6g  (±%.1f%%)' % (p, spec[1], 100 * spec[2]))
    print('Desafío   : %s' % info['desafio'])

    print('\nMétodos SUGERIDOS (los que la autocalificación exige seleccionar):')
    for m in info['metodos_sugeridos']:
        print('   %-30s familia: %s' % (m, familia(m)))

    # Raíz de referencia con valores nominales
    print('\nRaíz(es) de referencia (valores nominales):')
    if es_sis:
        R, ok = oraculo_sistema(lambda X: mod['F'](X, nom), info['x0'])
        print('   convergió=%s   raíz=%s' % (ok, R if ok else '(no convergió)'))
    else:
        lo, hi = info['intervalo']
        raices = oraculo_escalar_todas(lambda xs: mod['f_arr'](xs, nom), lo, hi)
        if raices:
            print('   %s' % (', '.join('%.8g' % r for r in raices)))
        else:
            print('   (sin raíces con cambio de signo en el intervalo)')
    return 0


if __name__ == '__main__':
    args = [a.upper() for a in sys.argv[1:]]
    if not args:
        sys.exit(listar_temas())
    tema = args[0]
    if tema not in CATALOGO:
        print('Tema desconocido: %r (usa T1–T19).' % tema)
        sys.exit(1)
    sys.exit(detalle(tema))
