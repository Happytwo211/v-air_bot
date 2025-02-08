import sqlite3
import datetime as dt
import telebot
from Keyboard.tutor_kb import show_tutor_kb_buttons, show_tutor_kb
from TOKEN import Token

connection = sqlite3.connect('DB/v_air_db', check_same_thread=False)
cursor = connection.cursor()
bot = telebot.TeleBot(Token.TOKEN)

# if call.data == 'previous_week':
            #     new_week = change_week(-1)
            #     send_current_week_message(new_week, chat_id, handle_group_id(call))
            #     print(f'Вызван pr wekk')

def register_tutor(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['tutor_miit', 'tutor_1273'])
    def send_current_week_message(call):
        chat_id = call.message.chat.id
        date = dt.date.today()
        start_of_week = date - dt.timedelta(days=date.weekday())
        end_of_week = start_of_week + dt.timedelta(days=6)

        query = '''
                                      SELECT student_name, date, attendance 
                                      FROM tutor
                                      WHERE group_id = ? and date BETWEEN ? AND ?
                                      '''
        if call.data == 'tutor_miit':

            group_id = 1
            message_text = (f'Группа\n'
                            f'<blockquote>МИИТ</blockquote>\n'
                            f'\nНеделя:\n <blockquote>{start_of_week}-{end_of_week}</blockquote>')

            for data in group_tutor_data:
                message_text += '<blockquote>{}</blockquote>\n'.format(data)

            bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')

        cursor.execute(query, (group_id, start_of_week, end_of_week))
        group_tutor_data = cursor.fetchall()

        message_text = (f'Группа\n'
                        f'<blockquote>МИИТ</blockquote>\n'
                        f'\nНеделя:\n <blockquote>{start_of_week}-{end_of_week}</blockquote>')

        for data in group_tutor_data:
            message_text += '<blockquote>{}</blockquote>\n'.format(data)

        bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')
        # bot.send_message(chat_id, f'<blockquote>{data[0],data[1],data[2]}</blockquote>', parse_mode='HTML')

        bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())





        if call.data == 'tutor_miit':

            group_id = 1

            cursor.execute(query, (group_id, start_of_week, end_of_week))
            group_tutor_data = cursor.fetchall()

            message_text = (f'Группа\n'
                      f'<blockquote>МИИТ</blockquote>\n'
                      f'\nНеделя:\n <blockquote>{start_of_week}-{end_of_week}</blockquote>')

            for data in group_tutor_data:
                message_text +='<blockquote>{}</blockquote>\n'.format(data)

            bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')
                # bot.send_message(chat_id, f'<blockquote>{data[0],data[1],data[2]}</blockquote>', parse_mode='HTML')

            bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())

        elif call.data == 'tutor_1273':

            group_id = 2

            cursor.execute(query, (group_id, start_of_week, end_of_week))
            group_tutor_data = cursor.fetchall()

            message_text = (f'Группа\n'
                            f'<blockquote>МИИТ</blockquote>\n'
                            f'\nНеделя:\n <blockquote>{start_of_week}-{end_of_week}</blockquote>')

            for data in group_tutor_data:
                message_text += '<blockquote>{}</blockquote>\n'.format(data)

            bot.send_message(chat_id, f'{message_text}', parse_mode='HTML')
            # bot.send_message(chat_id, f'<blockquote>{data[0],data[1],data[2]}</blockquote>', parse_mode='HTML')

            bot.send_message(chat_id, f'Выбери функционал', reply_markup=show_tutor_kb())

        else:
            bot.send_message(chat_id, f'Произошла ошибочка')



        @bot.callback_query_handler(func=lambda call: call.data in ['attendance', 'materials'])
        def send_current_week_message(call):
            chat_id = call.message.chat.id
            if call.data == 'attendance':
                bot.send_message(chat_id,f'zbs')

            elif call.data == 'materials':
                bot.send_message(chat_id, f'zbs')

            else:
                bot.send_message(chat_id, f'huio')