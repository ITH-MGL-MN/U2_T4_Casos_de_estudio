# -*- coding: utf-8 -*-
"""
tools/generar_notebook.py — Regenera U2_T4_Casos_de_estudio.ipynb.

Parte del notebook original (flujo de equipos/temas por Apps Script, que se
conserva) y reemplaza las celdas que cambian en esta entrega:

  * celda de configuración: carga el motor con MODO_MOTOR (modulos/bundle/blob)
  * gráficas: ahora interactivas con plotly (lib/metodos_equipo.py)
  * calificación: solo la SELECCIÓN de métodos (lo demás se revisa a mano)

Uso:  python tools/generar_notebook.py
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(RAIZ, '..', 'U2_T4_Casos_de_estudio', 'U2_T4_Casos_de_estudio.ipynb')
DESTINO = os.path.join(RAIZ, 'U2_T4_Casos_de_estudio.ipynb')


def _celda(tipo, fuente):
    return {'cell_type': tipo, 'metadata': {}, 'source': fuente.splitlines(keepends=True)}


# =====================================================================
#  Celdas nuevas / reescritas
# =====================================================================
CELDA_CONFIG = '''\
#@title ⚙️ Configuración general — ejecuta esta celda **PRIMERO** (no modificar)
# ============================================================
# Detecta si corre en Google Colab o en tu computadora, monta Drive y
# carga el motor de la tarea (ver MODO_MOTOR más abajo).
# ============================================================
import base64, importlib, os, subprocess, sys, zlib, json

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Markdown, display

try:
    import google.colab
    ES_COLAB = True
except ImportError:
    ES_COLAB = False

# --- Repositorio de la tarea  <-- EDITAR SOLO SI CAMBIA EL REPO ------
REPO_URL = 'https://github.com/ITH-MGL-MN/U2_T4_Casos_de_estudio.git'
REPO_NOMBRE = 'U2_T4_Casos_de_estudio'

# --- Solo en tu computadora: de dónde sale el motor ---
#   "modulos" -> profe/** tal cual, importado como paquete (para depurar)
#   "bundle"  -> grader_local.py, el motor APLANADO (forma exacta de Colab)
#   "blob"    -> grader_ofuscado.txt, lo que recibe el alumno
MODO_MOTOR = "modulos"

if ES_COLAB:
    BASE = "/content/drive/MyDrive/CursoMN"
    REPO = os.path.join(BASE, REPO_NOMBRE)
else:
    REPO = os.getcwd()
    for _ in range(4):
        if os.path.exists(os.path.join(REPO, "grader_local.py")):
            break
        _padre = os.path.dirname(REPO)
        if _padre == REPO:
            break
        REPO = _padre
    if not os.path.exists(os.path.join(REPO, "grader_local.py")):
        REPO = r"o:\\Mi unidad\\CursoMN\\U2_T4_Casos_de_estudio"

MODO = "blob" if ES_COLAB else MODO_MOTOR
print("Modo          :", "Google Colab" if ES_COLAB else "PC local")
print("Carpeta tarea :", REPO)

# ============================================================
# Montar Drive y traer el repositorio  (solo en Colab)
# ============================================================
if ES_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    os.makedirs(BASE, exist_ok=True)
    try:
        if not os.path.exists(REPO):
            subprocess.run(["git", "clone", REPO_URL, REPO], check=True)
        else:
            subprocess.run(["git", "-C", REPO, "pull"], check=True)
        print("✅ Repositorio listo en Drive.")
    except Exception as _e:
        print("⚠️ No se pudo clonar/actualizar el repositorio:", _e)
        print("   Si la carpeta ya existe en tu Drive puedes continuar.")
else:
    print("Modo local: no se monta Drive.")

# ============================================================
# Librerías necesarias
# ============================================================
for _pkg in ("numpy", "scipy", "sympy", "matplotlib", "requests", "ipywidgets", "plotly"):
    try:
        importlib.import_module(_pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", _pkg])

# ============================================================
# Motor de la tarea
# ============================================================
# El motor vive aparte del cuaderno y este recibe solo la API que el motor
# declara en su `__all__`. En Colab se usa el blob; en local, MODO_MOTOR.
sys.path.insert(0, REPO)

if MODO == "modulos":
    from profe.ui.cuaderno import *      # noqa: F401,F403
else:
    if MODO == "blob":
        _ruta = os.path.join(REPO, "grader_ofuscado.txt")
        with open(_ruta, encoding="utf-8") as f:
            _blob = f.read().strip()
        codigo = zlib.decompress(base64.b64decode(_blob)).decode("utf-8")
    else:
        _ruta = os.path.join(REPO, "grader_local.py")
        with open(_ruta, encoding="utf-8") as f:
            codigo = f.read()
    _MOTOR = {}
    try:
        exec(codigo, _MOTOR)
    except Exception as _e:
        raise RuntimeError(
            "No pude cargar el motor desde %s.\\n"
            "En local: ejecuta  python tools/build.py  para generarlo.\\n"
            "Detalle: %r" % (_ruta, _e))
    globals().update({_n: _MOTOR[_n] for _n in _MOTOR["__all__"]})

print("Motor cargado :", MODO)

# ============================================================
# Preludio estilo MATLAB + robomat
# ============================================================
sys.path.insert(0, os.path.join(REPO, "lib"))
with open(os.path.join(REPO, "lib", "matlab_like.py"), encoding="utf-8") as f:
    exec(f.read(), globals())
from robomat import M, I, sin, cos, tan, var, rad, deg, evaluar, mostrar, jacobiano
print("Preludio MATLAB:", os.path.join(REPO, "lib", "matlab_like.py"))

# ============================================================
# Herramientas de visualización (gráficas interactivas plotly)
# ============================================================
# Viven en tools/visualizar.py, FUERA del motor: no forman parte del sistema
# de calificación, así que puedes leerlas y reutilizarlas.
sys.path.append(os.path.join(REPO, "tools"))
try:
    import visualizar
    importlib.reload(visualizar)
except ImportError as _e:
    raise RuntimeError(
        "No encontré tools/visualizar.py, que las gráficas interactivas usan.\\n"
        "En la carpeta de la tarea ese archivo debe estar junto al cuaderno.\\n"
        "Detalle: %r" % (_e,))
print("Visualización :", os.path.join(REPO, "tools", "visualizar.py"))

# ============================================================
# Estado del equipo (se guarda en Drive para no perderlo)
# ============================================================
RUTA_ESTADO = os.path.join(REPO, "equipo_u2t4.json")
EQUIPO = None
if os.path.exists(RUTA_ESTADO):
    try:
        with open(RUTA_ESTADO, encoding="utf-8") as f:
            EQUIPO = json.load(f)
        print("📄 Estado del equipo recuperado:", EQUIPO.get("tema"), "-", EQUIPO.get("estado"))
    except Exception as e:
        print("No se pudo leer el estado previo:", e)

import requests

def _post(accion, **campos):
    """Llama a Apps Script y devuelve la carga útil o lanza el error del servidor."""
    payload = {"accion": accion, "token": WEBHOOK_TOKEN}
    payload.update(campos)
    r = requests.post(APPS_SCRIPT_URL, json=payload, timeout=40)
    data = r.json()
    if data.get("status") != "ok":
        raise RuntimeError(data.get("message", "Error desconocido del servidor"))
    return data.get("data", {})

def _guardar_estado():
    with open(RUTA_ESTADO, "w", encoding="utf-8") as f:
        json.dump(EQUIPO, f, ensure_ascii=False, indent=1)

print("✅ Entorno listo. Ahora ejecuta la celda de identificación.")
'''

CELDA_AISLAR = '''\
# @title 🔍 Aísla la raíz (gráfica interactiva)
# Los métodos CERRADOS (bisección, falsa posición, punto fijo modificado) no
# pueden ni empezar si en los extremos del intervalo f(x) NO cambia de signo.
# Ese intervalo es el resultado de tu ANÁLISIS GRÁFICO, y es lo que se usa en
# toda la simulación.
import numpy as np
from IPython.display import display, Markdown

MIS_LIMITES = None       # <-- opcional: propón tu propio intervalo, p. ej. (0.005, 0.03)

if not EQUIPO:
    print("⛔ Todavía no tienes tema asignado.")
elif ES_SISTEMA:
    print("Tu caso es un SISTEMA de ecuaciones: se resuelve con Newton multivariable")
    print("(Jacobiano), no con métodos de intervalo, así que aquí no hay que aislar.")
else:
    _lo, _hi = INFO["intervalo"]
    _nom = {n: (s[1] if s[0] == "n" else 0.5 * (s[1] + s[2])) for n, s in INFO["params"].items()}
    _raices = oraculo_escalar_todas(lambda z: MODELO["f_arr"](z, _nom), _lo, _hi)
    _r = _raices[0] if _raices else float("nan")

    _xs = np.linspace(_lo, _hi, 800)
    _fig = visualizar.graficar_funcion(
        lambda z: MODELO["f_arr"](np.asarray(z, dtype=float), _nom),
        _xs, raiz=_r, nombre_var=MODELO["vars"][0],
        titulo="Tu caso: %s — %s" % (TEMA, INFO["titulo"]))
    _fig.show(config=visualizar.config_plotly())

    _fa = MODELO["f_arr"](np.array([_lo]), _nom)[0]
    _fb = MODELO["f_arr"](np.array([_hi]), _nom)[0]
    print("Intervalo del tema : (%.6g, %.6g)" % (_lo, _hi))
    print("f(extremo izquierdo) = %+.6g" % _fa)
    print("f(extremo derecho)   = %+.6g" % _fb)
    print("¿Cambia de signo?    : %s" % ("SÍ ✅ el intervalo aísla la raíz"
                                          if _fa * _fb < 0 else "NO ⚠️"))
    print("Raíz con valores nominales: %.8g" % _r)
    print("Número de cruces del eje dentro del intervalo: %d" % len(_raices))

    display(Markdown(
        "Verifica con tu equipo que la curva cruce el eje **una sola vez** dentro del intervalo.  \\n"
        "Las perturbaciones del Monte Carlo son **pequeñas** (±1–5 %), así que este **mismo** "
        "intervalo contiene la raíz en **todas** las muestras de la simulación. **No hay que "
        "recalcularlo muestra por muestra.**"))

    if MIS_LIMITES is not None:
        _a, _b = MIS_LIMITES
        _za = MODELO["f_arr"](np.array([_a]), _nom)[0]
        _zb = MODELO["f_arr"](np.array([_b]), _nom)[0]
        _ok = _za * _zb < 0
        print("\\nTu intervalo (%g, %g): f(a)=%+.4g  f(b)=%+.4g  →  %s"
              % (_a, _b, _za, _zb, "AÍSLA ✅" if _ok else "NO aísla ❌"))
        if _ok:
            print("   ¡Bien! Ancho = %.4g. Cuanto más angosto, menos iteraciones necesita bisección." % (_b - _a))
'''

CELDA_METODOS = '''\
# @title Registro de métodos del equipo (TU SELECCIÓN — esto es lo que se autocalifica)
# Los métodos YA están implementados en lib/metodos_equipo.py. Aquí solo eliges
# CUÁLES quieres comparar. Para eso comenta (con #) o borra los que NO quieras.
#
# Regla: deja en METODOS  →  TODOS los métodos sugeridos de tu caso (los ves en
# la sección 3)  +  al menos UN método que NO esté sugerido (un contraejemplo,
# para contrastar en tu informe). En los casos de SISTEMA solo hay 2 métodos y
# ambos son sugeridos, así que ahí no se pide contraejemplo.

if ES_SISTEMA:
    METODOS = {
        "Newton-Raphson multivariable":
            lambda F, x0, x1, tol, it: equipo_lib.newton_sistema(F, x0, tol=tol, max_iter=it),
        "Punto fijo modificado":
            lambda F, x0, x1, tol, it: equipo_lib.punto_fijo_sistema(F, x0, tol=tol, max_iter=it),
    }
else:
    METODOS = {
        "Bisección":              lambda f, p0, p1, tol, it: equipo_lib.biseccion(f, p0, p1, tol, it),
        "Falsa posición":         lambda f, p0, p1, tol, it: equipo_lib.falsa_posicion(f, p0, p1, tol, it),
        "Punto fijo modificado":  lambda f, p0, p1, tol, it: equipo_lib.punto_fijo_modificado(f, p0, p1, tol, it),
        "Punto fijo":             lambda f, p0, p1, tol, it: equipo_lib.punto_fijo(f, p0, tol=tol, max_iter=it),
        "Newton-Raphson":         lambda f, p0, p1, tol, it: equipo_lib.newton_raphson(f, p0, tol=tol, max_iter=it),
        "NR modificado":          lambda f, p0, p1, tol, it: equipo_lib.nr_modificado(f, p0, tol=tol, max_iter=it),
        "Secante":                lambda f, p0, p1, tol, it: equipo_lib.secante(f, p0, p1, tol, it),
        "Secante modificado":     lambda f, p0, p1, tol, it: equipo_lib.secante_modificada(f, p0, tol=tol, max_iter=it),
        "Brent":                  lambda f, p0, p1, tol, it: equipo_lib.brent(f, p0, p1, tol, it),
        "Müller":                 lambda f, p0, p1, tol, it: equipo_lib.muller(f, p0, p1, tol=tol, max_iter=it),
        "Bairstow":               lambda f, p0, p1, tol, it: equipo_lib.bairstow(f, p0, p1, tol=tol, max_iter=it),
    }

print("Métodos seleccionados:")
for _n in METODOS:
    print("   %-30s familia: %s" % (_n, familia(_n)))

# Aviso (no califica): qué métodos sugeridos te faltan por seleccionar.
_sug_norm = metodos_sugeridos_para(TEMA)
print("\\nMétodos sugeridos de tu caso:", ", ".join(_sug_norm))
for _m in _sug_norm:
    print("   %-30s %s" % (_m, "✅ seleccionado" if _m in METODOS else "⚠️ no lo has seleccionado"))
'''

CELDA_MC = '''\
# @title Ejecutar Monte Carlo
N_MC = 1000                              # tamaño de la simulación
SEMILLA_EQUIPO = semilla(TEMA, NC_JEFE)  # misma semilla para todos los métodos

print("Simulando %d muestras para el tema %s..." % (N_MC, TEMA))
RES = evaluar_tema(TEMA, METODOS, N=N_MC, seed=SEMILLA_EQUIPO)
print("Listo.\\n")

print("%-30s %8s %8s %10s %10s %10s" % ("Método", "%éxito", "%diverg", "mediana", "media", "mediana_err"))
print("-" * 84)
for _m, _d in RES["metodos"].items():
    print("%-30s %7.1f%% %7.1f%% %10.0f %10.1f %10.1e" % (
        _m, 100 * _d["pct_exito"], 100 * _d["pct_diverge"],
        np.nanmedian(_d["n_iter"]), np.nanmean(_d["n_iter"]),
        np.nanmedian(_d["err_ref"])))
print("\\nUn método \\"CUENTA\\" si acierta la raíz de referencia en >= %.0f%% de las muestras."
      % (100 * UMBRAL_EXITO))
'''

CELDA_HIST = '''\
# @title 📊 Histograma de iteraciones y % de divergencia (interactivo)
_fig = visualizar.graficar_histograma(RES)
_fig.show(config=visualizar.config_plotly())
'''

CELDA_BOX = '''\
# @title ⭐ Box plot comparativo de iteraciones (interactivo)
_fig = visualizar.graficar_boxplot(RES)
_fig.show(config=visualizar.config_plotly())

_met = list(RES["metodos"].keys())
_ord = sorted(_met, key=lambda m: np.nanmedian(RES["metodos"][m]["n_iter"]))
print("Ordenados por mediana de iteraciones (más rápido primero):")
for m in _ord:
    d = RES["metodos"][m]
    print("   %-30s mediana=%4.0f  dispersión(IQR)=%4.0f  fallos=%5.1f%%" % (
        m, np.nanmedian(d["n_iter"]),
        np.nanpercentile(d["n_iter"], 75) - np.nanpercentile(d["n_iter"], 25),
        100 * d["pct_diverge"]))
'''

CELDA_DIST = '''\
# @title 📈 Distribución de la respuesta física ante la incertidumbre (interactivo)
_fig = visualizar.graficar_distribucion(RES, modelo=MODELO, es_sistema=ES_SISTEMA)
_fig.show(config=visualizar.config_plotly())

if not ES_SISTEMA:
    _rr = RES["raiz_ref"][np.isfinite(RES["raiz_ref"])]
    print("Respuesta física: media=%.6g  mediana=%.6g  desv=%.3g  min=%.6g  max=%.6g"
          % (np.mean(_rr), np.median(_rr), np.std(_rr), np.min(_rr), np.max(_rr)))
print("\\nEsto responde: ¿qué tanto cambia la respuesta del sistema por la incertidumbre?")
'''

CELDA_CRITERIO = '''\
# @title 🎓 Preguntas de criterio (para el informe — NO se autocalifican)
from IPython.display import display, Markdown

_conteo = [m for m, d in RES["metodos"].items() if d["cuenta"]] or list(RES["metodos"].keys())
_rapido = min(_conteo, key=lambda m: np.nanmedian(RES["metodos"][m]["n_iter"]))
_fallador = max(RES["metodos"].keys(), key=lambda m: RES["metodos"][m]["pct_diverge"])

display(Markdown("### 1. Según TU simulación, ¿qué método necesitó MENOS iteraciones?"))
display(Markdown("**%s** (mediana %d iteraciones)." % (
    _rapido, np.nanmedian(RES["metodos"][_rapido]["n_iter"]))))

display(Markdown("### 2. ¿Qué método falló (no llegó a la raíz) en MÁS muestras?"))
display(Markdown("**%s** (%.1f%% de divergencia)." % (
    _fallador, 100 * RES["metodos"][_fallador]["pct_diverge"])))

display(Markdown("### 3. Preguntas conceptuales (para la exposición)"))
for _p in PREGUNTAS_CONCEPTO:
    display(Markdown("- **%s**: %s" % (_p["id"], _p["texto"])))

display(Markdown(
    "> 🎓 **La pregunta de la exposición:** *\\"Si estuvieran diseñando el firmware del "
    "controlador de este sistema mecatrónico en tiempo real, ¿qué método programarían y por qué?\\"*"))
'''

CELDA_CALIFICAR = '''\
# @title ✅ Calificar selección y enviar
NOTA_METODOS, DESGLOSE = calificar(TEMA, list(METODOS.keys()), RES)

print("=" * 74)
print("AUTOCALIFICACIÓN — SELECCIÓN DE MÉTODOS")
print("=" * 74)
print("Caso: %s — %s" % (TEMA, RES["titulo"]))
print("Seleccionaste  :", ", ".join(DESGLOSE["seleccion"]))
print("Sugeridos      :", ", ".join(DESGLOSE["sugeridos"]))
print("Faltantes      :", ", ".join(DESGLOSE["faltantes"]) if DESGLOSE["faltantes"] else "(ninguno) ✅")
print("Contraejemplos :", ", ".join(DESGLOSE["contraejemplos"]) if DESGLOSE["contraejemplos"]
      else ("(no se pide en casos de sistema)" if not DESGLOSE["requiere_contraejemplo"] else "(ninguno) ⚠️"))
print("Familias       :", ", ".join(DESGLOSE["familias"]))

if DESGLOSE["aprueba"]:
    print("\\n✅ SELECCIÓN CORRECTA: incluiste los métodos correctos"
          + ("" if not DESGLOSE["requiere_contraejemplo"] else " y al menos un contraejemplo") + ".")
else:
    print("\\n⚠️ SELECCIÓN INCOMPLETA:")
    if DESGLOSE["faltantes"]:
        print("   Te faltan los métodos sugeridos:", ", ".join(DESGLOSE["faltantes"]))
    if DESGLOSE["requiere_contraejemplo"] and not DESGLOSE["contraejemplos"]:
        print("   Agrega al menos un método NO sugerido (un contraejemplo).")

print("\\n💡 Consejos:")
for _c in consejos(RES):
    print("   · %s" % _c)

# --- Envío ---
if not EQUIPO:
    print("\\n⛔ No se puede enviar: no hay equipo registrado.")
else:
    try:
        _r = enviar_resultado(NC_JEFE, TEMA, list(METODOS.keys()), NOTA_METODOS,
                              correo=CORREO, alcance="equipo")
        print("\\n✅ Enviado a la hoja de resultados:", _r.get("data", _r).get("mensaje", "ok"))
    except Exception as e:
        print("\\n⚠️ No se pudo enviar todavía:", e)
        print("   Guarda el notebook y avisa al profesor. Tu resultado NO se perdió.")

print("\\n--- Guarda el notebook en Drive (Archivo → Guardar) ---")
'''

# Índices de celdas del notebook ORIGINAL que se conservan sin cambios.
CONSERVAR = {0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 30, 32}

REEMPLAZOS = {
    2: ("code", CELDA_CONFIG),
    21: ("code", CELDA_AISLAR),
    23: ("code", CELDA_METODOS),
    25: ("code", CELDA_MC),
    27: ("code", CELDA_HIST),
    28: ("code", CELDA_BOX),
    29: ("code", CELDA_DIST),
    31: ("code", CELDA_CRITERIO),
    33: ("code", CELDA_CALIFICAR),
}


def generar():
    with open(ORIGEN, encoding="utf-8") as f:
        nb = json.load(f)

    celdas_nuevas = []
    for i, celda in enumerate(nb["cells"]):
        if i in REEMPLAZOS:
            tipo, fuente = REEMPLAZOS[i]
            celdas_nuevas.append(_celda(tipo, fuente))
        elif i in CONSERVAR:
            celdas_nuevas.append(celda)
        else:
            celdas_nuevas.append(celda)  # por seguridad: no se pierde nada

    nb["cells"] = celdas_nuevas
    nb["metadata"].setdefault("kernelspec", {"name": "python3",
                                            "display_name": "Python 3",
                                            "language": "python"})
    with open(DESTINO, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("Notebook regenerado:", DESTINO)
    print("Celdas:", len(celdas_nuevas))


if __name__ == "__main__":
    generar()
