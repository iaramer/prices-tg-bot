import telebot
import requests
import os
from dotenv import load_dotenv

"""
Links:
https://www.toptal.com/python/telegram-bot-tutorial-python
https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples
https://tproger.ru/translations/telegram-bot-create-and-deploy/ - outdated
"""

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.AsyncTeleBot(TOKEN)

text_messages = {
    'start': 'Hi! I am AIAdvisor bot.\nUse /help command to see what I can.\nUse /go command to get prices.',

    'info':
    '''
    You can ask me about USD/RUB and EUR/RUB currency pairs and BTC/USD, ETH/USD cryptocurrencies.\
    \nUse the following commands:\
    \n/help - shows help;\
    \n/go - shows prices.
    ''',

    'go': 'USD/RUB: {:>12}\nEUR/RUB: {:>12}\nBTC/USD: {:>12}\nETH/USD: {:>12}'
}


@bot.message_handler(commands=['start'])
def on_start(message):
    bot.send_message(message.chat.id, text_messages['start'])


@bot.message_handler(commands=['info', 'help'])
def on_info(message):
    bot.reply_to(message, text_messages['info'])


@bot.message_handler(commands=['go'])
def on_go(message):
    response_btc = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    price_btc = "{:,}".format(response_btc.json()['USD'])

    response_eth = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
    price_eth = "{:,}".format(response_eth.json()['USD'])

    response_btc = requests.get('https://www.cbr-xml-daily.ru/latest.js')
    price_usd = "{:,}".format(round(1 / float(response_btc.json()['rates']['USD']), 2))
    price_eur = "{:,}".format(round(1 / float(response_btc.json()['rates']['EUR']), 2))

    prices = text_messages['go'].format(price_usd, price_eur, price_btc, price_eth)
    bot.send_message(message.chat.id, prices)


@bot.message_handler(func=lambda m: True)
def on_any_message(message):
    if message.text.lower() in ['go', 'currency', 'btc', 'eth', 'rub', 'usd', 'eur']:
        on_go(message)
    elif message.text.lower() in ['info', 'help']:
        on_info(message)
    else:
        bot.reply_to(message, 'Wooo! Here should be some ML.\nFor now I can answer only fixed set of commands :(')
        bot.send_message(message.chat.id, text_messages['info'])


def listener(messages):
    for m in messages:
        print(str(m))


bot.set_update_listener(listener)
bot.polling()
