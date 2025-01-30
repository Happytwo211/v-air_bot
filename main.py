import os
import telebot
import sqlite3
from Commands.start import register_start
from Commands.schedule import register_schedule
from Callback_Data.Callback_Data import register_callback
from Admins import admin_list
from TOKEN import Token


#Подключение БД
db_path = os.path.join(os.getcwd(), 'DB/Groups.db')
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

#Настройки бота и инициализвация
bot = telebot.TeleBot(Token.TOKEN)
admins = admin_list.admin_id

#commands
register_start(bot)
register_schedule(bot)

register_callback(bot)


if __name__ == "__main__":
    bot.polling(none_stop=True)