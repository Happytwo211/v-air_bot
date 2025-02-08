import sqlite3
import datetime as dt
import telebot
from Keyboard.tutor_kb import show_tutor_kb_buttons, show_tutor_kb
from TOKEN import Token

connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)

def register_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['tutor_miit', 'tutor_1273'])
    def send_current_week_message(call):
        chat_id = call.message.chat.id
        date = dt.date.today()

        query = '''
                                      SELECT student_name, date, attendance 
                                      FROM tutor
                                      WHERE group_id = ? and date = ?
                                      '''

        if call.data == 'tutor_miit':

            group_id = 1

            cursor.execute(query, (group_id, date))
            group_tutor_data = cursor.fetchall()
            bot.send_message(chat_id, f'Участники группы миит')

            for data in group_tutor_data:
                bot.send_message(chat_id,f'{data}', )

            bot.send_message(chat_id, f'Выбери функционал', reply_markup = show_tutor_kb())

        elif call.data == 'tutor_1273':

            group_id = 2
            cursor.execute(query, (group_id, date))
            group_tutor_data = cursor.fetchall()
            bot.send_message(chat_id, f'Участники группы 1273')

            for data in group_tutor_data:
                bot.send_message(chat_id, f'{data}')

            bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())

        else:
            bot.send_message(chat_id, f'Произошла ошибочка')

        @bot.callback_query_handler(func=lambda call: call.data in ['attendance', 'materials'])
        def send_current_week_message(call):
            chat_id = call.message.chat.id
            if call.data == 'attendance':
                bot.send_message(chat_id,f'zbs')

            elif call.data == 'materials':
                bot.send_message(chat_id, f'zbs')

            else:
                bot.send_message(chat_id, f'huio')