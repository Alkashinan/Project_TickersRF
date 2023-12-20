def analyze_multipliers(stock_data, recommended_values):
    analysis = {}
    for key, (recommended_value, buy_or_sell_logic) in recommended_values.items():
        actual_value = stock_data.get(key)
        if actual_value is not None and actual_value != 0:
            analysis[key] = buy_or_sell_logic(actual_value, recommended_value)
        else:
            analysis[key] = 'No Data'
    return analysis