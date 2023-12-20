import requests

def find_international_ticker(russian_ticker):
    api_key = 'eFuPGSs4sz2cBp0Bg9gcP6h0rzO3zI645vQU538B'
    url = f'https://api.financeapi.net/your-endpoint?apikey={api_key}&ticker={russian_ticker}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Допустим, международный тикер находится в 'international_ticker'
        return data.get('international_ticker')
    else:
        return "Ошибка: Не удалось получить данные"

# Пример использования
russian_ticker = 'MVID'
international_ticker = find_international_ticker(russian_ticker)
print(f'Международный тикер для {russian_ticker}: {international_ticker}')
