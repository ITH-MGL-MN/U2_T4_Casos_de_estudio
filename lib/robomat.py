"""robomat — sintaxis estilo MATLAB para robótica y métodos numéricos.

Atajos para que el alumno escriba menos código:

    M[[a, b], [c, d]]   -> crear matriz (numérica o simbólica)
    I[4]                -> matriz identidad 4x4
    I[3, 4]             -> identidad rectangular (como eye(3, 4))
    var('q1', 'q2')     -> variables simbólicas
    sin, cos, tan       -> trigonométricas "inteligentes" (SymPy o NumPy)
    rad / deg           -> conversión grados <-> radianes
    evaluar(expr, vars, valores) -> sustituir valores numéricos
    mostrar(expr)       -> renderizar en LaTeX
    jacobiano(pos, vars)-> matriz jacobiana
"""

import numpy as np
import sympy as sym
from IPython.display import display, Math

sym.init_printing(use_latex='mathjax')


def mostrar(expr):
    """Renderiza una matriz o expresión en LaTeX."""
    if isinstance(expr, (sym.MatrixBase, MatrizRobomat)):
        display(Math(sym.latex(expr)))
    else:
        display(expr)


class MatrizRobomat(sym.MutableDenseMatrix):
    """Matriz simbólica cuya propiedad .T devuelve otra MatrizRobomat."""

    @property
    def T(self):
        return MatrizRobomat(self.transpose())

    def __array__(self, dtype=None, *args, **kwargs):
        """Permite np.array(m) y operaciones NumPy sobre la matriz."""
        return np.array(self.tolist(), dtype=dtype or float)


def _es_simbolico(x):
    return isinstance(x, (sym.Symbol, sym.Expr)) or hasattr(x, 'free_symbols')


def sin(x):
    return sym.sin(x) if _es_simbolico(x) else np.sin(x)


def cos(x):
    return sym.cos(x) if _es_simbolico(x) else np.cos(x)


def tan(x):
    return sym.tan(x) if _es_simbolico(x) else np.tan(x)


pi = np.pi
rad = np.radians
deg = np.degrees


class _CreadorMatriz:
    """M[[...], [...]] -> matriz (numérica o simbólica)."""

    def __getitem__(self, datos):
        if not isinstance(datos, (list, tuple)):
            datos = [datos]
        filas = [fila if isinstance(fila, (list, tuple)) else [fila] for fila in datos]
        plano = [x for fila in filas for x in fila]
        if any(_es_simbolico(x) for x in plano):
            return MatrizRobomat(filas)
        return np.array(filas, dtype=float)


class _CreadorIdentidad:
    """I[4] -> eye(4); I[3, 4] -> eye(3, 4)."""

    def __getitem__(self, dims):
        if isinstance(dims, int):
            return np.eye(dims)
        if isinstance(dims, tuple) and len(dims) == 2:
            return np.eye(dims[0], dims[1])
        raise ValueError('Usa I[n] o I[m, n]')


M = _CreadorMatriz()
I = _CreadorIdentidad()


def var(*nombres):
    """Crea variables simbólicas: var('q1', 'q2', 'L1')."""
    return sym.symbols(' '.join(nombres))


variables_articulares = var  # alias legible


def jacobiano(vector_posicion, variables):
    if not isinstance(vector_posicion, sym.MatrixBase):
        vector_posicion = sym.Matrix(vector_posicion)
    return MatrizRobomat(vector_posicion.jacobian(sym.Matrix(variables)))


def evaluar(expresion, variables, valores):
    if not isinstance(expresion, (sym.MatrixBase, MatrizRobomat)):
        return np.array(expresion, dtype=float)
    sustituciones = list(zip(variables, valores))
    resultado = expresion.subs(sustituciones)
    return np.array(resultado.tolist(), dtype=float)
