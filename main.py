from Admins import admin_list
from TOKEN import Token
from telebot import types
import os
import telebot
import sqlite3
from datetime import date, timedelta


db_path = os.path.join(os.getcwd(), 'DB/Groups.db')
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

bot = telebot.TeleBot(Token.TOKEN)
admins = admin_list.admin_id

class StartKeyboard:
    @staticmethod
    def show_start_kb():
        inline_keyboard_student_admin = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard_student_admin_button_1 = types.InlineKeyboardButton('Я ученик', callback_data='student')
        inline_keyboard_student_admin_button_2 = types.InlineKeyboardButton('Я преподаватель', callback_data='tutor')
        inline_keyboard_student_admin.add(inline_keyboard_student_admin_button_1).add(inline_keyboard_student_admin_button_2)
        return inline_keyboard_student_admin

class StudentKeyboard:
    @staticmethod
    def show_student_kb():
        inline_keyboard_student = types.InlineKeyboardMarkup()
        inline_keyboard_student_button_1 = types.InlineKeyboardButton('Узнать расписание cвоей группы', callback_data='schedule_student')
        inline_keyboard_student_button_2 = types.InlineKeyboardButton('Получить материалы уроков', callback_data='lesson_materials_student')
        inline_keyboard_student_button_3 = types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu')
        inline_keyboard_student.add(inline_keyboard_student_button_1).add(inline_keyboard_student_button_2).add(inline_keyboard_student_button_3)
        return inline_keyboard_student

class Commands:
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_photo(message.chat.id, 'https://imgur.com/a/4kg6OIp',
                       f'Это бот проекта ~V-Air~'
                       f'\n', reply_markup=StartKeyboard.show_start_kb())


class CurrentWeek():
    @staticmethod
    def get_current_week():
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        cursor.execute('''
            SELECT week
            FROM schedule 
            WHERE group_id = '1' AND date BETWEEN ? AND ?
            ''', (start_of_week, end_of_week))


        current_week = cursor.fetchone()



        if current_week:

            return current_week
        else:
            return None

class ScheduleStudent:

    def show_MIIT_schedule(message):
        current_week = CurrentWeek.get_current_week()

        if current_week:
            bot.send_message(
                message.chat.id,
                text=f"Текущая неделя: {current_week}",
                parse_mode='HTML'
            )
        else:
            bot.send_message(
                message.chat.id,
                text="Не удалось найти текущую неделю в расписании.",
                parse_mode='HTML'
            )

        # cursor.execute('''
        # SELECT week from schedule WHERE group_id = 1
        # ''')
        # show_data = cursor.fetchone()
        # if show_data is not None:
        #
        #     formated_data = '\n'.join([str(show_data[0])])
        #
        #     bot.send_message(
        #         message.chat.id,
        #         text=f'<blockquote>{formated_data}</blockquote>',
        #         parse_mode='HTML'
        #     )
        # else:
        #     bot.send_message(
        #         message.chat.id,
        #         text="Не удалось найти расписание для указанной группы.",
        #         parse_mode='HTML'
        #     )
        #
        # return formated_data

    def show_1273_schedule(message):
        cursor.execute('''
        SELECT * from Groups WHERE Group_Name = 'Гимназия РУТ МИИТ'
        ''')
        show_data = cursor.fetchone()
        formated_data = '\n'.join([' '.join(map(str, row)) for row in show_data])
        bot.send_message(message.chat.id, text=f'<blockquote>{formated_data}</blockquote>', parse_mode='HTML')
        return formated_data

class StudentCallBackData:
    @bot.callback_query_handler(func=lambda call: call.data == 'student')
    def student(call):
        message = call.message
        bot.send_message(message.chat.id, f'Что тебе нужно?', reply_markup=StudentKeyboard.show_student_kb())

    @bot.callback_query_handler(func=lambda call: call.data == 'schedule_student')
    def schedule_student(call):
        message = call.message
        inline_keyboard_db_choose_group = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard_db_button_1 = types.InlineKeyboardButton('Гимназия РУТ МИИТ', callback_data='РУТ МИИТ')
        inline_keyboard_db_button_2 = types.InlineKeyboardButton('Школа №1273', callback_data='1273')
        inline_keyboard_db_choose_group.add(inline_keyboard_db_button_1).add(inline_keyboard_db_button_2)
        bot.send_message(message.chat.id, text='Выбери свою группу', parse_mode='HTML',
                         reply_markup=inline_keyboard_db_choose_group)



    @bot.callback_query_handler(func=lambda call: call.data == 'lesson_materials_student')
    def schedule_student(call):
        message = call.message
        bot.send_message(message.chat.id, 'функиця в разработке')

    @bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
    def main_menu(call):
        message = call.message
        bot.send_message(message.chat.id, f'Вы вернулись в главнео меню',reply_markup=StudentKeyboard.show_student_kb())



class DataBaseCallBack:
    # @bot.callback_query_handler(func=lambda call: call.data == 'Гимназия РУТ МИИТ')
    # def schedule_student(call):
    #     message = call.message
    #     bot.answer_callback_query(callback_query_id=call.id, text= 'Вы уже на текущей неделе')

    @bot.callback_query_handler(func=lambda call: call.data == 'РУТ МИИТ')
    def schedule_student(call):
        message = call.message
        ScheduleStudent.show_MIIT_schedule(message)


    @bot.callback_query_handler(func=lambda call: call.data == '1273')
    def schedule_student(call):
        message = call.message
        ScheduleStudent.show_1273_schedule(message)
class TutorCallBackData:
    pass


if __name__ == '__main__':
    bot.infinity_polling()
