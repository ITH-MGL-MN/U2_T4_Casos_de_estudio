# U2_T4 · Proyecto: casos de estudio con raíces de ecuaciones + Monte Carlo

## ¿De qué se trata?

Cada equipo elige **un caso de estudio de ingeniería mecatrónica** planteado como una
**ecuación** (o un **sistema** de ecuaciones) de raíces, y lo analiza con una **simulación de
Monte Carlo** para decidir, con evidencia, **qué método numérico conviene** en un sistema real
donde nada es exacto.

**Al terminar entregarán:**

1. El **notebook de Colab** (la parte de métodos se califica automáticamente).
2. Un **informe** con sus gráficas y conclusiones.
3. Una **exposición de 5 a 10 minutos**.

**La pregunta que debe responder su exposición:**

> *"Si estuvieran diseñando el firmware del controlador de este sistema mecatrónico en tiempo
> real, ¿qué método programarían y por qué?"*

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

Como hay **más temas que equipos**, ningún tema se repite: cada equipo trabaja uno distinto.

---

## 2. Cómo elegir su caso (se hace una sola vez)

Solo el **jefe de equipo** ejecuta estas celdas, y **una sola vez**:

| Paso | Celda del notebook | Qué hace |
|---|---|---|
| 1 | **Identificación** | Valida el correo institucional y el número de control del jefe |
| 2 | **Ver temas disponibles** | Muestra los temas **libres** de su bloque |
| 3 | **Reservar tema** | Bloquea el tema para su equipo |
| 4 | **Integrantes** | Un selector por integrante, con el jefe ya puesto por defecto |
| 5 | **Registrar equipo** | Guarda al equipo completo |

El **jefe de equipo** es quien **descarga el repositorio** y **comparte la carpeta de Drive**
con sus compañeros. Una vez registrado el equipo, todos pueden trabajar en sus copias sin
repetir estos pasos.

> ⚠️ **Una vez reservado el tema ya no se puede cambiar.**
>
> Si se equivocaron (de tema o de integrantes), ejecuten la celda **Eliminar equipo**:
> requiere poner `PERMITIR_ELIMINAR = True` y que tu número de control **pertenezca** al
> equipo (así nadie puede borrar el equipo de otros). Después empiezan de nuevo desde el paso 1.

---

## 3. Trabajo en equipo con Google Drive

1. El jefe **descarga el repositorio** (el notebook lo hace solo en la primera celda) y
   **comparte la carpeta** `CursoMN/U2_T4_Casos_de_estudio` con su equipo.
2. Dentro de esa carpeta está **`lib/metodos_equipo.py`**: la **librería del equipo**, donde
   ustedes implementan sus métodos.
3. Esa librería se **importa** desde el notebook, así que todo el equipo trabaja sobre el mismo
   código y todos ven los cambios.

> Así trabajan como en un proyecto real: **librería propia → importar → usar**.

---

## 4. La librería del equipo (`lib/metodos_equipo.py`)

Sus métodos deben respetar **este contrato**:

```python
# Una ecuación
g(f, p0, p1, tol, max_iter) -> (raiz, n_iter)

# Sistemas de ecuaciones
g(F, x0, _x1, tol, max_iter) -> (vector_raiz, n_iter)
```

- `f` (o `F`) es la función del caso: una ecuación de una variable o el vector de residuos del
  sistema.
- `p0`, `p1` son los puntos iniciales. Los métodos de **intervalo** usan los dos; los de **un
  punto** usan solo `p0`.
- `tol` y `max_iter` son la tolerancia de paro y el máximo de iteraciones.
- Deben devolver **la raíz y las iteraciones realmente usadas**.

Si un método no puede aplicarse —por ejemplo, **bisección sin cambio de signo** en el
intervalo— debe **levantar una excepción**. Eso se registra como fallo de *esa* muestra y es
información valiosa para su informe.

> 🧪 **El bloque `if __name__ == '__main__':` es su banco de pruebas.** Sirve para comprobar que
> sus métodos están bien programados, usando una función conocida ($x^2-2$, cuya raíz es
> $\sqrt{2}$), sin necesidad de abrir Colab.
>
> **No** sirve para elegir el intervalo de su caso: eso se hace con el **análisis gráfico** en el
> notebook (sección 5), porque ahí están su ecuación y sus parámetros.

---

## 5. Qué contiene el notebook

| Sección | Qué hacen |
|---|---|
| **Configuración e identificación** | Monta Drive, descarga el repositorio y valida quién eres |
| **1. Elige tu caso** | Reservar el tema |
| **2. Integrantes** | Registrar al equipo |
| **3. Tu caso** | Muestran su ecuación, incógnita, incertidumbres y métodos sugeridos |
| **4. Librería del equipo** | Cargan `lib/metodos_equipo.py` |
| **5. Análisis del caso** | Ecuación y derivada con `sympy` · **verificación de la derivada a mano** · **aislamiento de la raíz** (gráfica + cambio de signo) |
| **6. Tus métodos** | Declaran qué métodos implementaron |
| **7. Monte Carlo** | Corren la simulación |
| **8. Gráficos** | Histogramas, % de divergencia, **gráfico de cajas** y respuesta física |
| **9. Conclusiones** | 5 preguntas de criterio |
| **10. Calificación y envío** | Nota automática y envío |


## 6. Familias de métodos

Cada equipo debe comparar **3 o 4 métodos de familias distintas** (ideal: uno *cerrado
garantizado* + uno *abierto rápido* + uno *híbrido o especial*).

| Familia | Métodos |
|---|---|
| **Cerrado** — converge siempre, *si* hay cambio de signo | Bisección, Falsa posición, Punto fijo modificado |
| **Abierto** — rápido, pero puede divergir | Punto fijo, Newton-Raphson, NR modificado, Secante, Secante modificado |
| **Híbrido** | Brent |
| **Polinomios** | Müller, Bairstow |

| Método | Tipo | Valores iniciales | Convergencia | Estabilidad | Programación |
|---|---|---|---|---|---|
| Bisección | Cerrado | 2 | Lenta | Siempre | Fácil |
| Falsa posición | Cerrado | 2 | Lenta/media | Siempre | Fácil |
| Punto fijo modificado | Cerrado | 2 | Media | Siempre | Fácil |
| Punto fijo | Abierto | 1 | Lenta | Posiblemente divergente | Fácil |
| Newton-Raphson | Abierto | 1 | Rápida | Posiblemente divergente | Fácil |
| NR modificado | Abierto | 1 | Rápida (múltiple), media (única) | Posiblemente divergente | Fácil |
| Secante | Abierto | 2 | Media/rápida | Posiblemente divergente | Fácil |
| Secante modificado | Abierto | 1 | Media/rápida | Posiblemente divergente | Fácil |
| Brent | Híbrido | 1 o 2 | Media | Siempre (2 condiciones) | Moderada |
| Müller | Polinomios | 2 | Media/rápida | Posiblemente divergente | Moderada |
| Bairstow | Polinomios | 2 | Rápida | Posiblemente divergente | Moderada |

> **Müller y Bairstow** solo se exigen en los **temas polinómicos** (T4). En los demás temas son
> opcionales y, si los incluyen, cuentan como **método extra**.

---

## 7. La simulación de Monte Carlo

La simulación somete sus algoritmos a la **incertidumbre real** del sistema: tolerancias de
componentes, ruido de sensores, variación de fabricación y errores al *aislar* la raíz.

**Cómo funciona**

- Se perturban los parámetros del caso (según la incertidumbre de su tema) y se generan
  **1000 escenarios distintos**.
- Todos los métodos se prueban sobre **exactamente los mismos** 1000 escenarios, para que la
  comparación sea justa.
- La **raíz de referencia** de cada escenario se calcula aparte, con un método de precisión
  altísima. Es el **juez**: no basta con que su método "se detenga", tiene que **acertar la
  raíz**.

**Qué se mide, por método**

| Métrica | Qué significa |
|---|---|
| `% éxito` | En qué porcentaje de escenarios acertó la raíz |
| `% divergencia` | En qué porcentaje falló |
| `n_iter` | Iteraciones usadas (velocidad) |
| `err_ref` | Qué tan lejos quedó de la raíz verdadera |

**Cuándo un método "cuenta"**

- Si acierta la raíz de referencia en **al menos el 80 %** de los escenarios, y
- si resuelve el problema con iteraciones de verdad: un *envoltorio* que delegue el trabajo en
  otra rutina no cuenta.

**Gráficos que deben generar y analizar**

1. **Histograma de iteraciones** por método.
2. **Tasa de divergencia** por método.
3. ⭐ **Gráfico de cajas (*box plot*)** de iteraciones: de un vistazo se ve qué método es más
   rápido, cuál es más consistente y cuáles tienen valores atípicos.
4. **Distribución de la respuesta física** ante la incertidumbre.

> 💡 **Pista para su informe:** si aíslan bien la raíz, los métodos **abiertos** suelen ser los
> más rápidos, y en este tipo de problemas también bastante confiables. Los de **intervalo** son
> su red de seguridad cuando el aislamiento es difícil, pero **necesitan** el cambio de signo
> para arrancar. Y ojo con la **falsa posición**: en algunas funciones se "estanca" de un lado y
> necesita muchísimas iteraciones. Muestren todo eso con datos, no con opiniones.

### 🔍 El paso que no se pueden saltar: aislar la raíz

Antes de simular, **grafíquen $f$** con los valores nominales y localicen dónde cruza el eje.
El notebook tiene una celda para eso: grafica la función, imprime el signo en los extremos,
marca la raíz y cuenta cuántas veces se cruza el eje.

**No tienen que rehacer el intervalo muestra por muestra.** Las perturbaciones son pequeñas
(±1 a 5 %), así que el intervalo que aíslen **una vez** contiene la raíz en *todos* los
escenarios de la simulación.

---

## 8. Evaluación

| Criterio | Peso |
|---|---|
| Notebook: métodos que *cuentan* + Monte Carlo correcto | **40 %** |
| Preguntas de criterio (se califican solas) | **20 %** |
| Informe (obligatorio, gráficas —incluido el gráfico de cajas— y conclusiones) | **20 %** |
| Exposición (claridad y defensa técnica) | **20 %** |

---

## 9. Catálogo de casos

Cada caso indica: **incógnita · ecuación · parámetros con incertidumbre · métodos sugeridos ·
desafío principal · qué deben ver en el gráfico de cajas.**

---

### Bloque A — Básicos (equipos de 2)

#### T1 · Fuerza electrostática en sensor anular

- **Incógnita:** $x$ (distancia) tal que $F=1$ N.
- **Ecuación:** $F(x)=\dfrac{1}{4\pi\varepsilon_0}\dfrac{qQx}{(x^2+a^2)^{3/2}}=1$.
- **Incertidumbre:** $q$, $Q$, $a$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Newton-Raphson · Secante.
- **Desafío:** $F'(x)=0$ en el máximo de la fuerza, así que **Newton-Raphson puede divergir** con
  un mal $x_0$. Además hay **dos ramas** de solución: hay que aislar la correcta.
- **En el box plot deben ver:** bisección estable frente a Newton-Raphson, que es más rápido pero
  con valores atípicos cuando el arranque es malo.

#### T2 · Resorte no lineal en suspensión de robot móvil

- **Incógnita:** deflexión $d\ge 0$.
- **Ecuación:** $\tfrac12 k_1 d^2+\tfrac25 k_2 d^{5/2}-mgd-mgh=0$.
- **Incertidumbre:** $k_1$, $k_2$, $m$, $h$ con $\sigma=3\%$.
- **Métodos sugeridos:** Punto fijo · Secante · Brent.
- **Desafío:** el exponente fraccionario $d^{5/2}$ **restringe el dominio** a $d\ge0$; el punto
  fijo puede divergir.
- **En el box plot deben ver:** la estabilidad de Brent frente a la dispersión del punto fijo.

#### T3 · Ángulo crítico de vuelco de robot móvil

- **Incógnita:** $\theta$ con $N_t(\theta)=0$.
- **Ecuación:** $N_t = mg\cos\theta - ma\,\mathrm{sen}\,\theta - mg\dfrac{h}{L}\mathrm{sen}\,\theta = 0$.
- **Incertidumbre:** $m$, $a$, $h$, $L$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Secante modificado · Brent.
- **Desafío:** es trigonométrica; hay que **filtrar la raíz física** en $[0,\pi/2]$.
- **En el box plot deben ver:** que Brent reduce la mediana de iteraciones sin perder robustez.

#### T4 · Calibración de sensor de temperatura (polinomio de 4.º grado)

- **Incógnita:** $T$ tal que $c_p(T)=1.2$.
- **Ecuación:** $0.99403+1.671\!\times\!10^{-4}T+9.7215\!\times\!10^{-8}T^2-9.5838\!\times\!10^{-11}T^3+1.9520\!\times\!10^{-14}T^4=1.2$.
- **Incertidumbre:** coeficientes y objetivo con $\sigma=1\%$.
- **Métodos sugeridos:** **Bairstow · Müller** · Newton-Raphson.
- **Desafío:** hay **varias raíces reales**; deben elegir la **físicamente válida** y comparar los
  métodos **especializados en polinomios**.
- **En el box plot deben ver:** Müller y Bairstow frente a Newton-Raphson (velocidad y fallos).

> 🔺 **Este es un tema polinómico:** se exige **Müller o Bairstow** entre sus métodos.

---

### Bloque B — Intermedios (equipos de 3)

#### T5 · Punto de operación con diodo Zener

- **Incógnita:** $V_D$.
- **Ecuación:** $I_S\!\left(e^{V_D/nV_T}-1\right)=\dfrac{V_{CC}-V_D}{R_L}$.
- **Incertidumbre:** $I_S$, $n$, $V_T$, $V_{CC}$, $R_L$ con $\sigma=5\%$.
- **Métodos sugeridos:** Newton-Raphson · Punto fijo · Bisección.
- **Desafío:** la exponencial explota; el punto fijo converge lento y Newton-Raphson es sensible
  al valor inicial.
- **En el box plot deben ver:** Newton-Raphson con pocas iteraciones frente al punto fijo con
  muchas, y el porcentaje de divergencia de Newton-Raphson.

#### T6 · Tensión en cable de catenaria

- **Incógnita:** $T_A$.
- **Ecuación:** $y=\dfrac{T_A}{w}\cosh\!\left(\dfrac{w}{T_A}x\right)+y_0-\dfrac{T_A}{w}$.
- **Incertidumbre:** $w$, $x$, $y$, $y_0$ con $\sigma=2\%$.
- **Métodos sugeridos:** Punto fijo · Secante modificado · Brent.
- **Desafío:** el $\cosh$ **desborda** si $T_A$ es pequeño; hay que **acotar bien** el intervalo.
- **En el box plot deben ver:** la mediana de iteraciones y los fallos por desbordamiento.

#### T7 · Tirante en canal abierto (Manning)

- **Incógnita:** $H$.
- **Ecuación:** $Q=\dfrac{\sqrt{S}(BH)^{5/3}}{n(B+2H)^{2/3}}$.
- **Incertidumbre:** $S$, $Q$, $n$, $B$ con $\sigma=3\%$.
- **Métodos sugeridos:** Punto fijo modificado (comparen **dos despejes**) · Bisección · Secante.
- **Desafío:** la **forma del despeje** cambia la convergencia: unos convergen y otros divergen.
- **En el box plot deben ver:** el mismo método con dos despejes distintos, uno estable y otro no.

#### T8 · Tiro parabólico con alturas desiguales

- **Incógnita:** $\theta_0$.
- **Ecuación:** $y=(\tan\theta_0)x-\dfrac{g}{2v_0^2\cos^2\theta_0}x^2+y_0$.
- **Incertidumbre:** $x$, $v_0$, $y$, $y_0$ con $\sigma=2\%$.
- **Métodos sugeridos:** Secante modificado · Bisección · Brent.
- **Desafío:** usando $\sec^2\theta_0=1+\tan^2\theta_0$ se vuelve un **polinomio en $\tan\theta_0$**
  con **dos ángulos posibles**; deben elegir la raíz físicamente válida.
- **En el box plot deben ver:** las iteraciones de cada método y su dispersión.

#### T9 · Transitorio RLC de servomotor

- **Incógnita:** $R$ para que $q/q_0=1\%$ en $t=0.05$ s.
- **Ecuación:** $e^{-Rt/2L}\cos\!\Big(\sqrt{\tfrac{1}{LC}-(\tfrac{R}{2L})^2}\,t\Big)-\tfrac{q}{q_0}=0$.
- **Incertidumbre:** $L$, $C$, $t$, $q/q_0$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Newton-Raphson · Secante.
- **Desafío:** es **oscilatoria**, así que hay varias raíces; hay que acotar $R$ para aislar la
  correcta.
- **En el box plot deben ver:** bisección estable frente a Newton-Raphson con valores atípicos.

---

### Bloque C — Estándar mecatrónica (equipos de 4)

#### T10 · Impedancia / resonancia en sensor piezoeléctrico

- **Incógnita:** $\omega$ tal que $Z=75\ \Omega$.
- **Ecuación:** $\dfrac{1}{Z}=\sqrt{\dfrac{1}{R^2}+\left(\omega C-\dfrac{1}{\omega L}\right)^2}$.
- **Incertidumbre:** $R$, $C$, $L$, $Z$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Falsa posición · Brent.
- **Desafío:** hay una **asíntota** cuando $\omega\to0$, y la **falsa posición se estanca** de un
  lado.
- **En el box plot deben ver:** la falsa posición estancada frente a Brent.

#### T11 · Volumen molar (Van der Waals)

- **Incógnita:** $v$.
- **Ecuación:** $\left(p+\dfrac{a}{v^2}\right)(v-b)=RT$.
- **Incertidumbre:** $p$, $T$, $a$, $b$ con $\sigma=2\%$.
- **Métodos sugeridos:** Newton-Raphson (arrancando con $v_0=RT/p$ del gas ideal) · Secante · Brent.
- **Desafío:** comparar con el gas ideal y analizar la sensibilidad a la presión.
- **En el box plot deben ver:** qué tan rápido es Newton-Raphson si arranca del gas ideal, y cómo
  se dispersa al variar $p$.

#### T12 · Razón de recirculación en reactor autocatalítico

- **Incógnita:** $R$ con $X_{Af}=0.9$.
- **Ecuación:** $\ln\dfrac{1+R(1-X_{Af})}{R(1-X_{Af})}=\dfrac{R+1}{R\,[1+R(1-X_{Af})]}$.
- **Incertidumbre:** $X_{Af}$ con $\sigma=2\%$.
- **Métodos sugeridos:** Bisección · Punto fijo · Secante.
- **Desafío:** hay una **discontinuidad** del logaritmo cerca de $R\to0$.
- **En el box plot deben ver:** cómo se disparan las iteraciones al acercarse al polo.

#### T13 · Colebrook + caída de presión (actuador neumático)

- **Incógnita:** $f$ (y luego $\Delta p$).
- **Ecuaciones:** $\dfrac{1}{\sqrt f}=-2\log_{10}\!\left(\dfrac{\epsilon}{3.7D}+\dfrac{2.51}{Re\sqrt f}\right)$,
  con $Re=\dfrac{\rho VD}{\mu}$.
- **Incertidumbre:** $\epsilon$, $D$, $V$, $\rho$, $\mu$ con $\sigma=2\%$.
- **Métodos sugeridos:** Punto fijo (aquí es rápido) · Newton-Raphson · Brent.
- **Desafío:** Newton-Raphson **diverge** si $x_0>0.066$; usen **Swamee-Jain** como valor inicial.
- **En el box plot deben ver:** el punto fijo estable y rápido frente a Newton-Raphson con fallos.

#### T14 · Cinemática inversa 2-DOF (Jacobiano)

- **Incógnitas:** $(\theta_1,\theta_2)$.
- **Sistema:**
  $L_1\cos\theta_1+L_2\cos(\theta_1+\theta_2)=x$
  y $L_1\mathrm{sen}\,\theta_1+L_2\mathrm{sen}(\theta_1+\theta_2)=y$.
- **Incertidumbre:** $L_1$, $L_2$ con $\sigma=1\%$; objetivo $(x,y)$ con $\sigma=1\%$; valores
  iniciales $(\theta_1^0,\theta_2^0)$ aleatorios.
- **Métodos sugeridos:** **Newton-Raphson multivariable** (Jacobiano con `sympy`) · Punto fijo
  modificado.
- **Desafío:** el **Jacobiano se vuelve singular** en la frontera del espacio de trabajo.
- **En el box plot deben ver:** las iteraciones del sistema 2×2 y el porcentaje de divergencia
  cuando el Jacobiano está casi singular.

#### T15 · Multilateración con 3 balizas (Jacobiano)

- **Incógnitas:** $(x,y)$.
- **Sistema:** $(x-x_i)^2+(y-y_i)^2=d_i^2$ para $i=1,2,3$.
- **Incertidumbre:** $d_i$ con $\sigma=1\%$ (ruido de medición).
- **Métodos sugeridos:** Newton-Raphson multivariable (Jacobiano) · *(opcional)* mínimos cuadrados.
- **Desafío:** el sistema es **sobredeterminado**: hay que elegir bien el subconjunto de
  ecuaciones y la estimación inicial.
- **En el box plot deben ver:** la distribución de iteraciones y de la posición estimada.

---

### Bloque D — Avanzados (equipos de 5)

#### T16 · Velocidad terminal con $C_D$ no lineal

- **Incógnita:** $v$.
- **Ecuaciones:** $v=\sqrt{\dfrac{4g(\rho_s-\rho)d}{3C_D\rho}}$,
  $C_D=\dfrac{24}{Re}+\dfrac{3}{\sqrt{Re}}+0.34$, $Re=\dfrac{\rho dv}{\mu}$.
- **Incertidumbre:** $d$, $\rho_s$, $\rho$, $\mu$ con $\sigma=3\%$.
- **Métodos sugeridos:** Secante · Secante modificado · Brent.
- **Desafío:** verificar el **régimen** resultante ($Re>0.1$).
- **En el box plot deben ver:** la comparación entre métodos y el régimen que resulta.

#### T17 · Péndulo amortiguado forzado (amplitud / resonancia)

- **Incógnita:** $\omega$ (o $\zeta$ para la amplitud máxima).
- **Ecuación:** $(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2=(F_0/(mA))^2$.
- **Incertidumbre:** $\omega_n$, $F_0$, $m$, $\zeta$ con $\sigma=3\%$.
- **Métodos sugeridos:** Newton-Raphson · Secante modificado · Brent.
- **Desafío:** seleccionar las raíces **físicas** ($\omega>0$).
- **En el box plot deben ver:** las iteraciones y la dispersión de la frecuencia.

---

### Bloque E — Integradores (equipos de 6)

#### T18 · Empuje vectorizado (gimbal) — balance de momentos

- **Incógnita:** $\theta$ tal que $M(\theta)=0$ (momentos del orbitador, los cohetes y el tanque
  respecto al centro de gravedad $G$).
- **Incertidumbre:** empujes $\pm3\%$; peso del tanque $W_S$ entre $195{,}000$ y $230{,}000$ lb.
- **Métodos sugeridos:** Newton-Raphson (5 cifras) · Brent · Secante.
- **Desafío:** hay **varias raíces**; grafiquen $M(\theta)$ en $[-\pi,\pi]$ y analicen la
  sensibilidad al peso.
- **En el box plot deben ver:** cómo se distribuye el ángulo $\theta$ conforme cambia el peso.

#### T19 · Red de tuberías no lineal (2–3 nodos)

- **Incógnitas:** los caudales $(Q_1,\dots,Q_n)$.
- **Sistema:** $\sum Q_i = 0$ en cada nodo, y $\Delta p = K Q^n$ por tramo.
- **Incertidumbre:** $K_i$ y $n$ con $\sigma=3\%$.
- **Métodos sugeridos:** Newton-Raphson multivariable (Jacobiano con `sympy`) · Punto fijo
  modificado.
- **Desafío:** el **acoplamiento** entre nodos y elegir un buen punto inicial.
- **En el box plot deben ver:** las iteraciones del sistema y la dispersión de los caudales.

---

## 10. Preguntas frecuentes

**¿Puedo cambiar de tema después de reservarlo?**
No. El tema queda bloqueado. Si hubo un error, usen la celda **Eliminar equipo** (con
`PERMITIR_ELIMINAR = True` y siendo integrante) y empiecen de nuevo.

**¿Todos los integrantes tienen que ejecutar las celdas de selección?**
No. Solo el **jefe de equipo**, y una sola vez. Después, todos trabajan en el notebook.

**¿Tengo que recalcular el intervalo de la raíz en cada escenario de la simulación?**
No. Las perturbaciones son pequeñas, así que el intervalo que aíslen una vez sirve para toda la
simulación.

**Mi método falla en algunas muestras, ¿está mal?**
No necesariamente. Los métodos de intervalo **no pueden arrancar** si el intervalo no encierra la
raíz, y los abiertos pueden divergir con un mal arranque. Eso es exactamente lo que la simulación
mide: repórtenlo con datos.

**¿Qué pasa si mi método "casi" acierta?**
Cuenta como acierto si queda dentro de la tolerancia pedida ($10^{-6}$ absoluto o $10^{-4}$
relativo). Lo que **no** cuenta es detenerse en un punto que **no es raíz**.

**¿Y si mi método en realidad llama a otra rutina que ya resuelve todo?**
No cuenta: la simulación detecta los casos en los que el método no hace iteraciones de verdad, y
la revisión del informe y la exposición es del profesor.

**¿Cómo sé qué método conviene programar para el firmware?**
Compárenlos con **datos propios**: velocidad (mediana de iteraciones), robustez (% de
divergencia) y costo (¿necesita derivada? ¿necesita intervalo?). Esa comparación es el corazón de
su reporte y exposición.
