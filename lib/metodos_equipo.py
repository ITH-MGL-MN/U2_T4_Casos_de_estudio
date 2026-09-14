# -*- coding: utf-8 -*-
"""metodos_equipo.py — Librería de métodos numéricos del EQUIPO (U2_T4).

Cada equipo implementa aquí sus métodos y los prueba en su computadora.
El notebook de Colab IMPORTA este archivo desde su carpeta de Google Drive.

CONTRATO OBLIGATORIO (una ecuación):
    g(f, p0, p1, tol, max_iter) -> (raiz, n_iter)
      f        : función de una variable, callable, f(x) -> float
      p0, p1   : punto(s) inicial(es). Métodos de intervalo usan [p0,p1];
                 métodos de un punto usan solo p0.
      tol      : tolerancia de paro
      max_iter : iteraciones máximas
      raiz     : la raíz aproximada (float)
      n_iter   : iteraciones realmente usadas (int)

CONTRATO OBLIGATORIO (sistemas, para temas con Jacobiano):
    g(F, x0, _x1, tol, max_iter) -> (vector_raiz, n_iter)
      F   : callable X -> np.array([...])  (vector de residuos)
      x0  : punto inicial (np.array)

Prueba local:  python metodos_equipo.py
"""
import numpy as np

# ===========================================================================
# 1) ECUACIÓN DE PRUEBA (para probar en tu computadora)
#    f(x) = x^2 - 2  ->  raíz = sqrt(2) = 1.41421356...
# ===========================================================================
def f_prueba(x):
    return x ** 2 - 2.0


# ===========================================================================
# 2) MÉTODOS CERRADOS (intervalo)
# ===========================================================================
def biseccion(f, p0, p1, tol=1e-6, max_iter=100):
    """Bisección. Requiere f(a)*f(b) < 0."""
    a, b = min(p0, p1), max(p0, p1)
    fa, fb = f(a), f(b)
    if fa == 0:
        return a, 0
    if fb == 0:
        return b, 0
    if fa * fb > 0:
        raise ValueError('La bisección necesita cambio de signo en [a, b].')
    for k in range(1, max_iter + 1):
        m = 0.5 * (a + b)
        fm = f(m)
        if fm == 0 or (b - a) / 2 < tol:
            return m, k
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b), max_iter


def falsa_posicion(f, p0, p1, tol=1e-6, max_iter=100):
    """Falsa posición (regula falsi)."""
    a, b = min(p0, p1), max(p0, p1)
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError('La falsa posición necesita cambio de signo en [a, b].')
    x_prev = None
    for k in range(1, max_iter + 1):
        x = b - fb * (b - a) / (fb - fa)
        fx = f(x)
        if fx == 0 or (x_prev is not None and abs(x - x_prev) < tol):
            return x, k
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
        x_prev = x
    return x, max_iter


# ===========================================================================
# 3) MÉTODOS ABIERTOS
# ===========================================================================
def punto_fijo(f, p0, _p1=None, tol=1e-6, max_iter=100, g=None):
    """Iteración de punto fijo: x_{k+1} = g(x_k).

    Aquí `f` se usa solo para comprobar; `g` es el despeje (debes pasarlo).
    Si no defines `g`, se usa x -> x - f(x) (equivalente débil).
    """
    gg = g if g is not None else (lambda x: x - f(x))
    x = float(p0)
    for k in range(1, max_iter + 1):
        x_new = gg(x)
        if abs(x_new - x) < tol:
            return x_new, k
        x = x_new
    return x, max_iter


def newton_raphson(f, p0, _p1=None, tol=1e-6, max_iter=100, df=None):
    """Newton-Raphson. `df` es la derivada; si no se pasa, se aproxima numéricamente."""
    if df is None:
        def df(x, h=1e-7):
            return (f(x + h) - f(x - h)) / (2 * h)
    x = float(p0)
    for k in range(1, max_iter + 1):
        fx, dfx = f(x), df(x)
        if abs(dfx) < 1e-14:
            raise ValueError('Derivada casi nula: Newton-Raphson no puede continuar.')
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            return x_new, k
        x = x_new
    return x, max_iter


def secante(f, p0, p1, tol=1e-6, max_iter=100):
    """Secante. No requiere cambio de signo ni derivada."""
    x0, x1 = float(p0), float(p1)
    f0, f1 = f(x0), f(x1)
    for k in range(1, max_iter + 1):
        if abs(f1 - f0) < 1e-14:
            raise ValueError('División por cero en la secante.')
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(x2 - x1) < tol:
            return x2, k
        x0, f0, x1, f1 = x1, f1, x2, f(x2)
    return x1, max_iter


# ===========================================================================
# 4) SISTEMAS (2x2) — para T14, T15, T19
# ===========================================================================
def newton_sistema(F, x0, _x1=None, tol=1e-6, max_iter=100, J=None):
    """Newton-Raphson multivariable con Jacobiano numérico."""
    X = np.array(x0, dtype=float)
    n = len(X)
    h = 1e-7
    for k in range(1, max_iter + 1):
        Fx = np.array(F(X), dtype=float)
        if np.max(np.abs(Fx)) < tol:
            return X, k
        Jm = np.zeros((n, n))
        for j in range(n):
            dX = np.zeros(n); dX[j] = h
            Jm[:, j] = (np.array(F(X + dX)) - np.array(F(X - dX))) / (2 * h)
        if abs(np.linalg.det(Jm)) < 1e-14:
            raise ValueError('Jacobiano casi singular.')
        X = X - np.linalg.solve(Jm, Fx)
    return X, max_iter


# ===========================================================================
# 5) PRUEBAS LOCAL (python metodos_equipo.py)
# ===========================================================================
if __name__ == '__main__':
    esperado = np.sqrt(2)
    pruebas = [
        ('Bisección', biseccion(f_prueba, 0, 2)),
        ('Falsa posición', falsa_posicion(f_prueba, 0, 2)),
        ('Secante', secante(f_prueba, 0, 2)),
        ('Newton-Raphson', newton_raphson(f_prueba, 1.0)),
    ]
    print('Raíz de x^2-2 = %.10f' % esperado)
    for nombre, (raiz, it) in pruebas:
        err = abs(raiz - esperado)
        estado = 'OK ' if err < 1e-5 else 'REVISAR'
        print('%-16s %s  raiz=%.10f  iter=%d  err=%.2e' % (nombre, estado, raiz, it, err))
