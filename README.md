# U2_T4 · Proyecto: casos de estudio con raíces de ecuaciones + Monte Carlo

Cada equipo elige **un caso de estudio de ingeniería mecatrónica** planteado como una
**ecuación** (o un **sistema**) de raíces, y lo analiza con una **simulación de Monte Carlo**
para decidir, con evidencia, **qué método numérico conviene** en un sistema real donde nada es
exacto.

**Al terminar entregarán:**

1. Los **cuadernos de Colab** (`U2_T4_1_Equipo` y `U2_T4_2_Caso`).
2. Un **informe** con sus **gráficas interactivas (plotly)** y conclusiones.
3. Una **exposición de 5 a 10 minutos**.

**La pregunta que debe responder su exposición:**

> *"Si estuvieran diseñando el firmware del controlador de este sistema mecatrónico en tiempo
> real, ¿qué método programarían y por qué?"*

---

## Qué cambió en esta entrega (formato 2026)

Esta entrega adopta el **formato más reciente** (heredero de `U2_T3B`) y simplifica la
calificación:

* **Los métodos ya están implementados** y viven **dentro del motor** (`profe/core/metodos.py`),
  así que quedan **ocultos**: el equipo no los programa. La tarea es **teórica**.
* **La selección es con casillas**: **marcas** qué métodos comparar (una casilla por método,
  agrupadas por familia), sin `Ctrl` ni atajos.
* **Las gráficas son interactivas** (plotly): se pueden **seleccionar puntos** (caja y lazo),
  hacer zoom, ver valores al pasar el cursor y **descargar** la imagen.
* **Lo único que se autocalifica** es que el equipo haya **seleccionado al menos los métodos
  correctos** de su caso (y al menos un **contraejemplo**). **Todo lo demás** —interpretación de
  las gráficas, informe y exposición— se revisa **a mano**.

---

## Estructura de la carpeta (formato `U2_T3B`)

```
U2_T4_Casos_de_estudio/
├── config/
│   ├── config.yaml          pesos, tolerancias, webhook y regla de selección
│   └── preguntas.yaml       preguntas conceptuales de criterio
├── lib/
│   ├── matlab_like.py       preludio estilo MATLAB
│   ├── robomat.py           atajos de robótica (matrices, sympy)
│   └── (sin métodos: ahora viven ocultos en el motor)
├── profe/
│   ├── config.py            lectura de config/ (embebida en el bundle)
│   ├── core/                catálogo, modelos, oráculo, métodos, Monte Carlo, evaluador
│   └── ui/cuaderno.py       la API pública del motor (`__all__`)
├── tools/
│   ├── build.py             empaqueta grader_local.py + grader_ofuscado.txt
│   ├── visualizar.py        gráficas interactivas (plotly) + tabla de resultados
│   └── exportar_notebooklm.py   exporta todo a .txt
├── probador.py              inspecciona un caso (uso del profesor)
├── grader_local.py          bundle legible (generado por build.py)
├── grader_ofuscado.txt      bundle que usa el alumno en Colab
├── U2_T4_1_Equipo.ipynb     cuaderno 1: jefe, tema e integrantes (una sola vez)
└── U2_T4_2_Caso.ipynb       cuaderno 2: el ejercicio (Monte Carlo y gráficas)
```

> El alumno recibe **solo** los dos cuadernos y `grader_ofuscado.txt` (además de `lib/` y
> `tools/visualizar.py`, que los cuadernos necesitan). `profe/`, `tools/build.py` y
> `grader_local.py` son material del profesor.

## Dos cuadernos, no uno

El trabajo está partido en dos a propósito:

| Cuaderno | Quién | Para qué |
|---|---|---|
| **`U2_T4_1_Equipo`** | **solo el jefe**, **una vez** | Identificarse, **reservar el tema** y **registrar integrantes** |
| **`U2_T4_2_Caso`** | **cada integrante** | El **ejercicio**: aislar la raíz, elegir métodos, Monte Carlo y gráficas |

Si la selección de tema e integrantes viviera en el mismo cuaderno del ejercicio, un
**`Ejecutar todo`** volvería a reservar y a registrar. Al separarlos, **los dos se pueden
correr de golpe**:

* En el cuaderno 1, ninguna celda reserva ni registra por sí sola: el tema y los integrantes
  se eligen con **botones**, y hasta que no los pulsas no se guarda nada.
* En el cuaderno 2 no hay nada que reservar.

El cuaderno 1 guarda `equipo_u2t4.json` (equipo + correo + número de control del jefe) y el
cuaderno 2 lo **lee**, así que no hay que volver a identificarse. Si el archivo no existe, el
cuaderno 2 avisa de que hay que ejecutar primero el cuaderno 1.

---

## Cómo funciona el motor

Los **cuadernos** cargan el motor en **su propio namespace** y de ahí copian **solo** la API que el
motor declara en su `__all__` (al final de `profe/ui/cuaderno.py`). La primera celda elige de dónde
carga el motor con `MODO_MOTOR`:

| modo | qué carga | para qué |
|---|---|---|
| `modulos` | `profe/**` tal cual | depurar: F12, hover y breakpoints |
| `bundle` | `grader_local.py` (aplanado) | probar la forma exacta de Colab |
| `blob` | `grader_ofuscado.txt` | lo que recibe el alumno |

En Colab siempre se usa `blob`. Para regenerar los dos bundles:

```bash
python tools/build.py
```

---

## 1. Su equipo y su bloque de temas

El **tamaño de su equipo** determina **qué temas pueden elegir**:

| Integrantes | Bloque | Temas | Tipo de caso |
|---|---|---|---|
| 2 | **A** | T1 – T4 | Básico: una ecuación, derivada sencilla o polinomio |
| 3 | **B** | T5 – T9 | Intermedio: funciones trascendentes, dominio restringido |
| 4 | **C** | T10 – T15 | Estándar mecatrónica: RLC, sensores, actuadores |
| 5 | **D** | T16 – T17 | Avanzado: sistemas acoplados y fluidos |
| 6 | **E** | T18 – T19 | Integrador: Newton multivariable / empuje vectorizado |

Como hay **más temas que equipos**, ningún tema se repite.

---

## 2. Cómo elegir su caso (se hace una sola vez, en el cuaderno 1)

Todo esto ocurre en **`U2_T4_1_Equipo`**, y **solo el jefe de equipo** lo ejecuta:

| Paso | Celda | Qué hace |
|---|---|---|
| 1 | **Configuración general** | Monta Drive, trae el repositorio y carga el motor |
| 2 | **Identificación** | Valida el correo institucional y deduce el número de control del jefe |
| 3 | **Ver temas disponibles** | Muestra los temas **libres** de su bloque |
| 4 | **Reservar tema** | Bloquea el tema para su equipo (*botón*) |
| 5 | **Integrantes** | Un selector por integrante, con el jefe ya puesto |
| 6 | **Registrar equipo** | Guarda al equipo completo (*botón*) |

> ✅ Pueden usar **`Ejecutar todo`**: los pasos 4 y 6 solo ocurren al pulsar su botón.

> ⚠️ **Una vez reservado el tema ya no se puede cambiar.** Si se equivocaron, usen la celda
> **Eliminar equipo** (`PERMITIR_ELIMINAR = True` y que tu número de control **pertenezca** al
> equipo) y empiecen de nuevo.

---

## 3. Trabajo en equipo con Google Drive

1. El jefe **descarga el repositorio** (el cuaderno lo hace solo en la primera celda) y
   **comparte la carpeta** `CursoMN/U2_T4_Casos_de_estudio` con su equipo.
2. El jefe reserva el tema y registra al equipo en **`U2_T4_1_Equipo`**.
3. Cada integrante abre **su copia** de **`U2_T4_2_Caso`** y hace ahí el ejercicio completo
   (el cuaderno lee el equipo ya registrado). Los métodos **ya vienen implementados** y no se
   editan.

---

## 4. Los métodos (ya vienen resueltos)

**Los métodos ya están implementados y ocultos** dentro del motor
(`profe/core/metodos.py`, que viaja en el bundle). El equipo **no programa nada**: esta tarea
es **teórica**. Lo único que hace es:

1. **Marcar las casillas** de qué métodos comparar (eso es lo que se autocalifica).
2. Ejecutar la simulación de Monte Carlo.
3. **Interpretar** las gráficas interactivas de `tools/visualizar.py`.

Los métodos disponibles para las casillas son: **Bisección, Falsa posición, Punto fijo
modificado, Punto fijo, Newton-Raphson, NR modificado, Secante, Secante modificado, Brent,
Müller, Bairstow** y, en los casos de **sistema**, **Newton-Raphson multivariable** y
**Punto fijo modificado**.

> 🧪 El banco de pruebas del motor se corre con `python -m profe.core.metodos` (material del
> profesor, con $x^2-2$).

---

## 5. Familias de métodos

| Familia | Métodos |
|---|---|
| **Cerrado** — converge siempre, *si* hay cambio de signo | Bisección, Falsa posición, Punto fijo modificado |
| **Abierto** — rápido, pero puede divergir | Punto fijo, Newton-Raphson, NR modificado, Secante, Secante modificado |
| **Híbrido** | Brent |
| **Polinomios** | Müller, Bairstow |

> **Müller y Bairstow** solo se exigen en los **temas polinómicos** (T4). En los demás son
> opcionales.

---

## 6. La simulación de Monte Carlo y sus gráficas

La simulación somete los algoritmos a la **incertidumbre real** del sistema (tolerancias de
componentes, ruido de sensores, variación de fabricación y errores al *aislar* la raíz):

* Se perturban los parámetros del caso y se generan **1000 escenarios**.
* Todos los métodos se prueban sobre **exactamente los mismos** 1000 escenarios (comparación
  justa).
* La **raíz de referencia** de cada escenario se calcula aparte con alta precisión: es el
  **juez**.

**Qué se mide, por método:** `% éxito`, `% divergencia`, `n_iter` (velocidad) y `err_ref`
(distancia a la raíz verdadera).

**Gráficas que se generan (interactivas, plotly):**

1. **Histograma de iteraciones** por método.
2. **Tasa de divergencia** por método.
3. ⭐ **Box plot** de iteraciones (mediana, dispersión y valores atípicos).
4. **Distribución de la respuesta física** ante la incertidumbre.

Todas las gráficas permiten **seleccionar puntos** (herramienta de caja y de lazo), hacer
zoom con la rueda, ver valores al pasar el cursor y **descargar** la imagen (icono de cámara o
`visualizar.guardar_html`). Las genera `tools/visualizar.py`.

> ⚙️ **Rendimiento.** El **oráculo** (calcular la raíz de referencia muestra por muestra) se
> lleva ~84 % del tiempo; los métodos son ~1 %. Por eso el único ajuste que se nota es
> `monte_carlo.n_scan_oraculo` en `config/config.yaml` (500 puntos por defecto): da la **misma**
> raíz que 2000 (coincide a 1e-14) pero **4× más rápido**. La simulación completa de N=1000 baja
> de ~4.6 s a ~1.8 s. Si necesitas más margen, súbelo; si el equipo tiene prisa, bájalo.

---

## 7. Evaluación

| Criterio | Peso | ¿Autocalificado? |
|---|---|---|
| Selección de los métodos correctos del caso | **sí (binario)** | ✅ automático |
| Informe (gráficas + interpretación) | revisión manual | ✋ a mano |
| Exposición (claridad y defensa técnica) | revisión manual | ✋ a mano |

La **autocalificación** verifica, para el caso del equipo:

1. que **seleccionó todos** los métodos **sugeridos** de su caso, y
2. que incluyó al menos **un contraejemplo** (un método que en ese caso no funciona bien y que
   sirve para contrastar). En los casos de **sistema** (T14, T15, T19) esto **no** se exige: solo
   hay dos métodos disponibles y ambos son sugeridos.

La regla exacta vive en `config/config.yaml` (sección `seleccion`).

---

## 8. Catálogo de casos

Cada caso indica: **incógnita · ecuación · parámetros con incertidumbre · métodos sugeridos ·
desafío principal · qué deben ver en el gráfico de cajas.**

### Bloque A — Básicos (equipos de 2)

#### T1 · Fuerza electrostática en sensor anular

- **Incógnita:** $x$ (distancia) tal que $F=1$ N.
- **Ecuación:** $F(x)=\dfrac{1}{4\pi\varepsilon_0}\dfrac{qQx}{(x^2+a^2)^{3/2}}=1$.
- **Incertidumbre:** $q$, $Q$, $a$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Newton-Raphson · Secante.
- **Desafío:** $F'(x)=0$ en el máximo de la fuerza: **Newton-Raphson puede divergir** con un mal
  $x_0$; además hay **dos ramas** de solución.
- **En el box plot:** bisección estable frente a Newton-Raphson, más rápido pero con valores
  atípicos.

#### T2 · Resorte no lineal en suspensión de robot móvil

- **Incógnita:** deflexión $d\ge 0$.
- **Ecuación:** $\tfrac12 k_1 d^2+\tfrac25 k_2 d^{5/2}-mgd-mgh=0$.
- **Incertidumbre:** $k_1$, $k_2$, $m$, $h$ con $\sigma=3\%$.
- **Métodos sugeridos:** Punto fijo · Secante · Brent.
- **Desafío:** exponente fraccionario $d^{5/2}$: dominio $d\ge0$; el punto fijo puede divergir.
- **En el box plot:** estabilidad de Brent frente a la dispersión del punto fijo.

#### T3 · Ángulo crítico de vuelco de robot móvil

- **Incógnita:** $\theta$ con $N_t(\theta)=0$.
- **Ecuación:** $N_t = mg\cos\theta - ma\,\mathrm{sen}\,\theta - mg\dfrac{h}{L}\mathrm{sen}\,\theta = 0$.
- **Incertidumbre:** $m$, $a$, $h$, $L$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Secante modificado · Brent.
- **Desafío:** trigonométrica; filtrar la raíz física en $[0,\pi/2]$.
- **En el box plot:** Brent reduce la mediana de iteraciones sin perder robustez.

#### T4 · Calibración de sensor de temperatura (polinomio de 4.º grado)

- **Incógnita:** $T$ tal que $c_p(T)=1.2$.
- **Ecuación:** $0.99403+1.671\!\times\!10^{-4}T+9.7215\!\times\!10^{-8}T^2-9.5838\!\times\!10^{-11}T^3+1.9520\!\times\!10^{-14}T^4=1.2$.
- **Incertidumbre:** coeficientes y objetivo con $\sigma=1\%$.
- **Métodos sugeridos:** **Bairstow · Müller** · Newton-Raphson.
- **Desafío:** varias raíces reales; elegir la físicamente válida y comparar métodos de
  polinomios.
- **En el box plot:** Müller y Bairstow frente a Newton-Raphson (velocidad y fallos).

> 🔺 **Este es un tema polinómico:** se exige **Müller o Bairstow** entre sus métodos.

### Bloque B — Intermedios (equipos de 3)

#### T5 · Punto de operación con diodo Zener

- **Incógnita:** $V_D$.
- **Ecuación:** $I_S\!\left(e^{V_D/nV_T}-1\right)=\dfrac{V_{CC}-V_D}{R_L}$.
- **Incertidumbre:** $I_S$, $n$, $V_T$, $V_{CC}$, $R_L$ con $\sigma=5\%$.
- **Métodos sugeridos:** Newton-Raphson · Punto fijo · Bisección.
- **Desafío:** la exponencial explota; el punto fijo converge lento y NR es sensible al arranque.
- **En el box plot:** NR con pocas iteraciones frente al punto fijo con muchas, y el % de
  divergencia de NR.

#### T6 · Tensión en cable de catenaria

- **Incógnita:** $T_A$.
- **Ecuación:** $y=\dfrac{T_A}{w}\cosh\!\left(\dfrac{w}{T_A}x\right)+y_0-\dfrac{T_A}{w}$.
- **Incertidumbre:** $w$, $x$, $y$, $y_0$ con $\sigma=2\%$.
- **Métodos sugeridos:** Punto fijo · Secante modificado · Brent.
- **Desafío:** el $\cosh$ desborda si $T_A$ es pequeño; acotar bien el intervalo.
- **En el box plot:** mediana de iteraciones y fallos por desbordamiento.

#### T7 · Tirante en canal abierto (Manning)

- **Incógnita:** $H$.
- **Ecuación:** $Q=\dfrac{\sqrt{S}(BH)^{5/3}}{n(B+2H)^{2/3}}$.
- **Incertidumbre:** $S$, $Q$, $n$, $B$ con $\sigma=3\%$.
- **Métodos sugeridos:** Punto fijo modificado · Bisección · Secante.
- **Desafío:** la forma del despeje cambia la convergencia (unos divergen).
- **En el box plot:** el mismo método con dos despejes distintos, uno estable y otro no.

#### T8 · Tiro parabólico con alturas desiguales

- **Incógnita:** $\theta_0$.
- **Ecuación:** $y=(\tan\theta_0)x-\dfrac{g}{2v_0^2\cos^2\theta_0}x^2+y_0$.
- **Incertidumbre:** $x$, $v_0$, $y$, $y_0$ con $\sigma=2\%$.
- **Métodos sugeridos:** Secante modificado · Bisección · Brent.
- **Desafío:** con $\sec^2\theta_0=1+\tan^2\theta_0$ queda un polinomio en $\tan\theta_0$ con
  dos ángulos posibles.
- **En el box plot:** iteraciones y dispersión de cada método.

#### T9 · Transitorio RLC de servomotor

- **Incógnita:** $R$ para que $q/q_0=1\%$ en $t=0.05$ s.
- **Ecuación:** $e^{-Rt/2L}\cos\!\Big(\sqrt{\tfrac{1}{LC}-(\tfrac{R}{2L})^2}\,t\Big)-\tfrac{q}{q_0}=0$.
- **Incertidumbre:** $L$, $C$, $t$, $q/q_0$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Newton-Raphson · Secante.
- **Desafío:** oscilatoria (varias raíces); acotar $R$ para aislar la correcta.
- **En el box plot:** bisección estable frente a NR con valores atípicos.

### Bloque C — Estándar mecatrónica (equipos de 4)

#### T10 · Impedancia / resonancia en sensor piezoeléctrico

- **Incógnita:** $\omega$ tal que $Z=75\ \Omega$.
- **Ecuación:** $\dfrac{1}{Z}=\sqrt{\dfrac{1}{R^2}+\left(\omega C-\dfrac{1}{\omega L}\right)^2}$.
- **Incertidumbre:** $R$, $C$, $L$, $Z$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Falsa posición · Brent.
- **Desafío:** asíntota cuando $\omega\to0$; la falsa posición se estanca de un lado.
- **En el box plot:** la falsa posición estancada frente a Brent.

#### T11 · Volumen molar (Van der Waals)

- **Incógnita:** $v$.
- **Ecuación:** $\left(p+\dfrac{a}{v^2}\right)(v-b)=RT$.
- **Incertidumbre:** $p$, $T$, $a$, $b$ con $\sigma=2\%$.
- **Métodos sugeridos:** Newton-Raphson (arrancando con $v_0=RT/p$) · Secante · Brent.
- **Desafío:** comparar con el gas ideal y analizar la sensibilidad a la presión.
- **En el box plot:** rapidez de NR desde el gas ideal y su dispersión al variar $p$.

#### T12 · Razón de recirculación en reactor autocatalítico

- **Incógnita:** $R$ con $X_{Af}=0.9$.
- **Ecuación:** $\ln\dfrac{1+R(1-X_{Af})}{R(1-X_{Af})}=\dfrac{R+1}{R\,[1+R(1-X_{Af})]}$.
- **Incertidumbre:** $X_{Af}$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Punto fijo · Secante.
- **Desafío:** discontinuidad del logaritmo cerca de $R\to0$.
- **En el box plot:** cómo se disparan las iteraciones al acercarse al polo.

#### T13 · Colebrook + caída de presión (actuador neumático)

- **Incógnita:** $f$ (y luego $\Delta p$).
- **Ecuaciones:** $\dfrac{1}{\sqrt f}=-2\log_{10}\!\left(\dfrac{\epsilon}{3.7D}+\dfrac{2.51}{Re\sqrt f}\right)$, con $Re=\dfrac{\rho VD}{\mu}$.
- **Incertidumbre:** $\epsilon$, $D$, $V$, $\rho$, $\mu$ con $\sigma=2\%$.
- **Métodos sugeridos:** Punto fijo · Newton-Raphson · Brent.
- **Desafío:** NR diverge si $x_0>0.066$; usar **Swamee-Jain** como valor inicial.
- **En el box plot:** el punto fijo estable y rápido frente a NR con fallos.

#### T14 · Cinemática inversa 2-DOF (Jacobiano)

- **Incógnitas:** $(\theta_1,\theta_2)$.
- **Sistema:** $L_1\cos\theta_1+L_2\cos(\theta_1+\theta_2)=x$ y $L_1\mathrm{sen}\,\theta_1+L_2\mathrm{sen}(\theta_1+\theta_2)=y$.
- **Incertidumbre:** $L_1$, $L_2$, $x$, $y$ con $\sigma=1\%$.
- **Métodos sugeridos:** **Newton-Raphson multivariable** (Jacobiano) · Punto fijo modificado.
- **Desafío:** el Jacobiano se vuelve singular en la frontera del espacio de trabajo.
- **En el box plot:** iteraciones del sistema 2×2 y % de divergencia con el Jacobiano casi
  singular.

#### T15 · Multilateración con 3 balizas (Jacobiano)

- **Incógnitas:** $(x,y)$.
- **Sistema:** $(x-x_i)^2+(y-y_i)^2=d_i^2$ para $i=1,2,3$.
- **Incertidumbre:** $d_i$ con $\sigma=1\%$ (ruido de medición).
- **Métodos sugeridos:** Newton-Raphson multivariable (Jacobiano).
- **Desafío:** estimación inicial crítica.
- **En el box plot:** distribución de iteraciones y de la posición estimada.

### Bloque D — Avanzados (equipos de 5)

#### T16 · Velocidad terminal con $C_D$ no lineal

- **Incógnita:** $v$.
- **Ecuaciones:** $v=\sqrt{\dfrac{4g(\rho_s-\rho)d}{3C_D\rho}}$, $C_D=\dfrac{24}{Re}+\dfrac{3}{\sqrt{Re}}+0.34$, $Re=\dfrac{\rho dv}{\mu}$.
- **Incertidumbre:** $d$, $\rho_s$, $\rho$, $\mu$ con $\sigma=3\%$.
- **Métodos sugeridos:** Secante · Secante modificado · Brent.
- **Desafío:** verificar el régimen resultante ($Re>0.1$).
- **En el box plot:** comparación entre métodos y el régimen que resulta.

#### T17 · Péndulo amortiguado forzado (amplitud / resonancia)

- **Incógnita:** $\omega$.
- **Ecuación:** $(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2=(F_0/(mA))^2$.
- **Incertidumbre:** $\omega_n$, $F_0$, $m$, $\zeta$ con $\sigma=3\%$.
- **Métodos sugeridos:** Newton-Raphson · Secante modificado · Brent.
- **Desafío:** seleccionar las raíces físicas ($\omega>0$).
- **En el box plot:** iteraciones y dispersión de la frecuencia.

### Bloque E — Integradores (equipos de 6)

#### T18 · Empuje vectorizado (gimbal) — balance de momentos

- **Incógnita:** $\theta$ tal que $M(\theta)=0$.
- **Ecuación:** $(2T_b a+T_o b)\cos\theta-W_S(c\,\mathrm{sen}\,\theta+d\cos\theta)=0$.
- **Incertidumbre:** empujes $\pm3\%$; peso $W_S$ entre $195{,}000$ y $230{,}000$ lb.
- **Métodos sugeridos:** Newton-Raphson · Brent · Secante.
- **Desafío:** varias raíces; graficar $M(\theta)$ en $[-\pi,\pi]$ y analizar la sensibilidad al
  peso.
- **En el box plot:** distribución de $\theta$ conforme cambia el peso.

#### T19 · Red de tuberías no lineal (2–3 nodos)

- **Incógnitas:** caudales $(Q_1,Q_2)$.
- **Sistema:** $\sum Q_i = 0$ en cada nodo, y $\Delta p = K Q^n$ por tramo.
- **Incertidumbre:** $K_i$ y $n$ con $\sigma=3\%$.
- **Métodos sugeridos:** Newton-Raphson multivariable (Jacobiano) · Punto fijo modificado.
- **Desafío:** acoplamiento entre nodos y buen punto inicial.
- **En el box plot:** iteraciones del sistema y dispersión de los caudales.

---

## 9. Herramientas (uso del profesor)

```bash
python tools/build.py                     # regenera grader_local.py + grader_ofuscado.txt
python probador.py                        # lista los temas T1–T19
python probador.py T4                     # detalle de un caso + raíz de referencia
python tools/exportar_notebooklm.py       # toda la tarea a .txt
```

Orden recomendado antes de publicar:

1. `probador.py` para revisar cada caso y su raíz de referencia.
2. `tools/build.py` → regenerar los dos bundles.
3. Simular los cuadernos en local (modo `modulos`, `bundle` y `blob`).
4. Configurar el Apps Script de U2_T4 y pegar `webhook_token` y `apps_script_url` en
   `config/config.yaml`.

---

## 10. Preguntas frecuentes

**¿Puedo cambiar de tema después de reservarlo?**
No. Usen la celda **Eliminar equipo** (con `PERMITIR_ELIMINAR = True`) y empiecen de nuevo.

**¿Tengo que programar los métodos?**
No. Ya están implementados (y **ocultos**) dentro del motor. Solo **marcas las casillas** de
qué métodos comparar y **interpretas** las gráficas.

**¿Tengo que recalcular el intervalo en cada escenario?**
No. Las perturbaciones son pequeñas; el intervalo que aíslen una vez sirve para toda la
simulación.

**Mi método falla en algunas muestras, ¿está mal?**
No necesariamente. Los métodos de intervalo no arrancan sin cambio de signo y los abiertos
pueden divergir con un mal arranque. Eso es lo que la simulación mide: repórtenlo con datos.

**¿Cómo sé qué método conviene para el firmware?**
Compárenlos con **datos propios**: velocidad (mediana de iteraciones), robustez (% de
divergencia) y costo (¿necesita derivada? ¿necesita intervalo?). Esa comparación es el corazón
de su reporte y exposición.
