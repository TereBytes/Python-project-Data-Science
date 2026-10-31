"""Tests del scraping con HTML local (sin red)."""

from pathlib import Path
import unittest

import pandas as pd

from stock_revenue.scraping import clean_revenue, parse_revenue_table
from stock_revenue.plotting import filter_by_date, make_graph_png

FIXTURE = Path(__file__).parent / "fixtures" / "sample_revenue.html"


class TestScraping(unittest.TestCase):
    """Comprueba extracción y limpieza de la tabla de ingresos."""

    def setUp(self):
        self.html = FIXTURE.read_text(encoding="utf-8")

    def test_picks_quarterly_table_not_annual(self):
        frame = parse_revenue_table(self.html, "Tesla Quarterly Revenue")
        self.assertEqual(len(frame), 4)  # la fila vacía se elimina

    def test_symbols_removed_and_numeric(self):
        frame = parse_revenue_table(self.html, "Tesla Quarterly Revenue")
        self.assertEqual(frame["Revenue"].iloc[0], 10389)
        self.assertTrue(pd.api.types.is_numeric_dtype(frame["Revenue"]))

    def test_date_is_datetime(self):
        frame = parse_revenue_table(self.html, "Tesla Quarterly Revenue")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(frame["Date"]))

    def test_lxml_parser_gives_same_result(self):
        a = parse_revenue_table(self.html, "Tesla Quarterly Revenue", "html.parser")
        b = parse_revenue_table(self.html, "Tesla Quarterly Revenue", "lxml")
        pd.testing.assert_frame_equal(a, b)

    def test_unknown_table_raises(self):
        with self.assertRaises(ValueError):
            parse_revenue_table(self.html, "Nope Revenue")

    def test_invalid_parser_raises(self):
        with self.assertRaises(ValueError):
            parse_revenue_table(self.html, "Tesla Quarterly Revenue", "xml-fake")

    def test_clean_revenue_handles_dollars_and_commas(self):
        raw = pd.DataFrame({"Date": ["2020-01-01"], "Revenue": ["$1,234"]})
        self.assertEqual(clean_revenue(raw)["Revenue"].iloc[0], 1234)


class TestPlotting(unittest.TestCase):
    """Comprueba el recorte de fechas y el gráfico estático."""

    def setUp(self):
        self.stock = pd.DataFrame(
            {"Date": pd.to_datetime(["2021-06-01", "2021-07-01"]), "Close": [1.0, 2.0]}
        )
        self.revenue = pd.DataFrame(
            {"Date": pd.to_datetime(["2021-03-31", "2021-06-30"]), "Revenue": [5, 6]}
        )

    def test_filter_by_date_cuts_after_cutoff(self):
        stock, revenue = filter_by_date(self.stock, self.revenue)
        self.assertEqual(len(stock), 1)
        self.assertEqual(len(revenue), 1)

    def test_png_is_created(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            out = make_graph_png(self.stock, self.revenue, "Demo", Path(tmp) / "g.png")
            self.assertTrue(Path(out).stat().st_size > 1000)


if __name__ == "__main__":
    unittest.main()
