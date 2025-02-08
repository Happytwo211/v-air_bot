import sqlite3
import datetime as dt
import telebot
from Keyboard.tutor_kb import show_tutor_kb_buttons
from TOKEN import Token

connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)

def register_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['tutor_miit', 'tutor_1273'])
    def send_current_week_message(call):
        chat_id = call.message.chat.id

        query = '''
                                      SELECT *
                                      FROM tutor
                                      WHERE group_id = ?
                                      '''

        if call.data == 'tutor_miit':

            group_id = 1
            cursor.execute(query, (group_id,))
            group_tutor_data = cursor.fetchall()

            bot.send_message(chat_id, f'ты выбрал группу МИИТ\n'
                                      f'{group_tutor_data}',
                             reply_markup=show_tutor_kb_buttons())
            return group_id

        elif call.data == 'tutor_1273':

            group_id = 2
            cursor.execute(query, (group_id,))
            group_tutor_data = cursor.fetchall()
            bot.send_message(chat_id, f' Ты выбрал группу 1273'
                                      f'{group_tutor_data}',
                             reply_markup=show_tutor_kb_buttons())

            return group_id

        else:
            bot.send_message(chat_id, f'Произошла ошибочка',
                             reply_markup=show_tutor_kb_buttons())

