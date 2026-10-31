"""Extracción de ingresos trimestrales mediante web scraping.

Se usa ``requests`` para descargar el HTML y ``BeautifulSoup`` para localizar
la tabla correcta; después ``pandas`` la convierte en un DataFrame.
"""

from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

# URLs de los HTML del laboratorio de IBM (Skills Network). Si el curso las
# cambia, basta con editar estas dos constantes o pasar otra URL a la función.
BASE_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/"
)
TESLA_REVENUE_URL = BASE_URL + "revenue.htm"
GME_REVENUE_URL = BASE_URL + "stock.html"

# Analizadores válidos de BeautifulSoup (pregunta 2 de la tarea).
VALID_PARSERS = ("html.parser", "lxml", "html5lib")


def download_html(url, timeout=20):
    """Descarga una página y devuelve su HTML como texto."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def clean_revenue(frame):
    """Limpia la columna ``Revenue`` y convierte ``Date`` a ``datetime``.

    - Quita los símbolos ``$`` y las comas (pregunta 4 de la tarea).
    - Elimina filas vacías.
    - Convierte ``Date`` a fecha real (pregunta 3 de la tarea).
    """
    frame = frame.copy().dropna(subset=["Revenue"])
    frame["Revenue"] = (
        frame["Revenue"].astype(str).str.replace(r"[,$]", "", regex=True).str.strip()
    )
    frame = frame[frame["Revenue"] != ""]
    frame["Date"] = pd.to_datetime(frame["Date"])
    frame["Revenue"] = pd.to_numeric(frame["Revenue"])
    return frame.reset_index(drop=True)


def parse_revenue_table(html, table_title, parser="html.parser"):
    """Extrae la tabla cuyo texto contiene ``table_title``.

    Args:
        html: código HTML completo de la página.
        table_title: texto que identifica la tabla, p. ej.
            ``"Tesla Quarterly Revenue"``.
        parser: analizador de BeautifulSoup (``html.parser``, ``lxml``...).

    Returns:
        DataFrame con las columnas ``Date`` y ``Revenue`` ya limpias.
    """
    if parser not in VALID_PARSERS:
        raise ValueError(f"Analizador no válido: {parser}")

    soup = BeautifulSoup(html, parser)
    for table in soup.find_all("table"):
        if table_title.lower() in table.get_text(" ").lower():
            frame = pd.read_html(StringIO(str(table)))[0]
            frame = frame.iloc[:, :2]
            frame.columns = ["Date", "Revenue"]
            return clean_revenue(frame)

    raise ValueError(f"No se encontró ninguna tabla con '{table_title}'")


def get_tesla_revenue(url=TESLA_REVENUE_URL):
    """Ingresos trimestrales de Tesla."""
    return parse_revenue_table(download_html(url), "Tesla Quarterly Revenue")


def get_gme_revenue(url=GME_REVENUE_URL):
    """Ingresos trimestrales de GameStop."""
    return parse_revenue_table(download_html(url), "GameStop Quarterly Revenue")
