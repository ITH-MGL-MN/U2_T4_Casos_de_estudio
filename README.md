# U2_T4 · Proyecto: casos de estudio con raíces de ecuaciones + Monte Carlo

Cada equipo elige **un caso de estudio de ingeniería mecatrónica** planteado como una
**ecuación** (o un **sistema**) de raíces, y lo analiza con una **simulación de Monte Carlo**
para decidir, con evidencia, **qué método numérico conviene** en un sistema real donde nada es
exacto.

> ⚠️ **La información de sus reportes se usará en el examen, en la sección de casos.**

## Contenido

1. [Qué tienes que hacer](#1-qué-tienes-que-hacer)
2. [Los 19 casos de estudio](#2-los-19-casos-de-estudio)
3. [Los dos cuadernos de Colab](#3-los-dos-cuadernos-de-colab)
4. [Las reglas de entrega](#4-las-reglas-de-entrega)
5. [Cómo se califica](#5-cómo-se-califica)
6. [Puntos extra](#6-puntos-extra)
7. [Qué debe llevar el reporte](#7-qué-debe-llevar-el-reporte)
8. [Preguntas frecuentes](#8-preguntas-frecuentes)

---

## 1. Qué tienes que hacer

1. **Elige un caso** de la lista de la sección 2 (lo reserva el jefe de equipo; queda bloqueado
   para tu equipo).
2. **Corre la simulación** en el cuaderno 2: el motor ya trae **todos los métodos
   implementados**, tú **no programas nada**.
3. **Elige con casillas** los métodos que vas a comparar: **todos los recomendados** de tu caso
   **+ al menos un método de contraejemplo** (uno que no convenga, para contrastar).
4. **Interpreta las gráficas** e **investiga por qué falló cada método**.
5. **Escribe el reporte** con la plantilla de Overleaf y entrégalo en PDF.

**La pregunta que debe responder tu reporte:**

> *"Si estuvieran diseñando el firmware del controlador de este sistema mecatrónico en tiempo
> real, ¿qué método programarían y por qué?"*

---

## 2. Los 19 casos de estudio

| Tema | Caso | Incógnita | Tipo | Métodos recomendados |
|---|---|---|---|---|
| **T1** | Fuerza electrostática en sensor anular | $x$ / m | Ecuación | Bisección, Newton-Raphson, Secante |
| **T2** | Resorte no lineal en suspensión de robot móvil | $d$ / m | Ecuación | Punto fijo, Secante, Brent |
| **T3** | Ángulo crítico de vuelco de robot móvil | $\theta$ / rad | Ecuación | Bisección, Secante modificado, Brent |
| **T4** | Calibración de sensor de temperatura (polinomio) | $T$ / K | Ecuación | Bairstow, Müller, Newton-Raphson |
| **T5** | Punto de operación con diodo Zener | $V_D$ / V | Ecuación | Newton-Raphson, Punto fijo, Bisección |
| **T6** | Tensión en cable de catenaria | $T_A$ / N | Ecuación | Punto fijo, Secante modificado, Brent |
| **T7** | Tirante en canal abierto (Manning) | $H$ / m | Ecuación | Punto fijo modificado, Bisección, Secante |
| **T8** | Tiro parabólico con alturas desiguales | $\theta_0$ / rad | Ecuación | Secante modificado, Bisección, Brent |
| **T9** | Transitorio RLC de servomotor | $R$ / $\Omega$ | Ecuación | Bisección, Newton-Raphson, Secante |
| **T10** | Impedancia/resonancia en sensor piezoeléctrico | $\omega$ / rad/s | Ecuación | Bisección, Falsa posición, Brent |
| **T11** | Volumen molar (Van der Waals) | $v$ / m³/mol | Ecuación | Newton-Raphson, Secante, Brent |
| **T12** | Razón de recirculación en reactor autocatalítico | $R$ | Ecuación | Bisección, Punto fijo, Secante |
| **T13** | Colebrook + caída de presión | $f$ | Ecuación | Punto fijo, Newton-Raphson, Brent |
| **T14** | Cinemática inversa 2-DOF (Jacobiano) | $(\theta_1,\theta_2)$ / rad | **Sistema** | Newton-Raphson multivariable, Punto fijo modificado |
| **T15** | Multilateración con 3 balizas (Jacobiano) | $(x,y)$ / m | **Sistema** | Newton-Raphson multivariable |
| **T16** | Velocidad terminal con $C_D$ no lineal | $v$ / m/s | Ecuación | Secante, Secante modificado, Brent |
| **T17** | Péndulo amortiguado forzado (resonancia) | $\omega$ / rad/s | Ecuación | Newton-Raphson, Secante modificado, Brent |
| **T18** | Empuje vectorizado (gimbal): balance de momentos | $\theta$ / rad | Ecuación | Newton-Raphson, Brent, Secante |
| **T19** | Red de tuberías no lineal (2-3 nodos) | $(Q_1,Q_2)$ / m³/s | **Sistema** | Newton-Raphson multivariable, Punto fijo modificado |

**El reto de cada caso** (útil para elegir — el motor te lo recuerda al correr):

| Tema | Lo difícil del caso |
|---|---|
| T1 | La fuerza tiene un **máximo**: hay dos ramas de solución, se trabaja la ascendente. |
| T2 | Exponente fraccionario $d^{5/2}$: el dominio exige $d \ge 0$ y el punto fijo puede divergir. |
| T3 | Trigonométrica: hay que filtrar la raíz física en $[0, \pi/2]$. |
| T4 | Varias raíces reales: hay que elegir la físicamente válida. |
| T5 | La exponencial explota; el punto fijo converge lento y Newton es sensible al arranque. |
| T6 | El $\cosh$ se desborda si $T_A$ es chico: hay que acotar bien el intervalo. |
| T7 | Según cómo se despeje, unos métodos divergen y otros no. |
| T8 | Hay dos ángulos posibles; se pide el de tiro tendido (la raíz menor). |
| T9 | Oscilatoria: hay varias raíces y hay que aislar la correcta. |
| T10 | Asíntota en $\omega \to 0$: la falsa posición se estanca de un solo lado. |
| T11 | Comparar con el gas ideal; sensibilidad a la presión. |
| T12 | Discontinuidad del logaritmo cerca de $R \to 0$. |
| T13 | Newton diverge si el arranque es malo; conviene usar Swamee-Jain como $x_0$. |
| T14 | El Jacobiano es singular en la frontera del espacio de trabajo. |
| T15 | Trae ruido de medición (±1 %): la estimación inicial es crítica. |
| T16 | Verificar el régimen resultante ($Re > 0.1$). |
| T17 | Hay que seleccionar la raíz física (la de la resonancia). |
| T18 | Varias raíces: graficar el momento y cuidar la sensibilidad al peso. |
| T19 | Acoplamiento entre nodos y buen punto inicial. |

> La **ecuación exacta** de tu caso aparece en tu cuaderno (sección 3) en cuanto el jefe reserva
> el tema.

---

## 3. Los dos cuadernos de Colab

El trabajo está partido en dos a propósito: así **los dos se pueden ejecutar de golpe** sin
volver a reservar nada.

| Cuaderno | Quién lo usa | Cuándo | Para qué |
|---|---|---|---|
| **`U2_T4_1_Equipo`** | **solo el jefe** | **una sola vez** | Identificarse, **reservar el tema** y registrar a los integrantes |
| **`U2_T4_2_Caso`** | **cada integrante** | cuando quieran | **El ejercicio**: aislar la raíz, elegir métodos, Monte Carlo y gráficas |

**Pasos:**

1. Ábrelos en Colab y **guarda una copia en tu Drive** (Archivo → Guardar una copia en Drive),
   para que puedas volver a ellos.
2. **Solo el jefe** ejecuta el cuaderno 1. No hay que escribir su número de control: se detecta
   solo a partir de su correo institucional. **Inicia sesión con tu correo institucional.**
3. **Cada integrante** abre el cuaderno 2 y lo ejecuta completo. El cuaderno 2 **lee** lo que
   guardó el cuaderno 1, así que no hay que volver a identificarse.
4. Las **gráficas son interactivas**: puedes seleccionar puntos (caja y lazo), hacer zoom, ver
   el valor al pasar el cursor y **descargarlas como imagen** para el reporte.

---

## 4. Las reglas de entrega

**Qué se entrega:**

1. **Reporte en PDF**, hecho sobre la **plantilla de Overleaf** (el enlace está en Classroom).
   Es **por equipo**: compartan la carpeta de Overleaf entre los integrantes.
2. *(Opcional)* **Diapositivas** de la exposición.
3. El **envío de la calificación** lo hace el propio cuaderno 2 con su última celda.

**Reglas del envío:**

* Se puede enviar **hasta 2 veces**.
* **Basta con que una persona** del equipo ejecute la celda de envío: la calificación se registra
  para **todos** los integrantes.
* El cuaderno **no deja enviar** si la selección de métodos está incompleta, y **no gasta
  intento** cuando lo bloquea.
* Antes de enviar, la sección 10 del cuaderno te deja **ver lo que ya está guardado** (no envía
  nada ni gasta intentos).

---

## 5. Cómo se califica

| Parte | Quién la evalúa |
|---|---|
| **Selección de métodos** | **Automática**: 100 si incluyes todos los recomendados de tu caso **y** al menos un contraejemplo; 0 si no |
| **Reporte** (interpretación, gráficas, conclusiones) | **A mano** |
| **Exposición** | **A mano** |

* En los casos de **sistema** (T14, T15, T19) **no** se pide contraejemplo: sus dos únicas
  opciones ya son las recomendadas.
* La autocalificación **solo mira la selección**, no la calidad del reporte.

---

## 6. Puntos extra

Hay **dos formas** de ganar puntos extra, y las dos se demuestran con el cuaderno:

1. 🏆 **Un método con 100 % de éxito.** Si algún método de tu caso acierta la raíz en
   **todas** las muestras (0 % de fallos), ganas puntos extra.
2. 🏆 **Un intervalo (o un arranque) con 100 % de éxito.** Usa los controles de la **sección 4**
   del cuaderno:
   * `MIS_INTERVALOS`: si propones un intervalo que **encierre la raíz en todas las muestras**,
     los métodos de paréntesis (bisección, falsa posición, punto fijo modificado, Brent) pasan
     al **100 %**. Ojo: la incertidumbre **mueve** la raíz, así que el intervalo debe cubrir
     **todo su rango**, no solo el cruce de la gráfica (el cuaderno te imprime ese rango y te
     avisa si te quedas corto).
   * `MIS_ARRANQUES`: lo mismo para los métodos **abiertos y polinómicos**, con un punto de
     arranque **cerca** de la raíz.

> En **18 de los 19 casos** se puede llegar al 100 % con el intervalo o el arranque correctos.
> Si tu caso es el único donde no se puede, **explica por qué** (varias raíces: el método llega
> a una raíz distinta de la que buscas) y **también cuenta** para los puntos extra.

**Lo que vale es la justificación:** que el 100 % salga de un intervalo o un arranque
*defendible*, no de probar números al azar hasta que dé bien.

---

## 7. Qué debe llevar el reporte

* Los **métodos recomendados** de tu caso, con la evidencia de la simulación.
* Al **menos un método de contraejemplo**: uno que **no** convenga en tu caso, y **por qué**.
* La **interpretación de las gráficas**:
  * quién es más **rápido** y quién más **confiable**;
  * **por qué falló** cada método (no es lo mismo *"no arrancó"* que *"divergió"*, *"se fue al
    plano complejo"* o *"convergió a otra raíz"*);
  * qué tan **sensible** es la respuesta a la incertidumbre del caso.
* La respuesta a la **pregunta del firmware**.
* Las **gráficas** (descárgalas del cuaderno con el botón de descarga).

---

## 8. Preguntas frecuentes

**¿Tengo que programar los métodos?**
No. **Todos vienen implementados** en el motor. Este trabajo es **teórico**: se trata de
elegir y de interpretar.

**¿Qué es un método de contraejemplo?**
Un método que **no** está entre los recomendados de tu caso: sirve para **contrastar** y
demostrar que no siempre "más rápido" es mejor. Es **obligatorio** incluir al menos uno (salvo
en los casos de sistema).

**¿Puedo cambiar de tema?**
El tema queda **bloqueado** para tu equipo en cuanto el jefe lo reserva. Si se equivocaron, hay
una celda para **eliminar el equipo** (el jefe la habilita cambiando `PERMITIR_ELIMINAR = True`).

**¿Por qué falla un método aunque el intervalo "encierre" la raíz?**
Porque **la raíz se mueve**: la incertidumbre del caso la desplaza de una muestra a otra. Un
intervalo angosto alrededor del cruce de la gráfica deja fuera a la mayoría de las muestras. La
sección 4 del cuaderno te imprime el **rango real** de la raíz.

**¿Cuántas muestras corre la simulación?**
1000 por defecto. Puedes bajarlas mientras experimentas, pero **el reporte y la entrega deben
usar 1000**.

**¿Puedo enviar si mi selección está incompleta?**
No: el cuaderno lo bloquea y **no te gasta intento**. Corrige las casillas y vuelve a ejecutar.

**¿Las calificaciones de todos los integrantes son iguales?**
Sí: el envío es **por equipo** y se registra para todos. La calificación que aparece es la de la
**selección**; el reporte y la exposición se revisan a mano.
