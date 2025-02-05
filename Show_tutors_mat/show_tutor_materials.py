import sqlite3
import datetime as dt
import telebot
from Keyboard.keyboards import switch_week_kb
from TOKEN import Token

# TODO сделать клаву через реплай меседж текст
#todo либо удаление
connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)

def register_tutor(bot):
        @bot.callback_query_handler(func=lambda call: call.data in ['classroom'])
        def send_tutor_kb(call):
            chat_id = call.message.chat.id

            query = '''
                     SELECT *
                     FROM tutor_test
            
                     '''
            # if group_id == 1:
            #     group_id = 'РУТ МИИТ'
            #     return group_id
            # if group_id == 2:
            #     group_id = '1273'
            #     return group_id

            current_week = cursor.fetchone()
            print(current_week)

            if current_week:

                bot.send_message(
                    chat_id,
                    text=f"Занятия на текущей неделе: "
                         f"ФИО:<blockquote>{current_week[0][0]}</blockquote>\n"
                         f"Дата: <blockquote>{current_week[0][1]}</blockquote>\n"
                         f"Группа: <blockquote>{current_week[0][2]}</blockquote>\n",

                    parse_mode='HTML',
                    # reply_markup=switch_week_kb(),
                )

                print(f'current week : {current_week[0]}\n'
                      f'{query}')


            else:
                bot.send_message(
                    chat_id,
                    text="Ошибка.",
                    parse_mode='HTML',
                    # reply_markup=switch_week_kb()
                )
            return current_week if current_week else None

