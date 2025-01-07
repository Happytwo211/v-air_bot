from Admins import admin_list
from TOKEN import Token
from telebot import types
import os
import telebot
import sqlite3
from DB import groups_db_commands


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
class DB:
    @bot.message_handler(commands=['db'])
    def db_test(message):
        inline_keyboard_db_choose_group = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard_db_button_1 = types.InlineKeyboardButton(f'{groups_db_commands.List.list_group_name()}', callback_data='gr-1')
        inline_keyboard_db_button_2 = types.InlineKeyboardButton('Группа-2', callback_data='gr-2')
        inline_keyboard_db_choose_group.add(inline_keyboard_db_button_1).add(inline_keyboard_db_button_2)
        bot.send_message(message.chat.id, f'Выбери свою группу', reply_markup=inline_keyboard_db_choose_group)

class Commands:
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_photo(message.chat.id, 'https://imgur.com/a/4kg6OIp',
                       f'Это бот проекта ~V-Air~'
                       f'\n', reply_markup=StartKeyboard.show_start_kb())

class StudentCallBackData:
    @bot.callback_query_handler(func=lambda call: call.data == 'student')
    def student(call):
        message = call.message
        bot.send_message(message.chat.id, f'Чем бот может тебе помочь?', reply_markup=StudentKeyboard.show_student_kb())

    @bot.callback_query_handler(func=lambda call: call.data == 'schedule_student')
    def schedule_student(call):
        message = call.message
        bot.send_message(message.chat.id, 'функиця в разработке')

    @bot.callback_query_handler(func=lambda call: call.data == 'lesson_materials_student')
    def schedule_student(call):
        message = call.message
        bot.send_message(message.chat.id, 'функиця в разработке')

    @bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
    def schedule_student(call):
        message = call.message
        bot.send_message(message.chat.id, f'Вы вернулись в главнео меню',reply_markup=StudentKeyboard.show_student_kb())

class DataBaseCallBack:
    @bot.callback_query_handler(func=lambda call: call.data == 'gr-1')
    def schedule_student(call):
        message = call.message
        db_data = cursor.execute('SELECT * FROM Groups ORDER BY "Group_Name"')
        formated_data = '\n'.join([' '.join(map(str, row)) for row in db_data])
        bot.send_message(message.chat.id, f'Расписание группы-1\n{(formated_data)}')

class TutorCallBackData:
    pass


if __name__ == '__main__':
    bot.infinity_polling()