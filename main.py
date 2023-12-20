import telebot
from telebot import types
import config
import requests
from bs4 import BeautifulSoup
import sqlite3
from function import *

bot = telebot.TeleBot(config.bot_token)

# Примеры рекомендованных значений и логики покупки/продажи
recommended_values = {
    'trailingPE': (15, lambda x, y: 'Buy' if x < y else 'Sell'),
    'priceToBook': (1.5, lambda x, y: 'Buy' if x < y else 'Sell'),
    'regularMarketChangePercent': (0.02, lambda x, y: 'Buy' if x > y else 'Sell'),
    'fiftyTwoWeekHighChangePercent': (-0.1, lambda x, y: 'Buy' if x < y else 'Sell'),
    'fiftyTwoWeekLowChangePercent': (0.1, lambda x, y: 'Buy' if x > y else 'Sell'),
    'epsTrailingTwelveMonths': (1, lambda x, y: 'Buy' if x > y else 'Sell'),
    'forwardPE': (10, lambda x, y: 'Buy' if x < y else 'Sell'),
    'marketCap': (1000000000, lambda x, y: 'Buy' if x > y else 'Sell'),
    'averageDailyVolume3Month': (500000, lambda x, y: 'Buy' if x > y else 'Sell'),
    'averageDailyVolume10Day': (200000, lambda x, y: 'Buy' if x > y else 'Sell'),
    'fiftyDayAverage': (200, lambda x, y: 'Buy' if x > y else 'Sell'),
    'twoHundredDayAverage': (180, lambda x, y: 'Buy' if x > y else 'Sell'),
    'fiftyDayAverageChange': (-10, lambda x, y: 'Buy' if x > y else 'Sell'),
    'twoHundredDayAverageChange': (-20, lambda x, y: 'Buy' if x > y else 'Sell'),
    'fiftyDayAverageChangePercent': (-0.05, lambda x, y: 'Buy' if x > y else 'Sell'),
    'twoHundredDayAverageChangePercent': (-0.1, lambda x, y: 'Buy' if x > y else 'Sell'),
    'bidSize': (1000, lambda x, y: 'Buy' if x > y else 'Sell'),
    'askSize': (1000, lambda x, y: 'Buy' if x < y else 'Sell'),
    # Добавить другие мультипликаторы при необходимости
}
friendly_names = {
    'trailingPE': 'P/E Ratio (Trailing)',
    'priceToBook': 'Price to Book Ratio',
    'regularMarketChangePercent': 'Market Change Percent (Regular Market)',
    'fiftyTwoWeekHighChange': '52-Week High Change',
    'fiftyTwoWeekLowChange': '52-Week Low Change',
    'regularMarketVolume': 'Regular Market Volume',
    'bookValue': 'Book Value per Share',
    'sharesOutstanding': 'Shares Outstanding',
    'averageDailyVolume3Month': 'Average Daily Volume (3 Month)',
    'averageDailyVolume10Day': 'Average Daily Volume (10 Day)',
    'fiftyDayAverage': '50-Day Moving Average',
    'twoHundredDayAverage': '200-Day Moving Average',
    'fiftyDayAverageChange': '50-Day Average Change',
    'twoHundredDayAverageChange': '200-Day Average Change',
    'fiftyDayAverageChangePercent': '50-Day Average Change Percent',
    'twoHundredDayAverageChangePercent': '200-Day Average Change Percent',
    'bidSize': 'Bid Size',
    'askSize': 'Ask Size',
    # Добавьте другие мультипликаторы по аналогии
}


def scrape_stock_leaders(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим элементы с данными о лидерах роста и падения
    leaders = soup.find_all('ul', {'class': ['leader_up', 'leader_down']})

    stock_data = []

    for leader in leaders:
        stocks = leader.find_all('li')
        for stock in stocks:
            percent = stock.find('span', {'class': 'percent'}).text
            name = stock.find('a').text
            link = stock.find('a')['href']
            stock_data.append({'name': name, 'percent': percent, 'link': 'https://investfunds.ru' + link})

    return stock_data

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Топ акций по росту и падению")
    btn2 = types.KeyboardButton("История поиска")
    markup.add(btn1)

    markup.add(btn2)
    bot.send_message(message.from_user.id, "Приветвую! Для начала работы бота введите тикет акции, которой вы интересуетесь. ", reply_markup=markup)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Топ акций по росту и падению")
    btn2 = types.KeyboardButton("История поиска")
    markup.add(btn1)
    markup.add(btn2)
    if message.text == "Топ акций по росту и падению":


        url = 'https://investfunds.ru/stocks-leaders/'
        stock_leaders = scrape_stock_leaders(url)
        a = []
        for stock in stock_leaders:
            a.append(stock["name"] + " " +  stock["percent"])
        bot.send_message(message.from_user.id, "Топ 5 акций по росту:\n" + str(a[0]) + '\n' + str(a[1]) + '\n' + str(a[2]) + '\n' + str(a[3]) + '\n' + str(a[4]) + "\n" + "Топ 5 акций по падению:\n" + str(a[5]) + '\n' + str(a[6]) + '\n' + str(a[7]) + '\n' + str(a[8]) + '\n' + str(a[9]))
    elif message.text == "История поиска":
        conn = sqlite3.connect('user_messages.db')

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()



        # Функция для получения последних 5 сообщений пользователя



        # Получение последних 5 сообщений для user1
        last_five_messages = get_last_five_messages(str(message.from_user.id), cursor)
        bot.send_message(message.from_user.id, "Ваши полследние 5 запросов:")
        for messagess in last_five_messages:
            bot.send_message(message.from_user.id, messagess[0])
        cursor.close()
        conn.close()


    else:
        api_key = "CFFHiFbLwF6OnIzEhU1lE2LgkiWTkEYe9wuOKBwK"  # Замените на ваш ключ API
        ticker = message.text
        stock_data = get_stock_data(ticker, api_key)
        text = ""
        b = 0
        s = 0
        itog = ''
        if stock_data:
            analysis = analyze_multipliers(stock_data, recommended_values)
            text += f"Цена акций: {stock_data.get('regularMarketPrice')} {stock_data.get('currency')}\n"
            for key, recommendation in analysis.items():
                if recommendation == 'Buy':
                    b += 1
                elif recommendation == 'Sell':
                    s += 1
                if recommendation != 'No Data':
                    friendly_name = friendly_names.get(key, key)
                    text += f"{friendly_name}: {stock_data.get(key)}\n"
            if b > s :
                itog = "После глубокого аннализа акции мы рекомндуем приобрести акцию"
            elif b < s :
                itog = "После глубокого аннализа акции мы рекомндуем воздержаться от приобретения акции"
            else:
                itog = "После глубокого аннализа акции мы рекомндуем приобрести акцию"


            bot.send_message(message.from_user.id, text + itog)
        # Подключение к базе данных SQLite (будет создан новый файл базы данных, если он не существует)
            conn = sqlite3.connect('user_messages.db')

            # Создание курсора для выполнения SQL-запросов
            cursor = conn.cursor()

            # Создание таблицы для хранения сообщений
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    message_text TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Функция для вставки нового сообщения
            def insert_message():
                cursor.execute('''
                    INSERT INTO messages (user_id, message_text)
                    VALUES (?, ?)
                ''', (str(message.from_user.id), ticker))
                conn.commit()

            # Пример вставки сообщений
            insert_message()



            # Закрытие соединения с базой данных
            cursor.close()
            conn.close()

        else:

            bot.send_message(message.from_user.id,"Ошибка при получении данных акции.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Топ акций по росту и падению")
    btn2 = types.KeyboardButton("История поиска")
    markup.add(btn1)
    markup.add(btn2)


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть