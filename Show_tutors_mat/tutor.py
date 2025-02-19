import sqlite3
import datetime as dt
import telebot
import types
import re
from Keyboard.tutor_kb import show_tutor_kb, show_tutor_kb_buttons
from TOKEN import Token

connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)

def register_tutor_group_id(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['tutor_miit', 'tutor_1273'])
    def wrapped_group_id_tutor(call):
        return group_id_tutor(call)

@bot.callback_query_handler(func=lambda call: call.data in ['tutor_miit', 'tutor_1273'])
def group_id_tutor(call):
    chat_id = call.message.chat.id
    global group_id
    group_id = []
    if call.data == 'tutor_miit':
        group_id.append(1)

    elif call.data == 'tutor_1273':
        group_id.append(2)

    else:
        bot.send_message(chat_id, f'Произошла ошибочка')

    return group_id

def register_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['tutor_miit', 'tutor_1273'])
    def send_current_week_message(call):
        chat_id = call.message.chat.id
        group_id = group_id_tutor(call)
        date = dt.date.today()
        start_of_week = date - dt.timedelta(days=date.weekday())
        end_of_week = start_of_week + dt.timedelta(days=6)

        query = '''
              SELECT date
              FROM tutor
              WHERE group_id = ? and date BETWEEN ? AND ?
              '''

        cursor.execute(query, (group_id[0], start_of_week, end_of_week))
        print('group_id=', group_id)
        group_tutor_data = cursor.fetchall()
        print(group_tutor_data)

        #test
        start_of_week_str = str(start_of_week)
        end_of_week_str= str(end_of_week)

        message_text = (
                        f'\nНеделя: <blockquote>{start_of_week_str[8:]}.{start_of_week_str[5:7]}-{end_of_week_str[8:]}.{end_of_week_str[5:7]}</blockquote>\nДаты занятий:\n'

        )

        for data in group_tutor_data:
            cleaned_data = ''.join(data).strip("()'")
            message_text += f'<code>{cleaned_data}</code>\n'.format(data)

        # bot.send_message(chat_id, f'\n{message_text}\n', parse_mode='HTML')
        # bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())
        if group_tutor_data:

            bot.send_message(chat_id, f'\n{message_text}\n', parse_mode='HTML')
            bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())

        else:
            bot.send_message(chat_id, f'\n{message_text}\n'
                                      f'<i>На этой неделе занятий нет</i>', parse_mode='HTML')
            bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())




def change_week_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['change_week_tutor'])
    def handle_callback(call):

        chat_id = call.message.chat.id
        message = call.message
        bot.send_message(chat_id,f'Выбери нужную неделю')


        query = '''
                      SELECT week
                      FROM tutor
                      WHERE group_id = ? 
                      
                      '''
        cursor.execute(query, (group_id[0],))
        group_tutor_data = cursor.fetchall()


        message_text = (f'\nДоступные недели')


        try:

            for data in group_tutor_data:
                cleaned_data = ''.join(data).strip("()'")
                message_text += f'<code>{cleaned_data}</code>\n'.format(data)

        except TypeError:
            message_text = f'Нет доступных дат'



        register = bot.send_message(chat_id, f'{message_text}', parse_mode='HTML', reply_markup=show_tutor_kb())

        bot.register_next_step_handler(message, handle_change_week)



    def handle_change_week(message):

        week = message.text

        query = '''
                      SELECT date
                      FROM tutor
                      WHERE group_id = ? and week = ?
                '''
        try:
            cursor.execute(query, (group_id[0], week,))
            group_tutor_data = cursor.fetchall()

        except sqlite3.ProgrammingError:
           cursor.execute(query, (group_id[0], week,))
           group_tutor_data = cursor.fetchall()

        for data in group_tutor_data:
                message_text = f''
                cleaned_data = ''.join(data).strip("()'")
                message_text += f'<code>{cleaned_data}</code>\n'.format(data)
                bot.send_message(message.chat.id, f'Неделя  : <blockquote>{week}</blockquote>\nДаты занятий:\n<code>{cleaned_data}</code>',
                                 parse_mode="HTML", reply_markup=show_tutor_kb())


def change_group_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['change_group_tutor'])
    def handle_change_group(call):
        message = call.message
        bot.send_message(message.chat.id, f'Выбери группу', reply_markup=show_tutor_kb_buttons())

