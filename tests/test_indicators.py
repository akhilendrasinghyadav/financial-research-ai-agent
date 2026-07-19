import unittest

import pandas as pd

from src.indicators import add_indicators, calculate_rsi
from src.metrics import performance_summary


class IndicatorTests(unittest.TestCase):
    def test_add_indicators_adds_expected_columns(self):
        data = pd.DataFrame(
            {
                "Open": range(1, 61),
                "High": range(2, 62),
                "Low": range(0, 60),
                "Close": range(1, 61),
                "Volume": [1000] * 60,
            }
        )

        enriched = add_indicators(data)

        for column in ["SMA20", "SMA50", "RSI", "MACD", "MACD_SIGNAL", "BB_UPPER", "BB_LOWER"]:
            self.assertIn(column, enriched.columns)

    def test_rsi_stays_in_expected_range(self):
        close = pd.Series([100, 101, 102, 101, 103, 104, 105, 103, 102, 104, 106, 108, 107, 109, 110])
        rsi = calculate_rsi(close).dropna()

        self.assertTrue(((rsi >= 0) & (rsi <= 100)).all())

    def test_performance_summary_has_core_metrics(self):
        data = pd.DataFrame({"Close": [100, 105, 102, 110]})
        summary = performance_summary(data)

        self.assertGreater(summary["total_return"], 0)
        self.assertIn("max_drawdown", summary)


if __name__ == "__main__":
    unittest.main()
