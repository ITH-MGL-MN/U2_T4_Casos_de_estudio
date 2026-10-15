# Preguntas de criterio (conceptuales) — U2_T4

Estas preguntas **ya no se autocalifican**: son parte del **informe** y de la
**exposición**. La fuente de verdad de su texto está en `config/preguntas.yaml`
(banco `criterio`); este archivo solo las documenta para referencia del profesor.

1. **C1** — Si tuvieras que garantizar SIEMPRE una raíz (aunque tarde), ¿qué
   familia elegirías?
   * Correcta: un método de intervalo (bisección / falsa posición).

2. **C2** — ¿Qué necesitas además de `f(x)` para aplicar Newton-Raphson?
   * Correcta: la derivada `f'(x)`.

3. **C3** — Un método marca "convergió" porque `|x_{k+1}-x_k| < tol`. ¿Eso
   prueba que `x` es una raíz?
   * Correcta: no; hay que verificar el residuo `|f(x)|` y comparar con una
     referencia.

Además, el cuaderno genera dos preguntas **basadas en los resultados propios**
de la simulación (qué método fue el más rápido y cuál falló más), que también
forman parte del informe y no se autocalifican.
