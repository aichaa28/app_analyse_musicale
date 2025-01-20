# tests/test_dashboard.py
import unittest
import pandas as pd
from dashboard import get_top_artists

class TestDashboard(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.df = pd.DataFrame({
            'artists': ['Artist A', 'Artist B', 'Artist C', 'Artist A'],
            'popularity': [80, 90, 70, 85]
        })

    def test_get_top_artists(self):
        # Test the function with valid input
        result = get_top_artists(self.df, 2)
        expected = pd.Series([87.5, 90], index=['Artist A', 'Artist B'])
        pd.testing.assert_series_equal(result, expected)

    def test_missing_columns(self):
        # Test the function with missing columns
        with self.assertRaises(ValueError):
            get_top_artists(self.df[['popularity']], 2)

    def test_empty_dataframe(self):
        # Test the function with an empty DataFrame
        empty_df = pd.DataFrame(columns=['artists', 'popularity'])
        result = get_top_artists(empty_df, 2)
        self.assertTrue(result.empty)

if __name__ == "__main__":
    unittest.main()
