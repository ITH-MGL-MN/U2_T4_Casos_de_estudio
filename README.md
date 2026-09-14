# U2_T4 — Casos de estudio: raíces de ecuaciones + Monte Carlo (Mecatrónica)

> **Estado del documento:** borrador para revisión del profesor. Una vez validado, este mismo archivo se
> convierte en el **catálogo público** que verán los alumnos para elegir su caso.

---

## 1. Objetivo

Que cada equipo resuelva un **caso de estudio de ingeniería mecatrónica** planteado como una **ecuación (o sistema) de raíces**, y que lo analice con una **simulación de Monte Carlo** para decidir, con evidencia, **qué método numérico conviene** en un sistema real con incertidumbre.

**Producto final por equipo**
1. **Notebook de Colab** (auto-calificado + simulación Monte Carlo).
2. **Informe** con las gráficas (histogramas, % de divergencia, **box plots** comparativos y distribución de la respuesta física).
3. **Exposición de 5–10 minutos**: caso, método elegido y justificación de ingeniería.

**Pregunta que debe responder la exposición:**
> *"Si estuvieran diseñando el firmware del controlador de este sistema mecatrónico en tiempo real, ¿qué método programarían y por qué?"*

---

## 2. Logística (40 alumnos)

Son **40 alumnos**. El tamaño de los equipos **no está garantizado**, así que el catálogo tiene **más temas que equipos**:

| Tamaño de equipo | N.º sugerido de equipos | Alumnos | Bloque de dificultad |
|---|---|---|---|
| 2 | 1–2 | 2–4 | Básico (1 ecuación, derivada sencilla o polinomio) |
| 3 | 1–2 | 3–6 | Intermedio-bajo (trascendentes, dominio restringido) |
| 4 | 6 (núcleo) | 24 | Estándar mecatrónica (RLC, sensores, actuadores) |
| 5 | 1 | 5 | Avanzado (sistemas acoplados, fluidos) |
| 6 | 1 | 6 | Integrador (Newton multivariable / empuje vectorizado) |

**Regla de asignación:** cada equipo recibe el tema que **elija** (ver §5) del bloque correspondiente a su tamaño. Los temas sobrantes quedan como **reserva**.

---

## 3. Encaje con el programa

- **U2_T2** — Métodos **abiertos**: Punto Fijo, Newton-Raphson, NR Modificado, Secante, Secante Modificado.
- **U2_T3** — **Casos especiales / polinomios**: Brent, Müller, Bairstow, Punto Fijo Modificado.
- **U2_T4 (esta tarea)** — Aplicación integradora **con incertidumbre (Monte Carlo)**.

Por eso la tarea se entrega **después** de ver los métodos abiertos y especiales.

---

## 4. Familias de métodos (basado en la Tabla PT2.3)

| Método | Tipo | Valores iniciales | Convergencia | Estabilidad | Programación | Comentarios |
|---|---|---|---|---|---|---|
| Directo | Analítico | — | — | — | — | A veces no existe solución |
| Gráfico | Visual | — | — | — | — | Impreciso |
| Bisección | Cerrado | 2 | Lenta | Siempre | Fácil | |
| Falsa posición | Cerrado | 2 | Lenta/media | Siempre | Fácil | |
| PF modificada | Cerrado | 2 | Media | Siempre | Fácil | |
| Punto fijo | Abierto | 1 | Lenta | Posiblemente divergente | Fácil | |
| Newton-Raphson | Abierto | 1 | Rápida | Posiblemente divergente | Fácil | Necesita $f'$ |
| NR modificado | Abierto | 1 | Rápida (múltiple), media (única) | Posiblemente divergente | Fácil | Necesita $f'$ y $f''$ |
| Secante | Abierto | 2 | Media/rápida | Posiblemente divergente | Fácil | Condiciones iniciales no tienen que abarcar la raíz |
| Secante modificado | Abierto | 1 | Media/rápida | Posiblemente divergente | Fácil | Robusto |
| Brent | Híbrido | 1 o 2 | Media | Siempre (2 condiciones) | Moderada | |
| Müller | Polinomios | 2 | Media/rápida | Posiblemente divergente | Moderada | |
| Bairstow | Polinomios | 2 | Rápida | Posiblemente divergente | Moderada | |

**Regla del proyecto:** cada equipo compara **3–4 métodos de familias distintas** (ideal: uno *cerrado garantizado* + uno *abierto rápido* + uno *híbrido o especial*).

> **Alcance de Müller y Bairstow (decisión tomada):** los métodos **especializados en polinomios se exigen únicamente en los temas polinómicos** (T4 y cualquier otro que se plantee como polinomio). El resto de los equipos **no** está obligado a usarlos; si los incluyen, cuentan como *método extra* opcional.

---

## 5. Selección del tema y registro de equipo (SIN semilla por NC)

Esta tarea **no** usa semilla por número de control. Se trabaja **por equipo**, y el flujo lo controla el **jefe de equipo**.

### 5.1 Quién es el jefe de equipo

El **jefe de equipo** es el alumno que:
- **Descarga el repositorio** (el notebook baja `CursoMN` de GitHub al inicio) y **comparte la carpeta de Drive** con sus compañeros.
- Es el **único** que ejecuta las celdas de **selección y registro** (una sola vez).
- **Inicia sesión con su cuenta de Google** en Colab, de modo que el notebook obtiene su **correo** y lo **verifica contra su número de control** (identidad). Una vez el equipo queda registrado, los demás integrantes pueden trabajar en sus copias sin repetir estas celdas.

### 5.2 Flujo de celdas

| # | Celda | Qué hace | Acción de Apps Script |
|---|---|---|---|
| 1 | **Iniciar sesión / identidad** | Toma el correo de la sesión de Google y el **NC del jefe**; valida que exista en la lista de alumnos. | `proyecto_equipo` |
| 2 | **Ver temas disponibles** | Consulta el servidor y **pinta un `Select`** con **solo los temas libres** (bloque = tamaño de su equipo). | `proyecto_temas` |
| 3 | **Reservar tema** | Al pulsar el botón, si el tema sigue libre lo **bloquea de forma atómica** (`LockService`). **Ya no se puede cambiar.** | `proyecto_reservar` |
| 4 | **Poner integrantes** | Muestra **tantos `Select` de NC/nombre como integrantes** tenga el tema, con **el jefe ya seleccionado por defecto**. | `proyecto_equipo` |
| 5 | **Verificar y registrar equipo** | Valida tamaño, que todos existan y que **nadie esté en otro equipo**; escribe el equipo en la hoja. | `proyecto_registrar` |
| 6 | **Eliminar equipo** (solo errores) | Requiere que una **variable de código esté en `true`** (por defecto `false`) **y** que el NC actual **pertenezca al equipo**. Libera el tema. | `proyecto_eliminar` |

**Mecánica de la celda 4 (integrantes):** el número de `Select` = `tamano` del tema (2, 3, 4, 5 o 6). Uno viene **por defecto** con el jefe (que ya inició sesión). Los demás se eligen de la lista del grupo. Si el tema ya está registrado, la celda muestra el equipo guardado y **no** deja volver a registrarlo.

**Mecánica de la celda 6 (borrado seguro):** el bloqueo evita que alguien borre equipos ajenos:
```python
PERMITIR_ELIMINAR = False   # el jefe lo cambia a True solo para corregir un error
```
El servidor valida dos cosas: `confirmar == true` **y** que el `NC_Actual` sea integrante de ese equipo.

**Después del registro:** el notebook **solo muestra la información del proyecto elegido** (de ahí que el catálogo completo viva en este README y no en el notebook, para no saturarlo).

### 5.3 Implementación en Apps Script

Archivo **`proyectos.gs`** (estructura propia, distinta a las tareas normales). Crea **solo dos hojas**, con `inicializarProyecto()`:

**`U2_T4_Casos_Equipos`** — *una fila por tema* (19 filas, pre-cargadas, **nunca crece**):

| Timestamp | Equipo | Tema | N_Integrantes | NC_Jefe | Correo | Apellido | Nombre | Estado |
|---|---|---|---|---|---|---|---|---|

- `Equipo` = **número del tema/equipo** (1…19).
- `Tema` = nombre del tema.
- `N_Integrantes` = integrantes **requeridos** por el tema (2, 3, 4, 5 o 6; pre-cargado del catálogo).
- `NC_Jefe`, `Correo`, `Apellido`, `Nombre` = datos del jefe de equipo.
- `Estado` ∈ **`disponible` | `tomado` | `completado`**.

**`U2_T4_Casos_Resultados`** — *una fila por alumno* (pre-cargadas del roster, **nunca crece**):

| Timestamp | NC | Correo | Apellido | Nombre | EsJefe | Equipo | Tema | Metodos | Calificacion |
|---|---|---|---|---|---|---|---|---|---|

- `EsJefe` = `TRUE`/`FALSE`.
- `Equipo` / `Tema` = a qué equipo pertenece (vacío = sin equipo).
- `Metodos` = **métodos que usó**, detectados por el Monte Carlo (§8.6).
- `Calificacion` = 0…100 (base + extras con tope, §8.6 y §9).

> **La pertenencia a un equipo se deriva agrupando por `Equipo` en Resultados**: no hace falta una tercera hoja. `Estado` en la hoja de equipos pasa de `disponible` → `tomado` (al reservar) → `completado` (al registrar a todos).

**Acciones** (POST al mismo `doPost`, agrupadas por prefijo `proyecto_`):

| Acción | Entrada | Salida |
|---|---|---|
| `proyecto_temas` | — | lista completa de temas con `estado`, `disponible`, `tamano`, `bloque` |
| `proyecto_reservar` | `NC_Jefe`, `correo`, `tema` | tema en `tomado` (bloqueado) + jefe dado de alta |
| `proyecto_equipo` | `NC`, `correo` | equipo del alumno (`null` si no tiene) + temas |
| `proyecto_registrar` | `NC_Jefe`, `correo`, `tema`, `integrantes[]` | tema en `completado` |
| `proyecto_eliminar` | `NC_Actual`, `tema`, `confirmar: true` | tema en `disponible` e integrantes liberados |
| `proyecto_resultado` | `NC`, `metodos[]`, `calificacion`, `alcance` | escribe `Metodos` y `Calificacion` (por alumno o a todo el equipo) |

**Utilidades del profesor** (desde el editor de Apps Script): `inicializarProyecto()` (crea/siembra las hojas), `reiniciarProyecto()` (recrea **borrando** lo capturado), `verProyectos()` (log de estados) y `liberarTemaProyecto(tema)`.

**Seguridad de la identidad:** si la hoja de alumnos trae una columna **`Correo`** (opcional), el servidor exige que el correo de la sesión de Google coincida con el del NC. Si no existe esa columna, solo se valida que el NC esté en la lista. *Recomendado:* agregar la columna `Correo` a `Resultados` para verificación estricta.

**Token:** usa `PROYECTO_TOKEN` si existe; si no, cae a `TAREA_TOKEN`/`WEBHOOK_TOKEN` (el mismo que ya está en los notebooks).

---

## 6. Flujo de trabajo con Google Drive Desktop (librerías propias)

Aprovechamos para que aprendan a trabajar como equipo con **Google Drive para escritorio**:

- El Notebook al principio ya descarga de github este repositorio en CursoMN, por lo que uno debe ser el encargado de descargarlo y compartirlo con los demás.
- Ahí guardan su **librería de métodos** `metodos_equipo.py` (bisección, newton, secante, etc.) que **ellos implementan**.
- Se hará una plantilla base de la librería con un `if __name__ == __main__` para que puedan hacer pruebas básicas en la computadora para no tener tantos problemas al cambiar entre Google Colab y Python de escritorio.


> Ventaja: los alumnos ven el ciclo real "librería propia → importar → usar", y aprenden a compartir un proyecto.

---

## 7. Estructura del notebook de Colab (ya construido)

`U2_T4_Casos_de_estudio.ipynb` — **33 celdas** (16 markdown + 17 código), generadas por `generar_notebook.py`.

| Sección | Celdas | Contenido |
|---|---|---|
| **0. Configuración** | 3–4 | Monta Drive, clona el repo, instala librerías, carga `grader` (oculto) y el estado del equipo. |
| **0. Identificación** | 5–6 | Correo institucional de la sesión + **NC del jefe** validado contra la lista. |
| **1. Elige tu caso** | 8–10 | Tabla de bloques · **Ver temas disponibles** · **Reservar tema** (bloqueo). |
| **2. Integrantes** | 11–15 | Selectores según el tamaño · **Registrar equipo** · **Eliminar equipo** (seguro). |
| **3. Tu caso** | 16–17 | Muestra **solo tu proyecto**: incógnita, ecuación en LaTeX, incertidumbres y métodos sugeridos. |
| **4. Librería del equipo** | 18–19 | Carga `lib/metodos_equipo.py` desde Drive + `recargar_libreria()`. |
| **5. Definición simbólica** | 20–21 | `sympy`: ecuación, derivada o **Jacobiano**, `lambdify`. |
| **6. Tus métodos** | 22–23 | Registro `METODOS` (adaptadores) + detección automática con `inspect`. |
| **7. Monte Carlo** | 24–25 | `evaluar_tema(...)`: $N=1000$ muestras y tabla de métricas por método. |
| **8. Gráficos** | 26–29 | Histograma + % divergencia · ⭐ **box plot** · distribución de la respuesta física. |
| **9. Conclusiones** | 30–31 | **5 preguntas**: 2 resueltas con las métricas reales (las juzga el oráculo) + 3 conceptuales con clave oculta. |
| **10. Calificación y envío** | 32–33 | `calificar` + **consejos automáticos** + `enviar_resultado` (acción `proyecto_resultado`). |

**Archivos que se publican** (el resto está en `.gitignore`):

| Archivo | Para quién |
|---|---|
| `lib/metodos_equipo.py` | **plantilla** de la librería del equipo (con `if __name__ == '__main__'`) |
| `lib/matlab_like.py`, `lib/robomat.py` | utilidades comunes |
| `grader_ofuscado.txt` | calificador ofuscado (lo carga Colab) |
| `README.md` | catálogo público |
| `U2_T4_Casos_de_estudio.ipynb` | se comparte por enlace de Colab (gitignoreado) |
| `profe/` | **no se publica** (`grader.py`, `ofuscar.py`, `generar_notebook.py` no, `verificar_temas.py`, `simular_notebook.py`) |

### 7.1 Herramientas del profesor

```powershell
# Dentro de la carpeta de la tarea, con el venv del curso:
python profe/verificar_temas.py     # valida los 19 temas (1 raíz por intervalo, f(raíz)≈0)
python generar_notebook.py          # regenera U2_T4_Casos_de_estudio.ipynb
python profe/verificar_notebook.py  # JSON válido + las 17 celdas de código compilan
python profe/simular_notebook.py    # EJECUTA las celdas analíticas con datos reales (T1, T4, T14)
python profe/ofuscar.py             # regenera grader_ofuscado.txt (hacerlo al final)
```

---

## 8. Simulación de Monte Carlo (especificación común)

**Objetivo:** someter los algoritmos a la **incertidumbre real** (tolerancia de componentes, ruido de sensores, variación de fabricación, condiciones iniciales).

### 8.1 · Definir la incertidumbre ($N = 1000$)
- Perturbar constantes físicas: $p \rightarrow p\,(1 + \sigma z)$, con $z \sim \mathcal N(0,1)$.
- O uniforme: $p \sim \mathcal U(a,b)$.
- Valor inicial aleatorio $x_0 \sim \mathcal U(a,b)$ para **forzar** convergencia/divergencia.
- **Misma semilla** para todos los métodos $\Rightarrow$ comparación justa.
  ```python
  rng = np.random.default_rng(SEMILLA_EQUIPO)
  muestras = {p: mu*(1 + sigma*rng.normal(size=N)) for p, (mu, sigma) in params.items()}
  ```

### 8.2 · Bucle de evaluación
Para cada una de las $N$ muestras, correr **cada método** y guardar:
- `exito` (¿$\varepsilon_a < 10^{-3}$ en $\le 100$ iteraciones?),
- `n_iter`,
- `raiz` (respuesta física),
- `tiempo` (opcional).

### 8.3 · Gráficos (automáticos)
1. **Histograma comparativo de iteraciones** (Bisección vs NR vs Secante vs Brent…).
2. **Tasa de divergencia (%)** por método (barras).
3. **Box plot de iteraciones por método** ⭐ — muestra mediana, dispersión y *outliers*: **se ve de inmediato por qué un método es mejor que otro** (menos iteraciones y menos dispersión).
4. **Distribución de la respuesta física** (histograma/box plot de $R$, $\theta$, $H$, $f$…) ante la incertidumbre.

### 8.4 · Análisis para la exposición
Contrastar: velocidad (medianas del box plot) vs robustez (% divergencia) vs costo por iteración (necesita $f'$, $f''$, etc.).

### 8.5 · Oráculo de raíz + consejos automáticos (decisión de diseño)

**Pregunta del profesor:** *¿el Monte Carlo puede conocer la respuesta correcta y dar consejos automáticos? ¿basta con comparar el código del alumno contra el "código real", o con exigir que cumpla la tolerancia en cierto número de iteraciones?*

**Decisión: el Monte Carlo se apoya en un ORÁCULO de raíz (verdad de referencia por muestra), y se compara el RESULTADO, nunca el código.**

Razones:

1. **Comparar código contra código no funciona.** Cada alumno escribe su método con estilo propio (distinto criterio de paro, distinto orden de operaciones). Un comparador de código daría falsos negativos. Lo que **sí** es objetivo es comparar **la raíz que devuelve** contra **la raíz verdadera** de esa muestra.
2. **Exigir solo la tolerancia tampoco basta.** Un criterio de paro por **paso** ($|\Delta x|<\text{tol}$) puede "converger" a un punto que **no es raíz** (p. ej. cerca de una asíntota o en una meseta). Por eso se exigen **dos condiciones juntas**: residual pequeño **y** coincidencia con el oráculo.

**Cómo se construye el oráculo (oculto, en `profe/grader.py`):**

- Para cada muestra del Monte Carlo se calcula la raíz verdadera $x^{*}$ con un método de confianza a **tolerancia muy fina** ($10^{-12}$) y muchas iteraciones: **Brent** (1 ecuación) o `scipy.optimize.root` / `sympy.nsolve` (sistemas, partiendo del Jacobiano).
- Como la raíz cambia con la perturbación, el oráculo se recalcula **por muestra** (no una sola vez).
- El oráculo es el **juez**: es lo único que permite decir *"tu raíz está equivocada"* y no solo *"tu método no convergió"*.

**Métricas por método y por muestra** (con la **misma semilla** para todos):

| Métrica | Definición | Para qué sirve |
|---|---|---|
| `exito` | residual $\lvert f(x)\rvert<\tau_f$ **y** error relativo vs $x^{*}$ $<\tau_x$ | correctitud real, no solo "se detuvo" |
| `n_iter` | iteraciones usadas | box plot de velocidad |
| `diverge` | no llegó a `exito` en $\le 100$ iter. | % de divergencia |
| `err_ref` | $\lvert x-x^{*}\rvert/\lvert x^{*}\rvert$ | exactitud |
| `rama` | si cayó en la raíz **física** esperada | detecta raíz "correcta pero no la útil" |

**Consejos automáticos (reglas if/else sobre las métricas, no juicios subjetivos):** el notebook imprime retroalimentación textual, por ejemplo:

- **"Tu Newton-Raphson divergió en el 12% de las muestras"** → *"Tu $x_0$ es muy agresivo; inicia en el rango que da el análisis gráfico o usa Brent."*
- **"Tu bisección converge, pero a una raíz distinta de la física"** → *"Aísla el intervalo: hay más de una raíz; verifica el cambio de signo correcto."*
- **"Tu falsa posición se estancó (muchas iteraciones, error apenas bajando)"** → *"Es la limitación conocida de FP; usa PFM o Brent."*
- **"Tu residual cumple la tolerancia pero no coincide con el oráculo"** → *"Tu criterio de paro se detuvo en un punto que no es raíz."*
- **"Todos los métodos coinciden en $\pm$tolerancia"** → *"Bien: úsalo como evidencia de que la respuesta física es confiable."*

**Auto-calificación de las conclusiones de ingeniería:** las respuestas de criterio se califican contra el **oráculo** (qué método resulta más rápido/robusto según las métricas reales del tema del equipo), no contra un texto fijo.

**Versión ligera (sin oráculo) — solo si se quiere simplificar:** el alumno puede obtener consejos de *auto-consistencia* sin servidor, verificando que **todos** sus métodos coinciden entre sí dentro de la tolerancia. Sirve como pista, pero **no** distingue "convergió a la raíz equivocada". Por eso el oráculo es la opción elegida.

### 8.6 · Detección de métodos y calificación automática

Esto alimenta las columnas **`Metodos`** y **`Calificacion`** de la hoja `U2_T4_Casos_Resultados`.

#### a) Cómo el Monte Carlo *identifica* los métodos

**Fuente de verdad: un registro explícito** que el equipo declara en su notebook (o en su `metodos_equipo.py`):

```python
METODOS = {
    "Bisección":       biseccion,
    "Falsa posición":  falsa_posicion,
    "Newton-Raphson":  newton_raphson,
    "Brent":           brent,
    # ... los que implementaron
}
```

El Monte Carlo **itera `METODOS.items()`**, así que los **nombres** de las llaves son exactamente lo que se reporta. No hay ambigüedad.

**Apoyo automático (para avisar, no para calificar):** además se escanea el módulo con `inspect` y se reconocen nombres normalizados (`biseccion`, `falsa_posicion`, `pfm`, `punto_fijo`, `newton_raphson`, `nr_modificado`, `secante`, `secante_modificada`, `brent`, `muller`, `bairstow`). Si hay funciones de método **sin declarar** en `METODOS`, o llaves que **no corresponden** a ninguna función, se avisa:

- *"Detecté `muller` en tu código pero no está en `METODOS`; agrégalo para que cuente."*
- *"`Secante` está declarado pero no encontré la función."*

#### b) ¿Qué método *cuenta*?

Un método **cuenta** solo si el **oráculo** lo aprueba, es decir `exito ≥ 80%` de las $N$ muestras (§8.5) — no basta con que "termine".

#### c) Familias (para exigir diversidad)

| Familia | Métodos | ¿Obligatoria? |
|---|---|---|
| **Cerrado** | Bisección, Falsa posición, PFM | sí (1) |
| **Abierto** | Punto fijo, Newton-Raphson, NR modificado, Secante, Secante modificado | sí (1) |
| **Híbrido** | Brent | sí (1) |
| **Polinomios** | Müller, Bairstow | **solo en temas polinómicos (T4)** |

#### d) Fórmula de `Calificacion`

| Concepto | Puntos |
|---|---|
| **Base**: 3 métodos que cuenten, de **≥ 3 familias distintas** (1 cerrada + 1 abierta + 1 híbrida) | **80** |
| Si no cumple la base: `20 × (nº de familias distintas con al menos un método válido)` | máx 60 |
| **Extra**: **+4 por cada método válido adicional** (a partir del 4.º), **hasta 5 extras** | máx **+20** |
| **Tema polinómico (T4)** sin Müller ni Bairstow válido | base baja a **60** |
| Mínimo / máximo final | **0 / 100** |

Así: 3 métodos bien hechos = **80**; 8 métodos bien hechos = **100** (tope). **El tope es a propósito**: no conviene "programar los 13 métodos" para inflar la nota, solo demuestra dominio quien añade hasta 5 métodos **que además pasan el oráculo**.

#### e) Reporte al servidor

Al final, el notebook envía una sola petición:

```python
{"accion": "proyecto_resultado", "NC": NC, "correo": correo,
 "metodos": list(METODOS.keys()), "calificacion": CALIF, "alcance": "equipo"}
```

`alcance`: `"alumno"` escribe solo la fila del NC; `"equipo"` replica el resultado a **todos** los integrantes (lo natural en un proyecto de equipo).

---

## 9. Evaluación

| Criterio | Peso sugerido | Dónde vive |
|---|---|---|
| Notebook: métodos que **cuentan** (pasan el oráculo) + Monte Carlo correcto | 40% | columna **`Calificacion`** (§8.6d) |
| Preguntas de criterio (auto-calificadas contra el oráculo) | 20% | notebook + `Calificacion` |
| Informe (gráficas, incluida el **box plot**, y conclusiones) | 20% | revisión del profesor |
| Exposición (claridad, defensa técnica) | 20% | rúbrica manual |

**`Metodos`** deja registro de qué métodos usó cada equipo (y por tanto de la **diversidad de familias**), y **`Calificacion`** ya trae la parte automática (base + extras con tope). El resto se captura manualmente en las dos últimas filas de la rúbrica.

---

## 10. Catálogo de casos de estudio

> Cada caso indica: **incógnita · ecuación · parámetros con incertidumbre · métodos sugeridos · desafíos · qué debe evidenciar el box plot.**

### Bloque A — Básicos (equipos de 2)

**T1 · Fuerza electrostática en sensor anular**
- **Incógnita:** $x$ (distancia) tal que $F=1$ N.
- **Ecuación:** $F(x)=\frac{1}{4\pi\varepsilon_0}\frac{qQx}{(x^2+a^2)^{3/2}}=1$.
- **Incertidumbre:** $q,Q,a$ con $\sigma=2\%$.
- **Métodos:** Bisección · Newton-Raphson · Secante.
- **Desafíos:** $F'(x)=0$ en el máximo de la fuerza → NR **diverge** con mal $x_0$; hay dos ramas de solución.
- **Box plot:** iteraciones de Bisección (estable) vs NR (rápido pero con *outliers* de divergencia).

**T2 · Resorte no lineal en suspensión de robot móvil**
- **Incógnita:** deflexión $d\ge 0$.
- **Ecuación:** $\tfrac12 k_1 d^2+\tfrac25 k_2 d^{5/2}-mgd-mgh=0$.
- **Incertidumbre:** $k_1,k_2,m,h$ con $\sigma=3\%$.
- **Métodos:** Punto Fijo · Secante · Brent.
- **Desafíos:** exponente fraccionario $d^{5/2}$ → **dominio** $d\ge0$; PF puede divergir.
- **Box plot:** estabilidad de Brent vs dispersión de PF.

**T3 · Ángulo crítico de vuelco de robot móvil**
- **Incógnita:** $\theta$ con $N_t(\theta)=0$.
- **Ecuación:** $N_t = mg\cos\theta - ma\,\mathrm{sen}\,\theta - mg\frac{h}{L}\mathrm{sen}\,\theta = 0$.
- **Incertidumbre:** $m,a,h,L$ con $\sigma=2\%$.
- **Métodos:** Bisección · Secante Modificado · Brent.
- **Desafíos:** trigonométrica; filtrar la raíz **física** en $[0,\pi/2]$.
- **Box plot:** iteraciones; ver que Brent reduce la mediana sin perder robustez.

**T4 · Calibración de sensor de temperatura (polinomio de 4.º)**
- **Incógnita:** $T$ con $c_p(T)=1.2$.
- **Ecuación:** $0.99403+1.671\!\times\!10^{-4}T+9.7215\!\times\!10^{-8}T^2-9.5838\!\times\!10^{-11}T^3+1.9520\!\times\!10^{-14}T^4=1.2$.
- **Incertidumbre:** coeficientes y objetivo con $\sigma=1\%$.
- **Métodos:** **Bairstow · Müller** · Newton-Raphson.
- **Desafíos:** varias raíces reales → elegir la **físicamente válida**; comparar métodos **especializados en polinomios**.
- **Box plot:** Müller/Bairstow vs NR (velocidad y fallos por raíz compleja).

### Bloque B — Intermedios (equipos de 3)

**T5 · Punto de operación con diodo Zener**
- **Incógnita:** $V_D$. **Ecuación:** $I_S\!\left(e^{V_D/nV_T}-1\right)=\frac{V_{CC}-V_D}{R_L}$.
- **Incertidumbre:** $I_S,n,V_T,V_{CC},R_L$ con $\sigma=5\%$.
- **Métodos:** Newton-Raphson · Punto Fijo · Bisección.
- **Desafíos:** exponencial explota; PF converge lento; NR sensible a $V_0$.
- **Box plot:** NR pocas iteraciones vs PF muchas; % de divergencia de NR.

**T6 · Tensión en cable de catenaria**
- **Incógnita:** $T_A$. **Ecuación:** $y=\frac{T_A}{w}\cosh\!\big(\frac{w}{T_A}x\big)+y_0-\frac{T_A}{w}$.
- **Incertidumbre:** $w,x,y,y_0$ con $\sigma=2\%$.
- **Métodos:** Punto Fijo · Secante Modificado · Brent.
- **Desafíos:** $\cosh$ → **overflow** si $T_A$ pequeño; acotar bien.
- **Box plot:** mediana de iteraciones y detección de fallos por overflow.

**T7 · Tirante en canal abierto (Manning)**
- **Incógnita:** $H$. **Ecuación:** $Q=\frac{\sqrt{S}(BH)^{5/3}}{n(B+2H)^{2/3}}$.
- **Incertidumbre:** $S,Q,n,B$ con $\sigma=3\%$.
- **Métodos:** Punto Fijo Modificado (comparar **despejes**) · Bisección · Secante.
- **Desafíos:** la **forma del despeje** cambia la convergencia (unos divergen).
- **Box plot:** comparar PFM con dos despejes distintos (uno estable, uno no).

**T8 · Tiro parabólico con alturas desiguales**
- **Incógnita:** $\theta_0$. **Ecuación:** $y=(\tan\theta_0)x-\frac{g}{2v_0^2\cos^2\theta_0}x^2+y_0$.
- **Incertidumbre:** $x,v_0,y,y_0$ con $\sigma=2\%$.
- **Métodos:** Secante Modificado · Bisección · Brent.
- **Desafíos:** identidad $\sec^2\theta_0=1+\tan^2\theta_0$ → polinomio en $\tan\theta_0$; dos ángulos posibles.
- **Box plot:** iteraciones por método; elegir raíz físicamente válida.

**T9 · Transitorio RLC de servomotor**
- **Incógnita:** $R$ para $q/q_0=1\%$ en $t=0.05$ s.
- **Ecuación:** $e^{-Rt/2L}\cos\!\Big(\sqrt{\tfrac{1}{LC}-(\tfrac{R}{2L})^2}\,t\Big)-\tfrac{q}{q_0}=0$.
- **Incertidumbre:** $L,C,t,q/q_0$ con $\sigma=2\%$.
- **Métodos:** Bisección · Newton-Raphson · Secante.
- **Desafíos:** **oscilatoria** → múltiples raíces; acotar $R$ para aislar la correcta.
- **Box plot:** Bisección estable vs NR con *outliers*.

### Bloque C — Estándar Mecatrónica (equipos de 4)

**T10 · Impedancia/resonancia en sensor piezoeléctrico**
- **Incógnita:** $\omega$ con $Z=75\ \Omega$. **Ecuación:** $\frac1Z=\sqrt{\frac{1}{R^2}+(\omega C-\frac{1}{\omega L})^2}$.
- **Incertidumbre:** $R,C,L,Z$ con $\sigma=2\%$.
- **Métodos:** Bisección · Falsa Posición · Brent.
- **Desafíos:** asíntota $\omega\to0$; **falsa posición se estanca** de un lado.
- **Box plot:** comparar FP (estancada) vs Brent.

**T11 · Volumen molar (Van der Waals)**
- **Incógnita:** $v$. **Ecuación:** $(p+\frac{a}{v^2})(v-b)=RT$.
- **Incertidumbre:** $p,T,a,b$ con $\sigma=2\%$.
- **Métodos:** Newton-Raphson ($v_0=RT/p$ del gas ideal) · Secante · Brent.
- **Desafíos:** comparar con gas ideal; sensibilidad a $p$.
- **Box plot:** NR muy rápido si $v_0$ ideal; dispersión al variar $p$.

**T12 · Razón de recirculación en reactor autocatalítico**
- **Incógnita:** $R$ con $X_{Af}=0.9$.
- **Ecuación:** $\ln\frac{1+R(1-X_{Af})}{R(1-X_{Af})}=\frac{R+1}{R[1+R(1-X_{Af})]}$.
- **Incertidumbre:** $X_{Af}$ con $\sigma=2\%$.
- **Métodos:** Bisección · Punto Fijo · Secante.
- **Desafíos:** discontinuidad log cerca de $R\to0$.
- **Box plot:** sensibilidad de iteraciones al acercarse al polo.

**T13 · Colebrook + caída de presión (actuador neumático)**
- **Incógnita:** $f$ (y luego $\Delta p$). **Ecuaciones:** $\frac{1}{\sqrt f}=-2\log_{10}\!\big(\frac{\epsilon}{3.7D}+\frac{2.51}{Re\sqrt f}\big)$, $Re=\frac{\rho VD}{\mu}$.
- **Incertidumbre:** $\epsilon,D,V,\rho,\mu$ con $\sigma=2\%$.
- **Métodos:** Punto Fijo (rápido aquí) · Newton-Raphson · Brent.
- **Desafíos:** NR **diverge** si $x_0>0.066$; usar **Swamee-Jain** como $x_0$.
- **Box plot:** PF estable y rápido vs NR con fallos.

**T14 · Cinemática inversa 2-DOF (Jacobiano)**
- **Incógnitas:** $(\theta_1,\theta_2)$.
- **Sistema:** $L_1\cos\theta_1+L_2\cos(\theta_1+\theta_2)=x$; $L_1\mathrm{sen}\,\theta_1+L_2\mathrm{sen}(\theta_1+\theta_2)=y$.
- **Incertidumbre:** $L_1,L_2$ con $\sigma=1\%$; $(x,y)$ objetivo con $\sigma=1\%$; $(\theta_1^0,\theta_2^0)$ aleatorios.
- **Métodos:** **Newton-Raphson multivariable** (Jacobiano con `sympy`) · Punto Fijo Modificado.
- **Desafíos:** **Jacobiano singular** en la frontera del espacio de trabajo.
- **Box plot:** iteraciones del sistema 2×2; % de divergencia por Jacobiano casi singular.

**T15 · Multilateración con 3 balizas (Jacobiano)**
- **Incógnitas:** $(x,y)$. **Sistema:** $(x-x_i)^2+(y-y_i)^2=d_i^2$, $i=1,2,3$.
- **Incertidumbre:** $d_i$ con $\sigma=1\%$ (ruido de medición).
- **Métodos:** Newton-Raphson multivariable (Jacobiano) · (opcional) mínimos cuadrados.
- **Desafíos:** sistema **sobredeterminado**; elegir buen subconjunto / estimación inicial.
- **Box plot:** distribución de iteraciones y de la posición estimada.

### Bloque D — Avanzados (equipos de 5)

**T16 · Velocidad terminal con $C_D$ no lineal**
- **Incógnita:** $v$. **Ecuaciones:** $v=\sqrt{\frac{4g(\rho_s-\rho)d}{3C_D\rho}}$, $C_D=\frac{24}{Re}+\frac{3}{\sqrt{Re}}+0.34$, $Re=\frac{\rho dv}{\mu}$.
- **Incertidumbre:** $d,\rho_s,\rho,\mu$ con $\sigma=3\%$.
- **Métodos:** Secante · Secante Modificado · Brent.
- **Desafíos:** verificar **régimen** ($Re>0.1$).
- **Box plot:** comparar métodos y régimen resultante.

**T17 · Péndulo amortiguado forzado (amplitud/resonancia)**
- **Incógnita:** $\omega$ (o $\zeta$ para amplitud máxima).
- **Ecuación:** $(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2=(F_0/(mA))^2$.
- **Incertidumbre:** $\omega_n,F_0,m,\zeta$ con $\sigma=3\%$.
- **Métodos:** Newton-Raphson · Secante Modificado · Brent.
- **Desafíos:** seleccionar raíces **físicas** ($\omega>0$).
- **Box plot:** iteraciones y dispersión de la frecuencia.

### Bloque E — Integradores (equipos de 6)

**T18 · Empuje vectorizado (gimbal) — balance de momentos**
- **Incógnita:** $\theta$ con $M(\theta)=0$ (momentos de orbitador, cohetes y tanque respecto a $G$).
- **Incertidumbre:** empujes $\pm3\%$; peso $W_S: 230{,}000 \to 195{,}000$ lb.
- **Métodos:** Newton-Raphson (5 cifras) · Brent · Secante.
- **Desafíos:** varias raíces; graficar $M(\theta)$ en $[-\pi,\pi]$; sensibilidad al peso.
- **Box plot:** evolución del ángulo $\theta$ ante la pérdida de peso (distribución).

**T19 · Red de tuberías no lineal (2–3 nodos)**
- **Incógnitas:** caudales $(Q_1,\dots,Q_n)$.
- **Sistema:** $\sum Q_i = 0$ (nodos) y $\Delta p = K Q^n$ por tramo.
- **Incertidumbre:** $K_i,n$ con $\sigma=3\%$.
- **Métodos:** Newton-Raphson multivariable (Jacobiano con `sympy`) · Punto Fijo Modificado.
- **Desafíos:** acoplamiento y buen punto inicial.
- **Box plot:** iteraciones del sistema y dispersión de caudales.

---

## 11. Pendientes / decisiones

### Resueltas
- [x] **Müller/Bairstow**: solo en los **temas polinómicos** (T4 y similares). §4.
- [x] **Mecanismo de selección por equipo** (jefe, identidad, reserva/bloqueo, integrantes, borrado seguro). §5.
- [x] **Solo dos hojas**: `U2_T4_Casos_Equipos` (una fila por tema) y `U2_T4_Casos_Resultados` (una fila por alumno). §5.3.
- [x] **Apps Script `proyectos.gs`** con las acciones `proyecto_temas`, `proyecto_reservar`, `proyecto_equipo`, `proyecto_registrar`, `proyecto_eliminar`, `proyecto_resultado`. §5.3.
- [x] **Monte Carlo con oráculo** y consejos automáticos (comparar *resultados*, no código). §8.5.
- [x] **Detección de métodos** (registro `METODOS` + escaneo con `inspect`) y **fórmula de `Calificacion`** con tope. §8.6.
- [x] **Plantilla de Colab** construida y verificada (33 celdas; las celdas analíticas se **ejecutan** en el simulacro con T1, T4 y T14). §7.
- [x] **Calificador oculto** con los 19 temas, el **oráculo** por muestra (Brent/sympy a 1e-13) y el motor de Monte Carlo. §7.1.

### Abiertas
- [ ] **Validar el catálogo** (valores nominales, incertidumbres y el desafío de **T18**, cuyos datos de empuje/peso son una **propuesta**).
- [ ] Confirmar la semántica de **`N_Integrantes`** (hoy es el **requerido** por el tema).
- [ ] Confirmar los **umbrales de `Calificacion`** (§8.6d) y de `exito` (`TAU_F`, `TAU_X`, `UMBRAL_EXITO`).
- [ ] Definir la **columna `Correo`** en la hoja de alumnos (verificación estricta de identidad).
- [ ] **Crear el repositorio en GitHub** `ITH-MGL-MN/U2_T4_Casos_de_estudio` (la URL ya está en la celda 1 del notebook).
- [ ] Pegar `proyectos.gs` en el proyecto de Apps Script existente y pegar el token en `WEBHOOK_TOKEN` del gradedor (ya comparte el de U2_T1).
- [ ] Regenerar `grader_ofuscado.txt` (`python profe/ofuscar.py`) **al final**, antes de las pruebas en Colab.
- [ ] Rúbrica final y fechas (entrega + exposiciones, 1 semana).

### Riesgo conocido (mitigado)
- Un alumno podría declarar un método cuyo cuerpo llame al oráculo. Se mitiga con: (a) el calificador va **ofuscado**; (b) `calificar` marca como **no válido** cualquier método con **mediana de iteraciones < 3** (envoltorio trivial); (c) el informe y la exposición son revisados por el profesor.
