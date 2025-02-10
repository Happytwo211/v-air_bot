import sqlite3
import datetime as dt
import telebot
from Keyboard.tutor_kb import show_tutor_kb
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
    if call.data == 'tutor_miit':
        group_id = 1
        return group_id

    elif call.data == 'tutor_1273':
        group_id = 2
        return group_id

    else:
        bot.send_message(chat_id, f'Произошла ошибочка')
        return None

def register_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['tutor_miit', 'tutor_1273'])
    def send_current_week_message(call):
        #def change_week
        chat_id = call.message.chat.id
        group_id = group_id_tutor(call)
        date = dt.date.today()
        start_of_week = date - dt.timedelta(days=date.weekday())
        end_of_week = start_of_week + dt.timedelta(days=6)

        query = '''
              SELECT student_name, date, attendance 
              FROM tutor
              WHERE group_id = ? and date BETWEEN ? AND ?
              '''


        print(group_id)
        cursor.execute(query, (group_id, start_of_week, end_of_week))
        group_tutor_data = cursor.fetchall()
        print(group_tutor_data)
        if group_id == 1:
            group_name = 'Миит'
        elif group_id == 2:
            group_name = '1273'
        else:
            group_name = 'Группы нет в БД'

        message_text = (f'Группа\n'
                        f'<blockquote>{group_name}</blockquote>\n'
                        f'\nНеделя: <blockquote>{start_of_week}-{end_of_week}</blockquote>\n'
                        f'\n')

        for data in group_tutor_data:
            message_text += '<blockquote>{}</blockquote>\n'.format(data)

        bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')
        bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())

        # @bot.callback_query_handler(func=lambda call: call.data in ['attendance', 'materials', 'change_week_tutor'])
        # def send_current_week_message(call):
        #     chat_id = call.message.chat.id
        #
        #     if call.data == 'attendance':
        #         bot.send_message(chat_id,f'a')
        #
        #     elif call.data == 'materials':
        #         bot.send_message(chat_id, f'Материалы преподавателя')
        #
        #     elif call.data == 'change_week_tutor':
        #         bot.send_message(chat_id, f'в разработке',)


# def change_week_tutor(bot):
#     @bot.callback_query_handler(func=lambda call: call.data in ['change_week_tutor'])
#     change_week()

# def change_week_tutor(bot):
#     @bot.callback_query_handler(func=lambda call: call.data in ['change_week_tutor'])
#     def handle_callback(call):
#         chat_id = call.message.chat.id
#         bot.send_message(chat_id,f'Выбери нужную неделю')
#
#         query = '''
#                       SELECT week
#                       FROM tutor
#                       WHERE group_id = ? and date BETWEEN ? AND ?
#                       '''
