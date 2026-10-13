# -*- coding: utf-8 -*-
"""
tools/visualizar.py — Presentación: gráficas interactivas (plotly) y tablas.

Vive FUERA del motor (igual que en U2_T3B): no forma parte del sistema de
calificación, así que no hay nada que esconder — puedes leer estas funciones y
reutilizarlas en tus propios cuadernos.

Las gráficas son INTERACTIVAS (plotly):

  * zoom con la rueda y arrastre;
  * SELECCIÓN de puntos con la caja (`select2d`) y el lazo (`lasso2d`);
  * valores al pasar el cursor;
  * DESCARGA de la imagen (botón de cámara → PNG) y exportación a HTML.

El cuaderno las usa así:

    import visualizar
    visualizar.graficar_boxplot(RES).show(config=visualizar.config_plotly())
"""
import numpy as np

COLORES = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']


def config_plotly():
    """Configuración común: zoom con rueda, selección (caja/lazo) y descarga PNG."""
    return {
        'scrollZoom': True,
        'displaylogo': False,
        'modeBarButtonsToAdd': ['select2d', 'lasso2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'grafica_u2t4',
            'height': 900,
            'width': 1400,
            'scale': 2,
        },
    }


def guardar_html(fig, nombre):
    """Guarda la figura como HTML autocontenido (para entregar/adjuntar)."""
    ruta = nombre + '.html'
    fig.write_html(ruta, include_plotlyjs='cdn', config=config_plotly())
    print('💾 Gráfica guardada en %s' % ruta)
    return ruta


def graficar_histograma(RES):
    """Histograma de iteraciones + tasa de divergencia (plotly)."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    mets = list(RES['metodos'].keys())
    fig = make_subplots(rows=1, cols=2, subplot_titles=(
        'Distribución de iteraciones por método', 'Tasa de divergencia (% sin acertar)'))

    for i, m in enumerate(mets):
        it = RES['metodos'][m]['n_iter']
        it = it[np.isfinite(it)]
        fig.add_trace(go.Histogram(x=it, name=m, opacity=0.55,
                                   marker_color=COLORES[i % len(COLORES)]),
                      row=1, col=1)

    div = [100 * RES['metodos'][m]['pct_diverge'] for m in mets]
    fig.add_trace(go.Bar(x=mets, y=div,
                         marker_color=[COLORES[i % len(COLORES)] for i in range(len(mets))]),
                  row=1, col=2)

    fig.update_layout(barmode='overlay', bargap=0.1, template='plotly_white',
                      height=450, legend=dict(font=dict(size=10)))
    fig.update_xaxes(title_text='iteraciones', row=1, col=1)
    fig.update_yaxes(title_text='frecuencia', row=1, col=1)
    fig.update_yaxes(title_text='%', row=1, col=2)
    return fig


def graficar_boxplot(RES):
    """Box plot comparativo de iteraciones (plotly, con puntos)."""
    import plotly.graph_objects as go

    mets = list(RES['metodos'].keys())
    fig = go.Figure()
    for i, m in enumerate(mets):
        it = RES['metodos'][m]['n_iter'][np.isfinite(RES['metodos'][m]['n_iter'])]
        fig.add_trace(go.Box(y=it, name=m, boxpoints='suspectedoutliers',
                             marker_color=COLORES[i % len(COLORES)],
                             line_color=COLORES[i % len(COLORES)]))
    fig.update_layout(title='Box plot de iteraciones por método (tema %s)' % RES.get('tema', ''),
                      yaxis_title='iteraciones', template='plotly_white', height=480)
    return fig


def graficar_distribucion(RES, modelo=None, es_sistema=False):
    """Distribución de la respuesta física ante la incertidumbre (plotly)."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    ref = RES['raiz_ref']
    if es_sistema:
        nvar = ref.shape[1]
        nombres = modelo['vars'] if modelo else ['x%d' % j for j in range(nvar)]
        fig = make_subplots(rows=1, cols=nvar, subplot_titles=[
            'Distribución de %s' % nombres[j] for j in range(nvar)])
        for j in range(nvar):
            col = ref[np.isfinite(ref[:, j]), j]
            fig.add_trace(go.Histogram(x=col, marker_color='teal', opacity=0.75),
                          row=1, col=j + 1)
            fig.update_xaxes(title_text=nombres[j], row=1, col=j + 1)
    else:
        rr = ref[np.isfinite(ref)]
        nombre = modelo['vars'][0] if modelo else 'x'
        fig = make_subplots(rows=1, cols=2, subplot_titles=(
            'Distribución de la raíz física (%s)' % nombre, 'Dispersión de la respuesta física'))
        fig.add_trace(go.Histogram(x=rr, marker_color='teal', opacity=0.75), row=1, col=1)
        fig.add_trace(go.Box(x=rr, marker_color='teal'), row=1, col=2)
        fig.update_xaxes(title_text=nombre, row=1, col=1)
    fig.update_layout(template='plotly_white', height=450, showlegend=False)
    return fig


def graficar_funcion(f, xs, raiz=None, nombre_var='x', titulo=''):
    """Gráfica de f(x) para aislar la raíz (plotly, con la raíz marcada)."""
    import plotly.graph_objects as go

    ys = np.asarray(f(xs), dtype=float)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(%s)' % nombre_var,
                             line=dict(color='#1f77b4', width=2)))
    fig.add_hline(y=0, line=dict(color='gray', width=1, dash='dot'))
    if raiz is not None and np.isfinite(raiz):
        fig.add_vline(x=raiz, line=dict(color='crimson', width=2, dash='dash'),
                      annotation_text='raíz ≈ %.6g' % raiz)
    fig.update_layout(title=titulo, xaxis_title=nombre_var, yaxis_title='f',
                      template='plotly_white', height=420)
    return fig


def graficar_todo(RES, modelo=None, es_sistema=False, descargar=False):
    """Muestra TODAS las gráficas interactivas y devuelve la lista de figuras."""
    figuras = [graficar_histograma(RES), graficar_boxplot(RES),
               graficar_distribucion(RES, modelo=modelo, es_sistema=es_sistema)]

    for i, fig in enumerate(figuras):
        fig.show(config=config_plotly())
        if descargar:
            guardar_html(fig, 'u2t4_grafica_%d' % (i + 1))
    return figuras


def tabla_resultados(RES):
    """HTML de la tabla resumen del Monte Carlo (para el informe)."""
    from IPython.display import HTML

    filas = []
    for m, d in RES['metodos'].items():
        filas.append(
            '<tr><td><b>%s</b></td><td>%s</td><td style="text-align:right">%.1f%%</td>'
            '<td style="text-align:right">%.1f%%</td><td style="text-align:right">%.0f</td>'
            '<td style="text-align:right">%.1f</td><td style="text-align:right">%.1e</td></tr>'
            % (m, d['familia'], 100 * d['pct_exito'], 100 * d['pct_diverge'],
               np.nanmedian(d['n_iter']), np.nanmean(d['n_iter']),
               np.nanmedian(d['err_ref'])))
    html = (
        '<table style="border-collapse:collapse;font-size:13px">'
        '<tr style="background:#eee"><th>Método</th><th>Familia</th><th>% éxito</th>'
        '<th>% divergencia</th><th>mediana iter</th><th>media iter</th><th>mediana err</th></tr>'
        + ''.join(filas) + '</table>')
    return HTML(html)
