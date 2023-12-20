import requests
from bs4 import BeautifulSoup


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


url = 'https://investfunds.ru/stocks-leaders/'
stock_leaders = scrape_stock_leaders(url)
for stock in stock_leaders:
    print(stock)
