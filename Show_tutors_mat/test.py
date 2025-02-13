import sqlite3
import datetime as dt
import telebot
import re
from Keyboard.tutor_kb import show_tutor_kb
from TOKEN import Token
#TODO после выбора недели сделать выбор даты и только потом уже выбор отметчки учеников
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


        print(group_id)
        cursor.execute(query, (group_id[0], start_of_week, end_of_week))
        group_tutor_data = cursor.fetchall()
        print(group_tutor_data)



        message_text = (
                        f'\nНеделя: <blockquote>{start_of_week}-{end_of_week}</blockquote>\n'
                        f'\n'
        )

        for data in group_tutor_data:
            cleaned_data = ''.join(data).strip("()'")
            message_text += f'<blockquote>{cleaned_data}</blockquote>\n'.format(data)

        bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')
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


        message_text = (f'\nДоступные недели\n')

        for data in group_tutor_data:
            cleaned_data = ''.join(data).strip("()'")
            message_text += f'<code>{cleaned_data}</code>\n'.format(data)


        register = bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')

        bot.register_next_step_handler(message, change_week_tutor)



    def change_week_tutor(message):
        week = message.text

        query = '''
                      SELECT student_name, date, attendance 
                      FROM tutor
                      WHERE group_id = ? and week = ?
                '''


        cursor.execute(query, (group_id[0], week,))
        group_tutor_data = cursor.fetchall()
        if group_tutor_data:
            bot.send_message(message.chat.id, f'Неделя : <blockquote>{week}</blockquote>\n<blockquote>{group_tutor_data}</blockquote>', parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, f'Такой недели нет')

#осещаемость
# если был, то апдейт колумн