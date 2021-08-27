from django.test import TestCase
from .views import get_stock_data

# Create your tests here.

"""
To run tests: 'python manage.py test projects'
"""


class TestStockData(TestCase):
    def test_NasdaqCompanyName(self):
        """
        Check to see if Nasdaq API outputs correct Company name for a given ticker
        """
        self.assertEqual(
            "Alphabet Inc. - Class C Capital Stock",
            get_stock_data("GOOG")["stock_obj"]["stock_name_long"],
        )

    def test_YahooClose(self):
        """
        Check to see if Yahoo API outputs floats close prices
        """
        self.assertEqual(
            True, isinstance(get_stock_data("GOOG")["stock_obj"]["close"], float)
        )

    def test_YahooOpen(self):
        """
        Check to see if Yahoo API outputs floats open prices
        """
        self.assertEqual(
            True, isinstance(get_stock_data("GOOG")["stock_obj"]["open"], float)
        )

    def test_YahooHigh(self):
        """
        Check to see if Yahoo API outputs floats high prices
        """
        self.assertEqual(
            True, isinstance(get_stock_data("GOOG")["stock_obj"]["high"], float)
        )

    def test_YahooLow(self):
        """
        Check to see if Yahoo API outputs floats for low prices
        """
        self.assertEqual(
            True, isinstance(get_stock_data("GOOG")["stock_obj"]["low"], float)
        )

    def test_YahooVolume(self):
        """
        Check to see if Yahoo API outputs integers for volume
        """
        self.assertEqual(
            True, isinstance(get_stock_data("GOOG")["stock_obj"]["volume"], int)
        )


if __name__ == "__main__":
    unittest.main()
