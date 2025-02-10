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


def change_week(offset: int) -> dt.date:
    current_date = dt.date.today()
    print(f'change week:')
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
             SELECT week, weekday, start_time,
             end_time, classroom, location
             FROM schedule
             WHERE group_id = ? AND date BETWEEN ? AND ?
             '''

    cursor.execute(query, (group_id, start_of_week, end_of_week))
    current_week = cursor.fetchall()
    # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
    #                               reply_markup=show_student_kb())

    # bot.edit_message_text(new_text,
    #                       chat_id=call.message.chat.id,
    #                       message_id=call.message.message_id,
    #                       reply_markup=call.message.reply_markup)

    if current_week:

        bot.send_message(
            chat_id,
            text=f"Занятия на текущей неделе: "
                 f"Неделя:<blockquote>{current_week[0][0]}</blockquote>\n"
                 f"День Недели: <blockquote>{current_week[0][1]}</blockquote>\n"
                 f"Начало занятия: <blockquote>{current_week[0][2]}</blockquote>\n"
                 f"Конец занятия: <blockquote>{current_week[0][3]}</blockquote>\n"
                 f"Аудитория: <blockquote>{current_week[0][4]}</blockquote>\n"
                 f"Локация: <blockquote>{current_week[0][5]}</blockquote>\n",

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

