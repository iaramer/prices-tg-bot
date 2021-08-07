import telebot
import requests
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.AsyncTeleBot(TOKEN)

text_messages = {
    'welcome':
        '''
        Hi!
        I am AIAdvisor bot.
        You can ask me about USD/RUB and EUR/RUB currency pairs and BTC/USD, ETH/USD cryptocurrencies.
        Use the following commands: 
        /help - shows help;
        /go - shows prices.
        ''',

    'info':
        '''
        You can ask me about USD/RUB and EUR/RUB currency pairs and BTC/USD, ETH/USD cryptocurrencies.
        Use the following commands: 
        /help - shows help;
        /go - shows prices.
        ''',

    'go':
        'USD/RUB: {:>12}\nEUR/RUB: {:>12}\nBTC/USD: {:>12}\nETH/USD: {:>12}'
}


@bot.message_handler(commands=['start'])
def on_start(message):
    bot.reply_to(message, text_messages['welcome'])


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

    prices = text_messages['go'].format(price_btc, price_eth, price_usd, price_eur)
    bot.send_message(message.chat.id, prices)


@bot.message_handler(func=lambda m: True)
def on_any_message(message):
    if message.text.lower() in ['go', 'currency', 'btc', 'eth', 'rub', 'usd', 'eur']:
        on_go(message)
    elif message.text.lower() in ['info', help]:
        on_info(message)
    else:
        bot.reply_to(message, 'Wooo! Here should be some ML')
        bot.send_message(message.chat.id, 'For now I can answer only fixed set of commands')
        bot.send_message(message.chat.id, text_messages['info'])


def listener(messages):
    for m in messages:
        print(str(m))


bot.set_update_listener(listener)
bot.polling()
