import yfinance as yf


def find_ticker(company_name):
    try:
        # Используем параметр locale для поддержки русского языка
        stock_info = yf.Ticker(company_name)

        # Получаем биржевой тикер (symbol)
        ticker = stock_info.info['symbol']

        return ticker
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


# Пример использования
company_name = "Магнит"  # Замените на название нужной русской компании
ticker = find_ticker(company_name)

if ticker:
    print(f"Биржевой тикер для {company_name}: {ticker}")
else:
    print(f"Не удалось найти биржевой тикер для {company_name}")