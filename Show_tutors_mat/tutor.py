import sqlite3
import datetime as dt
import telebot
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
        message = call.message
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


        start_of_week_str = str(start_of_week)
        end_of_week_str= str(end_of_week)

        message_text = (
                        f'\nНеделя: <blockquote>{start_of_week_str[8:]}.{start_of_week_str[5:7]}-{end_of_week_str[8:]}.{end_of_week_str[5:7]}</blockquote>\nДаты занятий:\n'

        )

        for data in group_tutor_data:
            cleaned_data = ''.join(data).strip("()'")
            message_text += f'<code>{cleaned_data}</code>\n'.format(data)

        if group_tutor_data:

            bot.send_message(chat_id, f'\n{message_text}\n', parse_mode='HTML')
            bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())

        else:
            bot.send_message(chat_id, f'\n{message_text}\n'
                                      f'<i>На этой неделе занятий нет</i>', parse_mode='HTML')
            bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())



    # bot.register_next_step_handler(message, show_group_by_date)
    # print('вызван show by date')

    # @bot.message_handler(content_types=['text'])
    # def show_by_date(message):
    #     show = bot.register_next_step_handler(message, show_group_by_date)
    #     print(f'вызвана функция тест')
    #     return show if show else bot.send_message(message.chat.id, f'Такой даты нет')


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
        try:
            cursor.execute(query, (group_id[0],))
            group_tutor_data = cursor.fetchall()

        except NameError:
            group_id_tutor(call)


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
        # finally:

        for data in group_tutor_data:
            try:
                message_text = f''
                cleaned_data = ''.join(data).strip("()'")
                message_text += f'<code>{cleaned_data}</code>\n'.format(data)
                bot.send_message(message.chat.id, f'Неделя  : <blockquote>{week}</blockquote>\nДаты занятий:\n<code>{cleaned_data}</code>',
                                 parse_mode="HTML", reply_markup=show_tutor_kb())
            except TypeError:
                print('test type error')
                bot.send_message(message.chat.id, f'bug')



        # bot.register_next_step_handler(message, show_group_by_date(message))


def change_group_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['change_group_tutor'])
    def handle_change_group(call):
        message = call.message
        bot.send_message(message.chat.id, f'Выбери группу', reply_markup=show_tutor_kb_buttons())


def register_show_by_date(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['date'])
    def handle_date(call):
        message = call.message
        bot.send_message(message.chat.id, f'Наиши дату занятия')
        bot.register_next_step_handler(message, show_group_by_date)

def show_group_by_date(message):

    print('Вызваена функиция by date')
    print(message.text)
    pattern = r'\d{4}-\d{2}-\d{2}'
    match = re.match(pattern, message.text)

    if match:

        query = '''
                              SELECT student_name 
                              FROM tutor
                              WHERE group_id = ? and date = ?
                        '''
        cursor.execute(query, (group_id[0], message.text,))
        data = cursor.fetchall()

        # bot.send_message(message.chat.id, f'{data}',
        #                     reply_markup=show_tutor_kb())
        for data in data:
                message_text = f''
                cleaned_data = ''.join(data).strip("()'")
                message_text += f'<code>{cleaned_data}</code>\n'.format(data)
                bot.send_message(message.chat.id, f'{cleaned_data}>',
                            reply_markup=show_tutor_kb())

    else:
        bot.send_message(message.chat.id, f'Такой даты в расписании нет!')
    return
