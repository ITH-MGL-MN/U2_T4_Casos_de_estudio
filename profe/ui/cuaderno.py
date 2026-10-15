# -*- coding: utf-8 -*-
"""
profe/ui/cuaderno.py — Interfaz pública del motor (el contrato del cuaderno).

El cuaderno carga el motor en su propio namespace y de ahí copia SOLO la API
declarada en `__all__` (al final de este archivo). Todo lo demás es interno.

A diferencia de U2_T3B (que sembraba un ejercicio por alumno), U2_T4 es un
PROYECTO POR EQUIPOS: cada equipo elige un caso y hace Monte Carlo. La
calificación automática se reduce a la SELECCIÓN de métodos (ver
profe/core/evaluator.py); las gráficas (plotly, interactivas) se generan con
lib/metodos_equipo.py y tools/visualizar.py.
"""
from profe.core import (
    CATALOGO,
    FAMILIA_DE,
    MAX_ITER,
    TAREA,
    REPO_URL,
    REPO_NOMBRE,
    TAU_X,
    TAU_ABS,
    UMBRAL_EXITO,
    MOTIVOS_TEXTO,
    familia,
    familia_de,
    es_sistema,
    metodos_sugeridos_para,
    detectar_metodos,
    extraer_nc,
    semilla,
    modelo,
    oraculo_escalar,
    oraculo_escalar_todas,
    oraculo_sistema,
    mapa_metodos,
    muestrear,
    evaluar_tema,
    calificar,
    consejos,
    preguntas_criterio,
    enviar_resultado,
)

# Configuración del webhook (la lee el cuaderno para sus llamadas a Apps Script).
from profe.config import obtener_configuracion
_CFG, _PREGUNTAS = obtener_configuracion()
WEBHOOK_TOKEN = _CFG['evaluacion']['webhook_token']
APPS_SCRIPT_URL = _CFG['evaluacion']['apps_script_url']

# Preguntas conceptuales de criterio (listas para el cuaderno). Ya no se
# autocalifican: son material del informe y de la exposición.
PREGUNTAS_CONCEPTO = preguntas_criterio()


__all__ = [
    'CATALOGO', 'FAMILIA_DE', 'UMBRAL_EXITO', 'MOTIVOS_TEXTO',
    'WEBHOOK_TOKEN', 'APPS_SCRIPT_URL', 'PREGUNTAS_CONCEPTO',
    'familia', 'familia_de', 'es_sistema', 'metodos_sugeridos_para', 'detectar_metodos',
    'extraer_nc', 'semilla',
    'modelo', 'oraculo_escalar', 'oraculo_escalar_todas', 'oraculo_sistema',
    'mapa_metodos', 'muestrear', 'evaluar_tema',
    'calificar', 'consejos', 'preguntas_criterio', 'enviar_resultado',
]
