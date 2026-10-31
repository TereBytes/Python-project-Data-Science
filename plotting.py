"""Gráficos: precio de la acción frente a los ingresos trimestrales."""

import pandas as pd

STOCK_CUTOFF = "2021-06-14"
REVENUE_CUTOFF = "2021-04-30"


def filter_by_date(stock_data, revenue_data):
    """Recorta ambas series a las fechas del enunciado (hasta junio de 2021)."""
    stock = stock_data[pd.to_datetime(stock_data["Date"]) <= STOCK_CUTOFF]
    revenue = revenue_data[pd.to_datetime(revenue_data["Date"]) <= REVENUE_CUTOFF]
    return stock, revenue


def make_graph(stock_data, revenue_data, stock, title=None):
    """Dibuja dos gráficos interactivos (Plotly): precio e ingresos.

    Args:
        stock_data: DataFrame con ``Date`` y ``Close``.
        revenue_data: DataFrame con ``Date`` y ``Revenue`` (en millones de $).
        stock: nombre que aparecerá en el título (``"Tesla"``...).
        title: título opcional.

    Returns:
        La figura de Plotly (también se puede mostrar con ``fig.show()``).
    """
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    stock_data, revenue_data = filter_by_date(stock_data, revenue_data)

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Precio histórico de la acción", "Ingresos históricos"),
        vertical_spacing=0.3,
    )
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_data["Date"]),
            y=stock_data["Close"].astype("float"),
            name="Precio de cierre ($)",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_data["Date"]),
            y=revenue_data["Revenue"].astype("float"),
            name="Ingresos (millones $)",
        ),
        row=2,
        col=1,
    )
    fig.update_xaxes(title_text="Fecha", row=2, col=1)
    fig.update_yaxes(title_text="Precio de cierre ($)", row=1, col=1)
    fig.update_yaxes(title_text="Ingresos (millones $)", row=2, col=1)
    fig.update_layout(
        showlegend=False,
        height=900,
        title=title or f"{stock}: precio vs ingresos",
    )
    return fig


def make_graph_png(stock_data, revenue_data, stock, path):
    """Versión estática con matplotlib (útil sin Plotly o para el README)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    stock_data, revenue_data = filter_by_date(stock_data, revenue_data)
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    top.plot(pd.to_datetime(stock_data["Date"]), stock_data["Close"])
    top.set_ylabel("Precio de cierre ($)")
    top.set_title(f"{stock}: precio histórico")
    bottom.plot(pd.to_datetime(revenue_data["Date"]), revenue_data["Revenue"])
    bottom.set_ylabel("Ingresos (millones $)")
    bottom.set_title(f"{stock}: ingresos trimestrales")
    bottom.set_xlabel("Fecha")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path
