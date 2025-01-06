from Admins import admin_list
from TOKEN import Token
from telebot import types
import os
import telebot
import sqlite3



db_path = os.path.join(os.getcwd(), 'DB/Groups.db')
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()



bot = telebot.TeleBot(Token.TOKEN)
admins = admin_list.admin_id

#Start Keyboard
inline_keyboard_student_admin = types.InlineKeyboardMarkup(row_width=2)
inline_keyboard_student_admin_button_1 = types.InlineKeyboardButton('Я ученик', callback_data='student')
inline_keyboard_student_admin_button_2 = types.InlineKeyboardButton('Я преподаватель', callback_data='tutor')
inline_keyboard_student_admin.add(inline_keyboard_student_admin_button_1).add(inline_keyboard_student_admin_button_2)

#Student Keyboard
inline_keyboard_student = types.InlineKeyboardMarkup()
inline_keyboard_student_button_1 = types.InlineKeyboardButton('Узнать расписание cвоей группы', callback_data='schedule_student')
inline_keyboard_student_button_2 = types.InlineKeyboardButton('Получить материалы уроков', callback_data='lesson_materials_student')
inline_keyboard_student_button_3 = types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu')
inline_keyboard_student.add(inline_keyboard_student_button_1).add(inline_keyboard_student_button_2).add(inline_keyboard_student_button_3)



class Commands:
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_photo(message.chat.id, 'https://imgur.com/a/4kg6OIp',
                       f'Это бот проекта ~V-Air~'
                       f'\n', reply_markup=inline_keyboard_student_admin)

    @bot.message_handler(commands=['db'])
    def db_test(message):
        cursor.execute('SELECT * FROM Groups')
        rows = cursor.fetchall()
        data_message = "\n".join([f"{row}" for row in rows])
        bot.send_message(message.chat.id, f'Вот твое расписание\n {data_message}')

class StudentCallBackData:
    @bot.callback_query_handler(func=lambda call: call.data == 'student')
    def student(call):
        message = call.message
        bot.send_message(message.chat.id, f'Чем бот может тебе помочь?', reply_markup=inline_keyboard_student)

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
        bot.send_message(message.chat.id, f'Вы вернулись в главнео меню',reply_markup=inline_keyboard_student_admin)

class TutorCallBackData:
    pass

if __name__ == '__main__':
    bot.infinity_polling()