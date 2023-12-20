import telebot
from telebot import types
import config
import requests



bot = telebot.TeleBot(config.bot_token)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    bot.send_message(message.from_user.id, "1")
    bot.send_message(message.from_user.id, "1\n")
    bot.send_message(message.from_user.id, "2")
    f = "1" +"\n"+ "2"
    bot.send_message(message.from_user.id, f)
bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть