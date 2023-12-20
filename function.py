import requests


def analyze_multipliers(stock_data, recommended_values):
    analysis = {}
    for key, (recommended_value, buy_or_sell_logic) in recommended_values.items():
        actual_value = stock_data.get(key)
        if actual_value is not None and actual_value != 0:
            analysis[key] = buy_or_sell_logic(actual_value, recommended_value)
        else:
            analysis[key] = 'No Data'
    return analysis



# Функция для получения данных акции
def get_stock_data(ticker, api_key):
    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols": ticker}
    headers = {'x-api-key': api_key}

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        quote_data = data.get('quoteResponse', {}).get('result', [])
        if quote_data:
            return quote_data[0]  # Возвращает данные первой акции в списке
    return None

# Функция анализа мультипликаторов

def get_last_five_messages(user_id, cursor):
    cursor.execute('''
        SELECT message_text FROM messages
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 5
    ''', (user_id,))
    return cursor.fetchall()