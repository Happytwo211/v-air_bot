import sqlite3
import datetime as dt
import telebot
from Keyboard.keyboards import switch_week_kb
from TOKEN import Token

# TODO сделать клаву через реплай меседж текст
# todo либо удаление
connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)


def register_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['classroom'])
    def send_tutor_kb(call):
        chat_id = call.message.chat.id

        query = '''
                     SELECT *
                     FROM tutor

                     '''

        cursor.execute(query)
        current_week = cursor.fetchall()

        if current_week:

            message_text = "Занятия на текущей неделе:\n\n"
            for item in current_week:
                message_text += f"<blockquote>{item}</blockquote>\n"

            bot.send_message(
                chat_id,
                text=message_text,
                parse_mode='HTML',
                # reply_markup=switch_week_kb(),
            )

        else:
            bot.send_message(
                chat_id,
                text="Ошибка.",
                parse_mode='HTML',
                # reply_markup=switch_week_kb()
            )
        return current_week if current_week else None