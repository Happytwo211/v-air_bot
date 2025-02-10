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
        cursor.execute(query, (group_id[0], start_of_week, end_of_week))
        group_tutor_data = cursor.fetchall()
        print(group_tutor_data)



        message_text = (
                        f'\nНеделя: <blockquote>{start_of_week}-{end_of_week}</blockquote>\n'
                        f'\n'
        )

        for data in group_tutor_data:
            message_text += '<blockquote>{}</blockquote>\n'.format(data)

        bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')
        bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())

        # global id_
        # id_ = []
        # id_.append(group_id)
        # print(id_)
        # return id_


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


def change_week_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['change_week_tutor'])
    def handle_callback(call):

        chat_id = call.message.chat.id
        bot.send_message(chat_id,f'Выбери нужную неделю')
        group_id = group_id_tutor(call)
        print(f'group_id\n{group_id}')
        # group_id = []
        # if id_[0] == 1:
        #     group_id.append('1')
        #
        # elif id_[0] == 2:
        #     group_id.append('2')

        query = '''
                      SELECT week
                      FROM tutor
                      WHERE group_id = ? 
                      
                      '''
        cursor.execute(query, (group_id,))
        group_tutor_data = cursor.fetchall()

        message_text = (f'<blockquote> {group_tutor_data}</blockquote>\n'
                        f'\n')

        for data in group_tutor_data:
            message_text += '<blockquote>{}</blockquote>\n'.format(data)

        bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')