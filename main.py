from Admins import admin_list
from TOKEN import Token
from telebot import types
import os
import telebot
import sqlite3
from datetime import date
# <blockquote>

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


    # @bot.message_handler(commands=['test'])
    # def test(message):
    #     bot.send_message(message.chat.id, text='<blockquote>test message</blockquote>', parse_mode='HTML')
    #     bot.send_message(message.chat.id, text='<code>test message</code>', parse_mode='HTML')
class ScheduleStudent:
    def show_MIIT_schedule(message):
        cursor.execute('''
        SELECT * from Groups WHERE Group_Name = 'Гимназия РУТ МИИТ'
        ''')
        show_data = cursor.fetchone()
        formated_data = '\n'.join([' '.join(map(str, row)) for row in show_data])
        bot.send_message(message.chat.id, text=f'<blockquote>{formated_data}</blockquote>', parse_mode='HTML')
        return formated_data

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


    # @bot.callback_query_handler(func=lambda call: call.data == 'test')
    # def schedule_student(call):
    #     message = call.message
    #     bot.answer_callback_query(callback_query_id=call.id, text= 'tbali')

class DataBaseCallBack:
    @bot.callback_query_handler(func=lambda call: call.data == 'РУТ МИИТ')
    def schedule_student(call):
        message = call.message
        ScheduleStudent.show_MIIT_schedule(message)
        # message = call.message
        # db_data = cursor.execute('SELECT Group_Name FROM Groups WHERE Group_Name = "Гимназия РУТ МИИТ"')
        # formated_data = '\n'.join([' '.join(map(str, row)) for row in db_data])
        # bot.send_message(message.chat.id, f'Расписание группы-1\n{(formated_data)}')

    @bot.callback_query_handler(func=lambda call: call.data == '1273')
    def schedule_student(call):
        message = call.message
        ScheduleStudent.show_1273_schedule(message)
class TutorCallBackData:
    pass


if __name__ == '__main__':
    bot.infinity_polling()
