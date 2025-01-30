import sqlite3
import datetime as dt
import telebot
import Keyboard.keyboards
from TOKEN import Token
from typing import Optional


connection = sqlite3.connect('Groups.db',check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)

def get_current_date() -> dt.date:
    return dt.date.today()


def change_week(current_date: dt.date, offset: int) -> dt.date:
    return current_date + dt.timedelta(days=offset * 7)


def get_current_week(group_id: str) -> Optional[str]:
    today = get_current_date()
    start_of_week = today - dt.timedelta(days=today.weekday())
    end_of_week = start_of_week + dt.timedelta(days=6)

    query = '''
             SELECT week
             FROM schedule 
             WHERE group_id = ? AND date BETWEEN ? AND ?
             '''
    cursor.execute(query, (group_id, start_of_week, end_of_week))
    current_week = cursor.fetchone()

    return current_week[0] if current_week else None


def send_current_week_message(message):
    current_week = get_current_week(message)

    if current_week:
        bot.send_message(
            message.chat.id,
            text=f"Текущая неделя:<blockquote>{current_week}</blockquote>",
            parse_mode='HTML',
            reply_markup=Keyboard.keyboards.show_schedule_kb()
        )
    else:
        bot.send_message(
            message.chat.id,
            text="Не удалось найти текущую неделю в расписании.",
            parse_mode='HTML'
        )

