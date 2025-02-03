import sqlite3
import datetime as dt
import telebot
from Keyboard.keyboards import switch_week_kb
from TOKEN import Token

# TODO сделать клаву через реплай меседж текст
connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)


def change_week(offset: int) -> dt.date:
    current_date = dt.date.today()
    print(current_date + dt.timedelta(days= offset *7))
    return current_date + dt.timedelta(days=offset * 7)


def send_current_week_message(today, chat_id, group_id: int):
    start_of_week = today - dt.timedelta(days=today.weekday())
    end_of_week = start_of_week + dt.timedelta(days=6)
    # result = f'{start_of_week}, {end_of_week}'
    # print(result)

    # query_test = '''
    #     SELECT *
    #     FROM schedule
    #     '''
    # cursor.execute(query_test)
    # test = cursor.fetchall()
    # for i in test:
    #     print(i)

    query = '''
             SELECT week, weekday, classroom
             FROM schedule
             WHERE group_id = ? AND date BETWEEN ? AND ?
             '''

    cursor.execute(query, (group_id, start_of_week, end_of_week))
    current_week = cursor.fetchall()

    if current_week:
        bot.send_message(
            chat_id,
            text=f"Текущая неделя:<blockquote>{current_week[0]}</blockquote>",
            parse_mode='HTML',
            reply_markup=switch_week_kb(),

        )
        print(f'current week : {current_week[0]}\n'
              f'{query}')
    else:
        bot.send_message(
            chat_id,
            text="Не удалось найти текущую неделю в расписании.",
            parse_mode='HTML',
            reply_markup=switch_week_kb()
        )
    return current_week if current_week else None, start_of_week, end_of_week

