"""Descarga de precios históricos con la librería ``yfinance``."""

import pandas as pd

TESLA_TICKER = "TSLA"
GME_TICKER = "GME"


def get_stock_data(ticker):
    """Devuelve el histórico completo de un ticker con ``Date`` como columna.

    ``yfinance`` entrega la fecha como índice; ``reset_index`` la convierte en
    columna (pregunta 1 de la tarea) y se retira la zona horaria para poder
    comparar con las fechas de los ingresos.
    """
    import yfinance as yf  # import local: solo hace falta con conexión

    data = yf.Ticker(ticker).history(period="max")
    data = data.reset_index()
    data["Date"] = pd.to_datetime(data["Date"]).dt.tz_localize(None)
    return data


def get_tesla_data():
    """Histórico de Tesla (TSLA)."""
    return get_stock_data(TESLA_TICKER)


def get_gme_data():
    """Histórico de GameStop (GME)."""
    return get_stock_data(GME_TICKER)
