import sqlite3
import datetime as dt
import telebot
import re
from Keyboard.keyboards import choose_group_kb
from TOKEN import Token


connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)
# def register_manual_week(bot):
    # @bot.callback_query_handler(func=lambda message: True)
    # def hanle_manual_week(message):
    #     date_pattern = r'\d{2}\.\d{2}-\d{2}\.\d{2}'
    #     if re.match(date_pattern, message.text):
    #         bot.send_message(message.chat.id, f'Выбери свою группу', reply_markup =choose_group_kb())

