from Admins import admin_list
from TOKEN import Token
from telebot import types
import os
import telebot
import sqlite3
from datetime import date, timedelta

#Подключение БД
db_path = os.path.join(os.getcwd(), 'DB/Groups.db')
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

#Настройки бота и инициализвация
bot = telebot.TeleBot(Token.TOKEN)
admins = admin_list.admin_id


# Клавиатуры
class StartKeyboard:
    @staticmethod
    def show_start_kb():
        inline_keyboard_student_admin = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard_student_admin_button_1 = types.InlineKeyboardButton('Я ученик', callback_data='student')
        inline_keyboard_student_admin_button_2 = types.InlineKeyboardButton('Я преподаватель', callback_data='tutor')
        inline_keyboard_student_admin.add(inline_keyboard_student_admin_button_1).add(
            inline_keyboard_student_admin_button_2)
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

class ScheduleKeyboard:
    @staticmethod
    def show_schedule_kb_MIIT():
        inline_keyboard_schedule = types.InlineKeyboardMarkup(row_width=1)
        inline_keyboard_schedule_button_1 = types.InlineKeyboardButton('Предыдущая неделя',
                                                                      callback_data='previous_week_MIIT')
        inline_keyboard_schedule_button_2 = types.InlineKeyboardButton('Текущая неделя',
                                                                      callback_data='current_week_MIIT')
        inline_keyboard_schedule_button_3 = types.InlineKeyboardButton('Cледующая неделя',
                                                                      callback_data='next_week_MIIT')
        inline_keyboard_schedule.add(inline_keyboard_schedule_button_1).add(inline_keyboard_schedule_button_2).add(
            inline_keyboard_schedule_button_3
        )
        return inline_keyboard_schedule

    @staticmethod
    def show_schedule_kb_1273():
        inline_keyboard_schedule = types.InlineKeyboardMarkup(row_width=1)
        inline_keyboard_schedule_button_1 = types.InlineKeyboardButton('Предыдущая неделя',
                                                                       callback_data='previous_week_1273')
        inline_keyboard_schedule_button_2 = types.InlineKeyboardButton('Текущая неделя',
                                                                       callback_data='current_week_1273')
        inline_keyboard_schedule_button_3 = types.InlineKeyboardButton('Cледующая неделя',
                                                                       callback_data='next_week_1273')
        inline_keyboard_schedule.add(inline_keyboard_schedule_button_1).add(inline_keyboard_schedule_button_2).add(
            inline_keyboard_schedule_button_3
        )
        return inline_keyboard_schedule

class TutorKeyboard:
    pass
    @staticmethod
    def show_tutor_kb():
        pass
        # inline_keyboard_tutor = types.InlineKeyboardMarkup()
        # inline_keyboard_tutor_button_2 = types.InlineKeyboardButton('Выбрать группу',
        #                                                               callback_data='schedule_student')
        # inline_keyboard_student_button_3 = types.InlineKeyboardButton('Получить материалы уроков',
        #                                                               callback_data='lesson_materials_student')
        # inline_keyboard_student_button_4 = types.InlineKeyboardButton('Вернуться в главное меню',
        #                                                               callback_data='main_menu')
        # inline_keyboard_student.add(inline_keyboard_student_button_1).add(inline_keyboard_student_button_2).add(
        #     inline_keyboard_student_button_3)
        # return inline_keyboard_student

#Комманды
class Commands:
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_photo(message.chat.id, 'https://imgur.com/a/4kg6OIp',
                       f'Это бот проекта ~V-Air~'
                       f'\n', reply_markup=StartKeyboard.show_start_kb())

#Выбор недели
class ShowWeek:
    @staticmethod
    def get_current_date():
        return date.today()
    @staticmethod
    def change_week():
        offset = int(None)
        #if callback data == previous_week
        #week_ossset = -1
        # return ofset
        #if callback data == next_week
        #week_offset == 1
        #return offset
        #if callback == current_week
        #week_offset == 0
        #return offset
        new_week = ShowWeek.get_current_date() + timedelta(days=offset*7)
        return new_week


    @staticmethod
    def get_MIIT_current_week(message):

        today = ShowWeek.get_current_date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        cursor.execute('''
               SELECT week
               FROM schedule 
               WHERE group_id = '1' AND date BETWEEN ? AND ?
               ''', (start_of_week, end_of_week))

        current_week = cursor.fetchone()

        if current_week:
            bot.send_message(
                message.chat.id,
                text=f"Текущая неделя:<blockquote>{current_week[0]}</blockquote>",
                parse_mode='HTML',
                reply_markup=ScheduleKeyboard.show_schedule_kb_MIIT()
            )
            return current_week
        else:
            bot.send_message(
                            message.chat.id,
                            text="Не удалось найти текущую неделю в расписании.",
                            parse_mode='HTML'
                        )
            return None

    def get_1273_current_week(message):
        today = ShowWeek.get_current_date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        cursor.execute('''
                       SELECT week
                       FROM schedule 
                       WHERE group_id = '2' AND date BETWEEN ? AND ?
                       ''', (start_of_week, end_of_week))

        current_week = cursor.fetchone()


        cursor.fetchone()

        if current_week:
            bot.send_message(
                message.chat.id,
                text=f"Текущая неделя:<blockquote>{current_week[0]}</blockquote>",
                parse_mode='HTML',
                reply_markup=ScheduleKeyboard.show_schedule_kb_1273()
            )
            return current_week

        else:
            bot.send_message(
                message.chat.id,
                text="Не удалось найти текущую неделю в расписании.",
                parse_mode='HTML'
            )
            return None

#CallData
class StartCallBackData:

    @bot.callback_query_handler(func=lambda call: call.data == 'student')
    def student(call):
        message = call.message
        bot.send_message(message.chat.id, f'Что тебе нужно?', reply_markup=StudentKeyboard.show_student_kb())

    @bot.callback_query_handler(func=lambda call: call.data == 'tutor')
    def tutor(call):
        message = call.message
        if message.from_user.id in admins:
            message = call.message
            bot.send_message(message.chat.id, f'Что тебе нужно?', reply_markup=TutorKeyboard.show_tutor_kb())
        else:
            bot.send_message(message.chat.id, f'Ты не преподаватель', reply_markup=StudentKeyboard.show_student_kb())

class StudentCallBackData:

    @bot.callback_query_handler(func=lambda call: call.data == 'schedule_student')
    def choose_group(call):
        message = call.message
        inline_keyboard_db_choose_group = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard_db_button_1 = types.InlineKeyboardButton('Гимназия РУТ МИИТ', callback_data='РУТ МИИТ')
        inline_keyboard_db_button_2 = types.InlineKeyboardButton('Школа №1273', callback_data='1273')
        inline_keyboard_db_choose_group.add(inline_keyboard_db_button_1).add(inline_keyboard_db_button_2)
        bot.send_message(message.chat.id, text='Выбери свою группу', parse_mode='HTML',
                         reply_markup=inline_keyboard_db_choose_group)

    @bot.callback_query_handler(func=lambda call: call.data == 'lesson_materials_student')
    def get_lesson_materials(call):
        message = call.message
        bot.send_message(message.chat.id, f'Твои материалы урока лежат здесь ...' )

    @bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
    def get_lesson_materials(call):
        message = call.message
        bot.send_message(message.chat.id, f'Вы вернулись в главное меню', reply_markup=StartKeyboard.show_start_kb())

class GroupsCallData:
    @bot.callback_query_handler(func=lambda call: call.data == 'РУТ МИИТ')
    def schedule_student(call):
        message = call.message
        ShowWeek.get_MIIT_current_week(message)

    @bot.callback_query_handler(func=lambda call: call.data == '1273')
    def schedule_student(call):
        message = call.message
        ShowWeek.get_MIIT_current_week(message)

class WeekCallData:
    @bot.callback_query_handler(func=lambda call: call.data == 'current_week')
    def current_week(call):
        message = call.message
        ShowWeek.get_current_date()

bot.infinity_polling()