import unittest
from function import analyze_multipliers


# Mock function for buy or sell logic
def mock_buy_or_sell_logic(actual, recommended):
    if actual > recommended:
        return 'Sell'
    elif actual < recommended:
        return 'Buy'
    else:
        return 'Hold'


# analyze_multipliers function definition

# Test class for analyze_multipliers
class TestAnalyzeMultipliers(unittest.TestCase):

    def test_empty_data(self):
        self.assertEqual(analyze_multipliers({}, {}), {})

    def test_single_multiplier_correct_data(self):
        stock_data = {'PE': 10}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Buy'})

    def test_single_multiplier_sell(self):
        stock_data = {'PE': 20}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Sell'})

    def test_single_multiplier_hold(self):
        stock_data = {'PE': 15}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Hold'})

    def test_single_multiplier_no_data(self):
        stock_data = {}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'No Data'})

    def test_multiple_multipliers(self):
        stock_data = {'PE': 10, 'PB': 2}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic), 'PB': (3, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Buy', 'PB': 'Buy'})

    def test_negative_values_in_stock_data(self):
        stock_data = {'PE': -10}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Buy'})

    def test_negative_recommended_values(self):
        stock_data = {'PE': 10}
        recommended_values = {'PE': (-5, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Sell'})

    def test_large_values_in_stock_data(self):
        stock_data = {'PE': 100000}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Sell'})



    def test_mixed_data_some_no_data(self):
        stock_data = {'PE': 10, 'PB': None}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic), 'PB': (3, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Buy', 'PB': 'No Data'})

    def test_floating_point_stock_data(self):
        stock_data = {'PE': 10.5}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Buy'})

    def test_floating_point_recommended_values(self):
        stock_data = {'PE': 10}
        recommended_values = {'PE': (10.5, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Buy'})

    def test_small_non_zero_values_in_stock_data(self):
        stock_data = {'PE': 0.001}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Buy'})

    def test_custom_logic_function(self):
        def custom_logic(actual, recommended):
            return 'Custom'
        stock_data = {'PE': 10}
        recommended_values = {'PE': (15, custom_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'Custom'})

    def test_invalid_key_in_stock_data(self):
        stock_data = {'InvalidKey': 10}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'No Data'})

    def test_invalid_key_in_recommended_values(self):
        stock_data = {'PE': 10}
        recommended_values = {'InvalidKey': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'InvalidKey': 'No Data'})

    def test_empty_stock_data_with_values_in_recommended_values(self):
        stock_data = {}
        recommended_values = {'PE': (15, mock_buy_or_sell_logic)}
        self.assertEqual(analyze_multipliers(stock_data, recommended_values), {'PE': 'No Data'})



if __name__ == '__main__':
    unittest.main()
