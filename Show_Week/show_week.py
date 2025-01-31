import sqlite3
import datetime as dt
import telebot
from Keyboard.keyboards import switch_week_kb
from TOKEN import Token


connection = sqlite3.connect('Groups.db',check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)

# def get_current_date() -> dt.date:
#     return dt.date.today()

def change_week(current_date: dt.date, offset: int) -> dt.date:
    return current_date + dt.timedelta(days=offset * 7)


# def send_current_week_message(chat_id, group_id: int):
def send_current_week_message(chat_id, group_id: int):
    today = dt.date.today()
    start_of_week = today - dt.timedelta(days=today.weekday())
    end_of_week = start_of_week + dt.timedelta(days=6)

    query = ''' 
             SELECT week
             FROM schedule
             WHERE group_id = ? AND date BETWEEN ? AND ?
             '''
    cursor.execute(query, (group_id, start_of_week, end_of_week))
    current_week = cursor.fetchone()


    if current_week:
        bot.send_message(
            chat_id,
            text=f"Текущая неделя:<blockquote>{current_week[0]}</blockquote>",
            parse_mode='HTML',
            reply_markup=switch_week_kb()
        )
    else:
        bot.send_message(
            chat_id,
            text="Не удалось найти текущую неделю в расписании.",
            parse_mode='HTML'
        )
    return current_week if current_week else None