from Commands.start import register_start
from Admins import admin_list
from TOKEN import Token
from telebot import types
import os
import telebot
import sqlite3

#Подключение БД
db_path = os.path.join(os.getcwd(), 'DB/Groups.db')
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

#Настройки бота и инициализвация
bot = telebot.TeleBot(Token.TOKEN)
admins = admin_list.admin_id

register_start(bot)


if __name__ == "__main__":
    bot.polling(none_stop=True)