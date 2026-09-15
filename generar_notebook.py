# -*- coding: utf-8 -*-
"""Genera U2_T4_Casos_de_estudio.ipynb (plantilla del proyecto por equipo).

Estructura:
  Config -> Identificación -> Selección de tema (3 celdas) -> Integrantes (3 celdas)
  -> Tu caso -> Librería del equipo -> Definición simbólica -> Tus métodos
  -> Monte Carlo -> Gráficos (histogramas, % divergencia, box plots, respuesta física)
  -> Conclusiones -> Calificación y envío
"""
# ⚠️ DESACTIVADO (2026-09-14).
# El notebook U2_T4_Casos_de_estudio.ipynb se edita DIRECTAMENTE en VS Code: es la
# fuente de verdad y ya tiene ediciones manuales del profesor. Ejecutar este script
# lo SOBRESCRIBIRIA POR COMPLETO y borraría esos cambios.
# Se conserva solo como referencia histórica de cómo se armó la plantilla.
# Si de verdad se quiere regenerar desde cero, borra el raise siguiente.
raise SystemExit(
    'generar_notebook.py está DESACTIVADO: edita U2_T4_Casos_de_estudio.ipynb directamente.'
)

import json

nb = {
    "cells": [],
    "metadata": {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
        "accelerator": "GPU",
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}


def md(src):
    nb["cells"].append({"cell_type": "markdown", "metadata": {},
                        "source": src.splitlines(keepends=True)})


def code(src, tags=None):
    nb["cells"].append({"cell_type": "code", "execution_count": None,
                        "metadata": {"tags": tags or []}, "outputs": [],
                        "source": src.splitlines(keepends=True)})


# ===========================================================================
# TÍTULO
# ===========================================================================
md("""# Proyecto — Casos de estudio de raíces de ecuaciones + Monte Carlo (U2_T4)

**Mecatrónica · Métodos Numéricos**

Cada **equipo** elige **un caso de estudio de ingeniería** (una ecuación o un sistema de
raíces) y lo analiza con una **simulación de Monte Carlo** para decidir, con evidencia,
**qué método numérico conviene** en un sistema real con incertidumbre.

Al terminar tendrás:
1. Tu **librería de métodos** implementada por el equipo.
2. Los **gráficos** de la simulación (incluido el **box plot** comparativo).
3. Una **calificación automática** de la parte de métodos y 5 preguntas de criterio.

---

> ### 👉 Antes de empezar
> - **Solo el jefe de equipo** ejecuta las celdas de **selección de tema** e **integrantes**.
> - El jefe **descarga el repositorio** y **comparte la carpeta de Drive** con su equipo.
> - El jefe **inicia sesión con su cuenta institucional** (`@campus.tecnm.mx`).
""")

md("""Al ejecutar la celda de configuración, Google te pedirá permiso para acceder a tu Drive.

> **INICIA SESIÓN CON TU CORREO INSTITUCIONAL**

- Debe ser un correo que termine en **@campus.tecnm.mx**.
- Si no es institucional, verás una alerta y no podrás continuar.
- Solo hay que seleccionar la **primera opción**; es seguro si seleccionas todo.
""")

# ===========================================================================
# CONFIGURACIÓN
# ===========================================================================
code(r'''# @title Ejecutar configuración general
# ============================================================
# CELDA 1 — CONFIGURACIÓN GENERAL (NO MODIFICAR)
# ============================================================
import os, sys, subprocess, importlib, base64, zlib, json

try:
    import google.colab
    ES_COLAB = True
except ImportError:
    ES_COLAB = False

# ------------------------------------------------------------
# EDITAR AQUÍ: repositorio de la tarea
# ------------------------------------------------------------
REPO_URL = 'https://github.com/ITH-MGL-MN/U2_T4_Casos_de_estudio.git'
REPO_NOMBRE = 'U2_T4_Casos_de_estudio'

if ES_COLAB:
    BASE = '/content/drive/MyDrive/CursoMN'
    REPO = os.path.join(BASE, REPO_NOMBRE)
else:
    REPO = os.getcwd()
    for _ in range(4):
        if os.path.exists(os.path.join(REPO, 'profe', 'grader.py')):
            break
        padre = os.path.dirname(REPO)
        if padre == REPO:
            break
        REPO = padre
    if not os.path.exists(os.path.join(REPO, 'profe', 'grader.py')):
        REPO = r'o:\Mi unidad\CursoMN\U2_T4_Casos_de_estudio'

print('Modo:', 'Google Colab' if ES_COLAB else 'PC local')
print('Carpeta de la tarea:', REPO)

if ES_COLAB:
    from google.colab import drive
    drive.mount('/content/drive')
    os.makedirs(BASE, exist_ok=True)
    if not os.path.exists(REPO):
        subprocess.run(['git', 'clone', REPO_URL, REPO])
    else:
        subprocess.run(['git', '-C', REPO, 'pull'])
    print('✅ Repositorio listo en Drive.')
else:
    print('Modo local: no se monta Drive.')

# Librerías necesarias
for pkg in ['numpy', 'scipy', 'sympy', 'matplotlib', 'requests', 'ipywidgets']:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', pkg])

sys.path.insert(0, os.path.join(REPO, 'lib'))

# Sintaxis estilo MATLAB
with open(os.path.join(REPO, 'lib', 'matlab_like.py'), encoding='utf-8') as f:
    exec(f.read(), globals())
from robomat import M, I, sin, cos, tan, var, rad, deg, evaluar, mostrar, jacobiano

# Calificador (oculto): ofuscado en Colab, fuente en tu computadora
if ES_COLAB:
    with open(os.path.join(REPO, 'grader_ofuscado.txt'), encoding='utf-8') as f:
        blob = f.read().strip()
    codigo = zlib.decompress(base64.b64decode(blob)).decode('utf-8')
else:
    with open(os.path.join(REPO, 'profe', 'grader.py'), encoding='utf-8') as f:
        codigo = f.read()
    print('🔧 Modo debug local: cargando profe/grader.py (sin ofuscar)')
exec(codigo, globals())

# Estado del equipo (se guarda en Drive para no perderlo)
RUTA_ESTADO = os.path.join(REPO, 'equipo_u2t4.json')
EQUIPO = None
if os.path.exists(RUTA_ESTADO):
    try:
        with open(RUTA_ESTADO, encoding='utf-8') as f:
            EQUIPO = json.load(f)
        print('📄 Estado del equipo recuperado:', EQUIPO.get('tema'), '-', EQUIPO.get('estado'))
    except Exception as e:
        print('No se pudo leer el estado previo:', e)

import requests

def _post(accion, **campos):
    """Llama a Apps Script y devuelve la carga útil o lanza el error del servidor."""
    payload = {'accion': accion, 'token': WEBHOOK_TOKEN}
    payload.update(campos)
    r = requests.post(APPS_SCRIPT_URL, json=payload, timeout=40)
    data = r.json()
    if data.get('status') != 'ok':
        raise RuntimeError(data.get('message', 'Error desconocido del servidor'))
    return data.get('data', {})

def _guardar_estado():
    with open(RUTA_ESTADO, 'w', encoding='utf-8') as f:
        json.dump(EQUIPO, f, ensure_ascii=False, indent=1)

print('✅ Entorno listo.')''')

md("""¿Verificaste que aparece algo como `[1] ✔ 2s` a la izquierda del bloque?

El `[n]` significa que se han ejecutado $n$ bloques. **Verifica que todos lo tengan.**""")

# ===========================================================================
# IDENTIFICACIÓN
# ===========================================================================
md("""## Identifícate (jefe de equipo)

Te identificarás con la cuenta institucional con la que montaste Google Drive.
Después escribe tu **número de control** y se validará contra la lista del grupo.""")

code(r'''# @title Identificación automática del jefe de equipo
import ipywidgets as widgets
from IPython.display import display, HTML

if ES_COLAB:
    from google.colab import auth
    import google.auth, google.auth.transport.requests
    try:
        auth.authenticate_user()
        creds, _ = google.auth.default()
        creds.refresh(google.auth.transport.requests.Request())
        info = requests.get(
            'https://www.googleapis.com/drive/v3/about?fields=user',
            headers={'Authorization': 'Bearer ' + creds.token}, timeout=20).json()
        CORREO = info.get('user', {}).get('emailAddress', '')
    except Exception as e:
        print('⚠️ No se pudo obtener tu correo automáticamente.', e)
        CORREO = ''
else:
    CORREO = input('Correo institucional (pruebas): ').strip()

if CORREO and '@' in CORREO and CORREO.lower().endswith('.tecnm.mx'):
    print('✅ Identificado: ' + CORREO)
elif CORREO:
    display(HTML('<p style="color:#b00020;background:#ffe0e0;padding:12px;border-radius:8px;'
                 'font-weight:bold">⛔ Este correo no es institucional.<br>'
                 'Usa tu cuenta @campus.tecnm.mx.</p>'))
else:
    print('No se pudo identificar el correo. Vuelve a intentar.')

# Número de control sugerido a partir del correo (si trae los 8 dígitos)
_sug = extraer_nc(CORREO) or (EQUIPO.get('jefe') if EQUIPO else '')
NC_JEFE = input('Número de control del jefe de equipo [%s]: ' % _sug).strip() or _sug
print('NC del jefe:', NC_JEFE)

# Validación contra la lista del grupo
if NC_JEFE:
    _al = _post('proyecto_equipo', NC=NC_JEFE, correo=CORREO)
    if _al.get('equipo'):
        EQUIPO = _al['equipo']
        _guardar_estado()
        print('✅ Este equipo YA tiene el tema %s (%s).' % (EQUIPO['tema'], EQUIPO['estado']))
    else:
        print('✅ NC válido y sin equipo asignado. Sigue con la selección de tema.')
else:
    print('⛔ Escribe tu número de control.')''')

md("""# Guarda el Notebook
Ve a `Archivo → Guardar una copia en Drive` y guárdalo en
`CursoMN/U2_T4_Casos_de_estudio` para conservar tu trabajo.""")

md("""---
# 1. Elige tu caso de estudio

Esta tarea **no** usa semilla por número de control: **el equipo elige su tema**.

| Paso | Quién | Celda |
|---|---|---|
| 1 | Jefe | **Ver temas disponibles** |
| 2 | Jefe | **Reservar tema** ← *queda bloqueado, ya no se puede cambiar* |
| 3 | Jefe | **Integrantes** |
| 4 | Jefe | **Registrar equipo** |
| 5 | Todo el equipo | Trabajar en el notebook |

> ⚠️ **Una vez reservado el tema, ya no se puede cambiar.** Si te equivocaste, usa la
> celda **Eliminar equipo** (hasta abajo) y vuelve a empezar.

**Bloques según el tamaño del equipo**

| Tamaño | Bloque | Temas |
|---|---|---|
| 2 | A — Básico | T1 – T4 |
| 3 | B — Intermedio | T5 – T9 |
| 4 | C — Estándar mecatrónica | T10 – T15 |
| 5 | D — Avanzado | T16 – T17 |
| 6 | E — Integrador | T18 – T19 |

El **catálogo completo** (con ecuaciones, incertidumbres y desafíos) está en el
`README.md` de la carpeta del proyecto.""")

code(r'''# @title Ver temas disponibles
from IPython.display import display, HTML

_datos = _post('proyecto_temas')
TEMAS = _datos['temas']
LIBRES = [t for t in TEMAS if t['disponible']]

print('Temas LIBRES: %d de %d\n' % (len(LIBRES), len(TEMAS)))
for t in TEMAS:
    if t['disponible']:
        print('  %-4s (%d integrantes) %s' % (t['id'], t['tamano'], t['titulo']))
print()
for t in TEMAS:
    if not t['disponible']:
        print('  %-4s OCUPADO (%s) por NC %s' % (t['id'], t['estado'], t['jefe']))

if EQUIPO:
    print('\n⚠️ Tu equipo ya tiene el tema %s. No necesitas reservar.' % EQUIPO['tema'])''')

code(r'''# @title Reservar tema (BLOQUEA el tema para tu equipo)
SL_TEMA = widgets.Dropdown(
    options=[('%s — %s' % (t['id'], t['titulo']), t['id']) for t in LIBRES],
    description='Tu tema:', layout=widgets.Layout(width='620px'))
BT_RESERVAR = widgets.Button(description='Verificar disponibilidad y reservar',
                             button_style='warning')
OUT_TEMA = widgets.Output()

def _reservar(_):
    global EQUIPO
    with OUT_TEMA:
        OUT_TEMA.clear_output()
        if EQUIPO:
            print('⚠️ Tu equipo ya tiene el tema %s (%s).' % (EQUIPO['tema'], EQUIPO['estado']))
            return
        if not NC_JEFE:
            print('⛔ Primero ejecuta la celda de identificación.')
            return
        try:
            res = _post('proyecto_reservar', NC_Jefe=NC_JEFE, correo=CORREO, tema=SL_TEMA.value)
        except Exception as e:
            print('⛔ No se pudo reservar:', e)
            print('   Vuelve a ejecutar la celda anterior para ver los temas libres.')
            return
        EQUIPO = res['equipo']
        _guardar_estado()
        print('✅', res['mensaje'])
        print('   Integrantes requeridos:', EQUIPO['tamano'])
        print('   Sigue con la celda de INTEGRANTES.')

BT_RESERVAR.on_click(_reservar)
display(widgets.VBox([SL_TEMA, BT_RESERVAR, OUT_TEMA]))''')

md("""---
# 2. Integrantes del equipo

Aparecerán **tantos selectores como integrantes** tenga tu tema. El **jefe ya viene
seleccionado** (es quien inició sesión). Elige a tus compañeros y luego registra.""")

code(r'''# @title Integrantes (un selector por integrante)
if not EQUIPO:
    print('⛔ Primero reserva tu tema (celda anterior).')
else:
    _al = _post('proyecto_alumnos')['alumnos']
    _opciones = [(a['nombre'], a['nc']) for a in _al]
    _opciones.sort()
    N_INT = int(EQUIPO['tamano'])
    _ya = [i['nc'] for i in EQUIPO.get('integrantes', [])]

    SEL = {}
    for i in range(N_INT):
        if i == 0:
            SEL[i] = widgets.Dropdown(options=_opciones, value=NC_JEFE,
                                      description='Jefe:', layout=widgets.Layout(width='620px'))
        else:
            _def = _ya[i] if len(_ya) > i else _opciones[0][1]
            SEL[i] = widgets.Dropdown(options=_opciones, value=_def,
                                      description='Integrante %d:' % (i + 1),
                                      layout=widgets.Layout(width='620px'))
    print('Tema %s — %s' % (EQUIPO['tema'], EQUIPO['titulo']))
    print('Selecciona los %d integrantes:' % N_INT)
    display(widgets.VBox(list(SEL.values())))''')

code(r'''# @title Verificar y registrar equipo
BT_REG = widgets.Button(description='Verificar y registrar equipo', button_style='success')
OUT_REG = widgets.Output()

def _registrar(_):
    global EQUIPO
    with OUT_REG:
        OUT_REG.clear_output()
        try:
            _integrantes = [SEL[i].value for i in range(len(SEL))]
        except Exception:
            print('⛔ Primero ejecuta la celda de integrantes.')
            return
        try:
            res = _post('proyecto_registrar', NC_Jefe=NC_JEFE, correo=CORREO,
                        tema=EQUIPO['tema'], integrantes=_integrantes)
        except Exception as e:
            print('⛔ No se pudo registrar:', e)
            return
        EQUIPO = res['equipo']
        _guardar_estado()
        print('✅', res['mensaje'])
        print('\nEquipo registrado:')
        for i in EQUIPO['integrantes']:
            print('   %s  %s%s' % (i['nc'], i['nombre'], '  (jefe)' if i['esJefe'] else ''))
        print('\n🎉 Listo. Ya no necesitas volver a ejecutar estas celdas.')
        print('   Avanza a la sección 4 con TU caso de estudio.')

BT_REG.on_click(_registrar)
display(widgets.VBox([BT_REG, OUT_REG]))''')

md("""### 🛑 Eliminar equipo (solo si hubo un error)

Si se equivocaron de tema o de integrantes, pueden **borrar el equipo** y volver a
empezar. Por seguridad se requieren **dos** condiciones:

1. Cambiar `PERMITIR_ELIMINAR = True` aquí abajo (por defecto `False`).
2. Que **tu** número de control **pertenezca** al equipo.

Así nadie puede borrar el equipo de otros.""")

code(r'''# @title Eliminar equipo (requiere PERMITIR_ELIMINAR = True)
PERMITIR_ELIMINAR = False   # <-- cámbialo a True solo para corregir un error
CONFIRMAR = True            # <-- debe quedar en True para borrar

if not PERMITIR_ELIMINAR:
    print('🔒 La eliminación está desactivada (PERMITIR_ELIMINAR = False).')
elif not EQUIPO:
    print('No hay equipo registrado en este notebook.')
else:
    try:
        res = _post('proyecto_eliminar', NC_Actual=NC_JEFE, tema=EQUIPO['tema'],
                    confirmar=(CONFIRMAR is True))
        print('🗑️', res['mensaje'])
        EQUIPO = None
        _guardar_estado()
        print('Vuelve a la sección 1 para elegir otro tema.')
    except Exception as e:
        print('⛔ No se pudo eliminar:', e)''')

md("""---
# 3. Tu caso de estudio

Aquí abajo aparece **solo tu proyecto** (el catálogo completo está en el `README.md`).""")

code(r'''# @title Muestra tu caso de estudio
from IPython.display import display, Markdown

if not EQUIPO:
    print('⛔ Todavía no tienes tema asignado. Regresa a la sección 1.')
else:
    TEMA = EQUIPO['tema']
    INFO = CATALOGO[TEMA]
    display(Markdown('## %s · %s' % (TEMA, INFO['titulo'])))
    display(Markdown('**Incógnita:** $%s$  (%s)' % (INFO['incognita'], INFO['unidad'])))
    display(Markdown('**Ecuación del caso:**\n\n$$%s$$' % INFO['ecuacion']))
    display(Markdown('**Desafío principal:** %s' % INFO['desafio']))
    display(Markdown('**Métodos sugeridos:** %s' % ', '.join(INFO['metodos_sugeridos'])))
    _filas = ['| Parámetro | Valor nominal | Incertidumbre |', '|---|---|---|']
    for p, spec in INFO['params'].items():
        if spec[0] == 'u':
            _filas.append('| `%s` | %.4g | uniforme en [%.4g, %.4g] |' % (p, 0.5 * (spec[1] + spec[2]), spec[1], spec[2]))
        else:
            _filas.append('| `%s` | %.6g | ±%.1f%% |' % (p, spec[1], 100 * spec[2]))
    display(Markdown('\n'.join(_filas)))
    if INFO.get('polinomico'):
        display(Markdown('> 🔺 **Tema polinómico:** se exige **Müller o Bairstow** entre tus métodos.'))''')

md(r"""---
# 4. La librería del equipo (`metodos_equipo.py`)

El equipo implementa sus métodos en **`lib/metodos_equipo.py`** (dentro de la carpeta
compartida de Drive). Ese archivo:

- tiene un `if __name__ == '__main__'` para que puedan **probarlo en su computadora**
  (`python metodos_equipo.py`) sin abrir Colab;
- se **importa** aquí abajo.

### Contrato obligatorio (¡respétalo!)

```python
# Una ecuación
g(f, p0, p1, tol, max_iter) -> (raiz, n_iter)

# Sistemas
g(F, x0, _x1, tol, max_iter) -> (vector_raiz, n_iter)
```

Los **nombres de las llaves** del diccionario `METODOS` son los que se reportan al
servidor, así que escribe los nombres "bonitos" (`'Newton-Raphson'`, `'Bisección'`…).""")

code(r'''# @title Cargar la librería del equipo
import importlib.util

RUTA_LIB = os.path.join(REPO, 'lib', 'metodos_equipo.py')
if not os.path.exists(RUTA_LIB):
    RUTA_LIB = os.path.join(REPO, 'lib', 'metodos_equipo.py')

if not os.path.exists(RUTA_LIB):
    print('⚠️ No encontré lib/metodos_equipo.py en', RUTA_LIB)
    equipo_lib = None
else:
    _spec = importlib.util.spec_from_file_location('metodos_equipo', RUTA_LIB)
    equipo_lib = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(equipo_lib)
    print('✅ Librería cargada:', RUTA_LIB)

# Recarga sin reiniciar el kernel (útil al editar la librería):
def recargar_libreria():
    import importlib
    global equipo_lib
    equipo_lib = importlib.reload(equipo_lib)
    print('🔄 Librería recargada.')
    return equipo_lib''')

md("""---
# 5. Definición simbólica del problema

Con `sympy` construimos la función del caso, su **derivada** (o el **Jacobiano** si es un
sistema) y las pasamos a funciones rápidas con `lambdify`.

> 📝 **Sobre los nombres.** En el **código** las variables se llaman con letras normales
> (`th1`, `omega`, `eps`), pero **en pantalla** se muestran como notación matemática
> ($\\theta_1$, $\\omega$, $\\varepsilon$). Es el mismo símbolo: en el código usa siempre
> el nombre normal.

> ✍️ Ya cursaron cálculo diferencial, así que **la derivada se obtiene a mano** y luego se
> comprueba contra `sympy`. La celda siguiente sirve justo para eso.""")

code(r'''# @title Definición simbólica y funciones numéricas
import numpy as np
import sympy as sp
from IPython.display import display, Markdown

MODELO = modelo(TEMA)          # viene del calificador (oculto)
ES_SISTEMA = MODELO['sistema']

if ES_SISTEMA:
    syms, exprs, sym_params = MODELO['sym']
    F_OFICIAL = exprs
    J_OFICIAL = sp.Matrix(exprs).jacobian(syms)
    display(Markdown('**Sistema de ecuaciones** $F(\\mathbf{x})=\\mathbf{0}$:'))
    for e in exprs:
        display(sp.Eq(e, 0))
    display(Markdown('**Jacobiano** $J=\\partial F/\\partial \\mathbf{x}$:'))
    display(J_OFICIAL)
else:
    x_sym, expr, sym_params = MODELO['sym']
    D_OFICIAL = sp.simplify(sp.diff(expr, x_sym))
    display(Markdown('**Ecuación** $f(%s)=0$:' % sp.latex(x_sym)))
    display(sp.Eq(expr, 0))
    display(Markdown('**Derivada** $f\'$:'))
    display(D_OFICIAL)

# Alias cómodos: ahora puedes escribir th1, omega, x, ... directamente
for _n, _s in zip(MODELO['vars'], (syms if ES_SISTEMA else [x_sym])):
    globals()[_n] = _s
print('Variables disponibles:', ', '.join(MODELO['vars']))
print('Parámetros del caso:', list(MODELO['params']))
print('Valores iniciales de referencia:', MODELO['info'].get('x0', MODELO['info'].get('intervalo')))''')

code(r'''# @title ✍️ Verifica a mano tu derivada (o tu Jacobiano)
# Obtén la derivada A MANO, escríbela aquí con sympy y compárala con la de sympy.
# Para una ecuación usa la variable con su nombre normal (th, omega, x, ...).
from IPython.display import display, Markdown

MI_DERIVADA  = None      # <-- p. ej.:  -2*sp.exp(-2*x) + sp.cos(x)
MI_JACOBIANO = None      # <-- solo si tu caso es un sistema, p. ej.: sp.Matrix([[0, -1], [1, 0]])

if not EQUIPO:
    print('⛔ Todavía no tienes tema asignado.')
elif ES_SISTEMA:
    if MI_JACOBIANO is None:
        print('Escribe tu MI_JACOBIANO (una sp.Matrix) en lugar de None.')
        print('El Jacobiano de sympy tiene forma', J_OFICIAL.shape)
    else:
        try:
            _tu = sp.Matrix(MI_JACOBIANO)
            _dif = _tu - J_OFICIAL
            display(Markdown('**Diferencia (tu Jacobiano − el de sympy):**'))
            display(_dif.applyfunc(sp.simplify))
            _n_f, _n_c = J_OFICIAL.shape
            _errs = [sp.simplify(_dif[i, j]) for i in range(_n_f) for j in range(_n_c)]
            if np.all([e == 0 for e in _errs]):
                print('✅ Se comprobó simbólicamente: tu Jacobiano coincide con el de sympy.')
            else:
                print('❌ No coincide. Las entradas distintas de cero de la diferencia te dicen cuáles revisar.')
        except Exception as _e:
            print('⚠️ No pude comprobar tu Jacobiano:', _e)
else:
    if MI_DERIVADA is None:
        print('Escribe tu MI_DERIVADA (una expresión de sympy) en lugar de None.')
        print('La derivada de sympy es:')
        display(D_OFICIAL)
    else:
        try:
            _dif = sp.simplify(D_OFICIAL - MI_DERIVADA)
            display(Markdown('**Diferencia (tu derivada − la de sympy), simplificada:**'))
            display(_dif)
            # Comprobación numérica en 3 puntos del intervalo (por si simplify no logra probarlo)
            _nom = {n: (s[1] if s[0] == 'n' else 0.5 * (s[1] + s[2])) for n, s in INFO['params'].items()}
            _vals = [_nom[n] for n in MODELO['params']]
            _lo, _hi = INFO['intervalo']
            _f_of = sp.lambdify([x_sym, list(sym_params.values())], D_OFICIAL, 'numpy')
            _f_mi = sp.lambdify([x_sym, list(sym_params.values())], MI_DERIVADA, 'numpy')
            _err = []
            for _k in (0.25, 0.5, 0.75):
                _xv = _lo + _k * (_hi - _lo)
                _a = abs(float(_f_of(_xv, _vals)))
                _b = float(_f_mi(_xv, _vals))
                _err.append(abs(_b - _a) / np.maximum(_a, 1e-12))
            _peor = float(np.max(_err))
            print('Error relativo máximo en 3 puntos: %.3e' % _peor)
            if _dif == 0 or _peor < 1e-8:
                print('✅ Tu derivada es correcta.')
                df_num = sp.lambdify(x_sym, MI_DERIVADA, 'numpy')
                print('   Quedó guardada como df_num: úsala en la sección 6 para Newton-Raphson.')
            else:
                print('❌ Todavía no coincide: revisa la regla de derivación (producto, cadena, cociente...).')
        except Exception as _e:
            print('⚠️ No pude comprobar tu derivada:', _e)
            print('   Asegúrate de escribirla con el nombre normal de la variable (th, omega, x, ...).')''')

md("""---
# 6. Tus métodos (el registro `METODOS`)

Aquí se **declara** qué métodos implementaron. Cada entrada es un *adaptador* al contrato
`(f, p0, p1, tol, max_iter) -> (raiz, n_iter)`.

> **Regla del proyecto:** al menos **3 métodos de familias distintas**
> (una *cerrada* + una *abierta* + una *híbrida/especial*).

**Familias:** *cerrado* = Bisección, Falsa posición, PFM · *abierto* = Punto fijo,
Newton-Raphson, NR modificado, Secante, Secante modificado · *híbrido* = Brent ·
*polinomios* = Müller, Bairstow.

> ⚠️ **Ojo al escribir código en estas celdas.** La configuración carga
> `matlab_like` con sintaxis estilo MATLAB (`from numpy import *`), así que
> `max`, `min`, `abs`, `any`, `all` y `sum` **son los de NumPy, no los de Python**.
> Concretamente: `max(a, b)` **falla** (`TypeError`) porque NumPy lo interpreta como
> un eje. Para comparar **dos valores** usa:
> ```python
> np.maximum(a, b)   # en vez de max(a, b)
> np.minimum(a, b)   # en vez de min(a, b)
> ```
> (Dentro de `lib/metodos_equipo.py` no hay problema: es un módulo aparte.)""")

code(r'''# @title Registro de métodos del equipo
if ES_SISTEMA:
    METODOS = {
        'Newton-Raphson multivariable':
            lambda F, x0, x1, tol, it: equipo_lib.newton_sistema(F, x0, tol=tol, max_iter=it),
        # 'Punto fijo modificado':
        #     lambda F, x0, x1, tol, it: equipo_lib.punto_fijo_sistema(F, x0, tol=tol, max_iter=it),
    }
else:
    METODOS = {
        'Bisección':      lambda f, p0, p1, tol, it: equipo_lib.biseccion(f, p0, p1, tol, it),
        'Falsa posición': lambda f, p0, p1, tol, it: equipo_lib.falsa_posicion(f, p0, p1, tol, it),
        'Newton-Raphson': lambda f, p0, p1, tol, it: equipo_lib.newton_raphson(f, p0, tol=tol, max_iter=it),
        # Si verificaste tu derivada a mano (sección 5), úsala en vez de la numérica:
        # 'Newton-Raphson (derivada a mano)':
        #     lambda f, p0, p1, tol, it: equipo_lib.newton_raphson(f, p0, tol=tol, max_iter=it, df=df_num),
        'Secante':        lambda f, p0, p1, tol, it: equipo_lib.secante(f, p0, p1, tol, it),
        # 'Brent':        lambda f, p0, p1, tol, it: equipo_lib.brent(f, p0, p1, tol, it),
        # 'Müller':       lambda f, p0, p1, tol, it: equipo_lib.muller(f, p0, p1, tol, it),
        # 'Bairstow':     lambda f, p0, p1, tol, it: equipo_lib.bairstow(f, p0, p1, tol, it),
    }

print('Métodos declarados:')
for _n in METODOS:
    print('   %-30s familia: %s' % (_n, familia(_n)))

# Detección automática (solo avisa, no califica)
if equipo_lib is not None:
    _enc, _avisos = detectar_metodos(vars(equipo_lib), list(METODOS.keys()))
    print('\nDetectados en tu librería:', _enc if _enc else '(ninguno)')
    for _a in _avisos:
        print('   ⚠️', _a)''')

md(r"""---
# 7. Simulación de Monte Carlo

Se perturban los parámetros del caso (incertidumbre real) y se corre **cada método** sobre
las **mismas** $N$ muestras. Después se compara cada resultado contra la **raíz de
referencia** (el *oráculo*), muestra por muestra.

> La incertidumbre simula tolerancias de componentes, ruido de sensores, variación de
> fabricación y errores al *aislar* la raíz.""")

code(r'''# @title Ejecutar Monte Carlo
N_MC = 1000                              # tamaño de la simulación
SEMILLA_EQUIPO = semilla(TEMA, NC_JEFE)  # misma semilla para todos los métodos

print('Simulando %d muestras para el tema %s...' % (N_MC, TEMA))
RES = evaluar_tema(TEMA, METODOS, N=N_MC, seed=SEMILLA_EQUIPO)
print('Listo.\n')

print('%-30s %8s %8s %10s %10s %8s' % ('Método', '%éxito', '%diverg', 'mediana', 'media', 'mediana_err'))
print('-' * 84)
for _m, _d in RES['metodos'].items():
    print('%-30s %7.1f%% %7.1f%% %10.0f %10.1f %10.1e' % (
        _m, 100 * _d['pct_exito'], 100 * _d['pct_diverge'],
        np.nanmedian(_d['n_iter']), np.nanmean(_d['n_iter']),
        np.nanmedian(_d['err_ref'])))
print('\nUn método "CUENTA" si acierta la raíz de referencia en >= %.0f%% de las muestras.'
      % (100 * UMBRAL_EXITO))''')

md("""---
# 8. Gráficos de desempeño

Primero el **histograma comparativo** y la **tasa de divergencia**; luego el
**box plot** (la vista más informativa) y la **distribución de la respuesta física**.""")

code(r'''# @title Histograma de iteraciones y % de divergencia
import matplotlib.pyplot as plt

_met = list(RES['metodos'].keys())
_n_col = len(_met) if len(_met) >= 2 else 2
_col = plt.cm.tab10(np.linspace(0, 1, _n_col))

fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
for i, m in enumerate(_met):
    it = RES['metodos'][m]['n_iter']
    it = it[np.isfinite(it)]
    ax[0].hist(it, bins=30, alpha=0.55, label=m, color=_col[i])
ax[0].set_title('Distribución de iteraciones por método')
ax[0].set_xlabel('iteraciones'); ax[0].set_ylabel('frecuencia')
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)

_div = [100 * RES['metodos'][m]['pct_diverge'] for m in _met]
ax[1].bar(range(len(_met)), _div, color=_col[:len(_met)])
ax[1].set_xticks(range(len(_met)))
ax[1].set_xticklabels(_met, rotation=30, ha='right', fontsize=8)
ax[1].set_title('Tasa de divergencia (% sin acertar la raíz)')
ax[1].set_ylabel('%'); ax[1].grid(alpha=0.3, axis='y')
plt.tight_layout(); plt.show()''')

code(r'''# @title ⭐ Box plot comparativo de iteraciones
# Muestra mediana, dispersión y outliers: se ve de inmediato por qué un método
# es mejor que otro (menos iteraciones y menos dispersión).
_ancho = 1.6 * len(_met)
if _ancho < 7:
    _ancho = 7
fig, ax = plt.subplots(figsize=(_ancho, 5))
_datos = [RES['metodos'][m]['n_iter'][np.isfinite(RES['metodos'][m]['n_iter'])] for m in _met]
bp = ax.boxplot(_datos, patch_artist=True, showfliers=True)
for i, caja in enumerate(bp['boxes']):
    caja.set_facecolor(_col[i % len(_col)]); caja.set_alpha(0.6)
ax.set_xticks(range(1, len(_met) + 1))
ax.set_xticklabels(_met, rotation=30, ha='right')
ax.set_title('Box plot de iteraciones por método (tema %s)' % TEMA)
ax.set_ylabel('iteraciones'); ax.grid(alpha=0.3, axis='y')
plt.tight_layout(); plt.show()

_ord = sorted(_met, key=lambda m: np.nanmedian(RES['metodos'][m]['n_iter']))
print('Ordenados por mediana de iteraciones (más rápido primero):')
for m in _ord:
    d = RES['metodos'][m]
    print('   %-30s mediana=%4.0f  dispersión(IQR)=%4.0f  fallos=%5.1f%%' % (
        m, np.nanmedian(d['n_iter']),
        np.nanpercentile(d['n_iter'], 75) - np.nanpercentile(d['n_iter'], 25),
        100 * d['pct_diverge']))''')

code(r'''# @title Distribución de la respuesta física ante la incertidumbre
_ref = RES['raiz_ref']
if ES_SISTEMA:
    fig, ax = plt.subplots(1, _ref.shape[1], figsize=(5 * _ref.shape[1], 4))
    if _ref.shape[1] == 1:
        ax = [ax]
    for j in range(_ref.shape[1]):
        ax[j].hist(_ref[np.isfinite(_ref[:, j]), j], bins=30, color='teal', alpha=0.75)
        ax[j].set_title('Distribución de %s' % MODELO['vars'][j])
        ax[j].set_xlabel(MODELO['vars'][j]); ax[j].set_ylabel('frecuencia')
        ax[j].grid(alpha=0.3)
else:
    _rr = _ref[np.isfinite(_ref)]
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
    ax[0].hist(_rr, bins=30, color='teal', alpha=0.75)
    ax[0].set_title('Distribución de la raíz física (%s)' % str(MODELO['vars'][0]))
    ax[0].set_xlabel(str(MODELO['vars'][0])); ax[0].set_ylabel('frecuencia'); ax[0].grid(alpha=0.3)
    ax[1].boxplot(_rr, patch_artist=True)
    ax[1].set_title('Dispersión de la respuesta física'); ax[1].grid(alpha=0.3, axis='y')
    print('Respuesta física: media=%.6g  mediana=%.6g  desv=%.3g  min=%.6g  max=%.6g'
          % (np.mean(_rr), np.median(_rr), np.std(_rr), np.min(_rr), np.max(_rr)))
plt.tight_layout(); plt.show()

print('\nEsto responde: ¿qué tanto cambia la respuesta del sistema por la incertidumbre?')''')

md("""---
# 9. Conclusiones de ingeniería

Cinco preguntas de criterio. **Dos se responden con TUS propios resultados** (las califica
el oráculo comparando con tus métricas) y **tres son conceptuales**.

> 🎓 **La pregunta de la exposición:** *"Si estuvieran diseñando el firmware del controlador
> de este sistema mecatrónico en tiempo real, ¿qué método programarían y por qué?"*""")

code(r'''# @title Preguntas de criterio
import ipywidgets as widgets
from IPython.display import display, Markdown

PREGUNTAS = []

# --- Q1 y Q2: se responden con las métricas reales de la simulación ---
_conteo = [m for m, d in RES['metodos'].items() if d['cuenta']] or list(RES['metodos'].keys())
_rapidos = sorted(_conteo, key=lambda m: np.nanmedian(RES['metodos'][m]['n_iter']))
_lentos = sorted(_conteo, key=lambda m: -RES['metodos'][m]['pct_diverge'])

PREGUNTAS.append({
    'id': 'M1',
    'texto': 'Según TU simulación, ¿qué método necesitó MENOS iteraciones?',
    'opciones': _rapidos, 'correcta': 0,
    'explica': 'El de menor mediana; suele ser el de orden de convergencia más alto.',
})
PREGUNTAS.append({
    'id': 'M2',
    'texto': 'Según TU simulación, ¿qué método falló (no llegó a la raíz) en MÁS muestras?',
    'opciones': _lentos, 'correcta': 0,
    'explica': 'El de mayor % de divergencia; casi siempre depende de un arranque mal aislado.',
})
for _p in PREGUNTAS_CONCEPTO:
    PREGUNTAS.append({'id': _p['id'], 'texto': _p['pregunta'],
                      'opciones': _p['opciones'], 'correcta': _p['correcta'],
                      'explica': ''})

W_RESP = {}
for _i, _p in enumerate(PREGUNTAS):
    display(Markdown('**%d. %s**' % (_i + 1, _p['texto'])))
    W_RESP[_p['id']] = widgets.RadioButtons(
        options=['(%s) %s' % (chr(97 + k), o) for k, o in enumerate(_p['opciones'])],
        layout=widgets.Layout(width='720px'))
    display(W_RESP[_p['id']])

BT_CRIT = widgets.Button(description='Calificar mis respuestas', button_style='info')
OUT_CRIT = widgets.Output()

def _calificar_criterio(_):
    global NOTA_CRITERIO
    with OUT_CRIT:
        OUT_CRIT.clear_output()
        aciertos = 0
        for _p in PREGUNTAS:
            _sel = W_RESP[_p['id']].value
            _idx = [chr(97 + k) for k in range(len(_p['opciones']))].index(_sel[1])
            _ok = (_idx == _p['correcta'])
            aciertos += int(_ok)
            print('%s %-4s %s' % ('✅' if _ok else '❌', _p['id'], _p['texto'][:62]))
            if not _ok and _p.get('explica'):
                print('      ↳ %s' % _p['explica'])
        NOTA_CRITERIO = 100.0 * aciertos / len(PREGUNTAS)
        print('\nAciertos: %d de %d  →  %.0f / 100' % (aciertos, len(PREGUNTAS), NOTA_CRITERIO))

BT_CRIT.on_click(_calificar_criterio)
NOTA_CRITERIO = 0.0
display(widgets.VBox([BT_CRIT, OUT_CRIT]))''')

md("""---
# 10. Calificación automática y envío

Aquí se calcula tu nota de la parte automática (métodos + criterio) y se envía al
servidor junto con **los métodos que usaste**.

| Parte | Peso | Cómo se calcula |
|---|---|---|
| Métodos (implementación + Monte Carlo) | 40% | `base` + extras con tope |
| Preguntas de criterio | 20% | aciertos |

El **40%** restante (informe y exposición) lo evalúa el profesor.""")

code(r'''# @title Calificar, consejos y enviar
NOTA_METODOS, DESGLOSE = calificar(RES)

print('=' * 74)
print('PARTE 1 — MÉTODOS Y MONTE CARLO')
print('=' * 74)
for m, d in RES['metodos'].items():
    _etq = 'CUENTA' if d['cuenta'] else 'no cuenta'
    _extra = '  ⚠️ envoltorio trivial' if d.get('sospechoso') else ''
    print('  %-30s %-10s (%5.1f%% éxito)%s' % (m, _etq, 100 * d['pct_exito'], _extra))
print('\n  Métodos válidos: %d' % len(DESGLOSE['validos']))
print('  Familias distintas: %s' % ', '.join(DESGLOSE['familias']) if DESGLOSE['familias'] else '  Familias distintas: (ninguna)')
print('  Base: %d   Bonificación por métodos extra: +%d   →  %.0f / 100'
      % (DESGLOSE['base'], DESGLOSE['bonus'], NOTA_METODOS))
if DESGLOSE['castigo']:
    print('  🔻 %s' % DESGLOSE['castigo'])

print('\n💡 Consejos automáticos:')
for _c in consejos(RES):
    print('   · %s' % _c)

print('\n' + '=' * 74)
print('PARTE 2 — PREGUNTAS DE CRITERIO: %.0f / 100' % NOTA_CRITERIO)
CALIFICACION = round((2 * NOTA_METODOS + NOTA_CRITERIO) / 3, 2)
print('NOTA AUTOMÁTICA (métodos 2/3 + criterio 1/3): %.2f / 100' % CALIFICACION)
print('=' * 74)

# --- Envío ---
if not EQUIPO:
    print('\n⛔ No se puede enviar: no hay equipo registrado.')
else:
    try:
        _r = enviar_resultado(NC_JEFE, TEMA, list(METODOS.keys()), CALIFICACION,
                              correo=CORREO, alcance='equipo')
        print('\n✅ Enviado a la hoja de resultados:', _r.get('data', _r).get('mensaje', 'ok'))
        print('   Equipo %s · tema %s · %d integrante(s) actualizados'
              % (EQUIPO['equipo'], TEMA, _r.get('data', _r).get('actualizados', 1)))
    except Exception as e:
        print('\n⚠️ No se pudo enviar todavía:', e)
        print('   Guarda el notebook y avisa al profesor. Tu resultado NO se perdió.')

print('\n--- Guarda el notebook en Drive (Archivo → Guardar) ---')''')

# ===========================================================================
# ESCRITURA
# ===========================================================================
import io
ruta = "U2_T4_Casos_de_estudio.ipynb"
with io.open(ruta, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

n_md = sum(1 for c in nb["cells"] if c["cell_type"] == "markdown")
n_code = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
print("Notebook generado: %s" % ruta)
print("Celdas: %d markdown + %d código = %d" % (n_md, n_code, n_md + n_code))





