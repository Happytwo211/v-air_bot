import re
from Admins import admin_list
from TOKEN import Token
from telebot import types
import os
import telebot
import sqlite3
from datetime import date, timedelta

#TODO Добавить выведение вместе с неделями самого расписаниия
#TODO Cделать, чтобы неделю можно было написать самому в чат бота и он выдал расписание с ней в формате 13.01-19.01

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
        inline_keyboard_student_button_1 = types.InlineKeyboardButton('Узнать расписание cвоей группы', callback_data='schedule_student', one_time_keyboard=True)
        inline_keyboard_student_button_2 = types.InlineKeyboardButton('Получить материалы уроков', callback_data='lesson_materials_student', one_time_keyboard=True)
        inline_keyboard_student_button_3 = types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu', one_time_keyboard=True)
        inline_keyboard_student.add(inline_keyboard_student_button_1).add(inline_keyboard_student_button_2).add(inline_keyboard_student_button_3)
        return inline_keyboard_student

class ScheduleKeyboard:
    @staticmethod
    def show_schedule_kb_MIIT():
        inline_keyboard_schedule = types.InlineKeyboardMarkup(row_width=3)
        inline_keyboard_schedule_button_1 = types.InlineKeyboardButton('⬅️',
                                                                      callback_data='previous_week_MIIT')
        inline_keyboard_schedule_button_2 = types.InlineKeyboardButton('🏠',
                                                                      callback_data='current_week_MIIT')
        inline_keyboard_schedule_button_3 = types.InlineKeyboardButton('➡️',
                                                                      callback_data='next_week_MIIT')
        inline_keyboard_schedule.row(
            inline_keyboard_schedule_button_1,
            inline_keyboard_schedule_button_2,
            inline_keyboard_schedule_button_3
        )
        # inline_keyboard_schedule.add(inline_keyboard_schedule_button_1).add(inline_keyboard_schedule_button_2).add(
        #     inline_keyboard_schedule_button_3
        return inline_keyboard_schedule

    @staticmethod
    def show_schedule_kb_1273():
        inline_keyboard_schedule = types.InlineKeyboardMarkup(row_width=1)
        inline_keyboard_schedule_button_1 = types.InlineKeyboardButton('⬅️',
                                                                       callback_data='previous_week_1273')
        inline_keyboard_schedule_button_2 = types.InlineKeyboardButton('🏠',
                                                                       callback_data='current_week_1273')
        inline_keyboard_schedule_button_3 = types.InlineKeyboardButton('➡️',
                                                                       callback_data='next_week_1273')
        inline_keyboard_schedule.row(
            inline_keyboard_schedule_button_1,
            inline_keyboard_schedule_button_2,
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
    def change_week(current_date, offset):
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
        ShowWeek.get_1273_current_week(message)

class WeekCallData:

    #MIIT

    @bot.callback_query_handler(func=lambda call: call.data == 'current_week_MIIT')
    def current_week_MIIT(call):
        message = call.message
        ShowWeek.get_MIIT_current_week(message)

    @bot.callback_query_handler(func=lambda call: call.data == 'next_week_MIIT')
    def next_week_MIIT(call):
        message = call.message
        current_date = ShowWeek.get_current_date()
        next_week_date = ShowWeek.change_week(current_date, offset=1)


        start_of_next_week = next_week_date - timedelta(days=next_week_date.weekday())
        end_of_next_week = start_of_next_week + timedelta(days=6)

        cursor.execute('''
                       SELECT week
                       FROM schedule 
                       WHERE group_id = '1' AND date BETWEEN ? AND ?
                       ''', (start_of_next_week, end_of_next_week))

        next_week = cursor.fetchone()

        if next_week:
            bot.send_message(
                message.chat.id,
                text=f"Следующая неделя:<blockquote>{next_week[0]}</blockquote>",
                parse_mode='HTML',
                reply_markup=ScheduleKeyboard.show_schedule_kb_MIIT()
            )
            return next_week
        else:
            bot.send_message(
                message.chat.id,
                text="Не удалось найти текущую неделю в расписании.",
                parse_mode='HTML'
            )
            return None

    @bot.callback_query_handler(func=lambda call: call.data == 'previous_week_MIIT')
    def next_week_MIIT(call):
        message = call.message
        current_date = ShowWeek.get_current_date()
        previous_week_date = ShowWeek.change_week(current_date, offset=-1)

        start_of_previous_week = previous_week_date - timedelta(days=previous_week_date.weekday())
        end_of_previous_week = start_of_previous_week + timedelta(days=6)

        cursor.execute('''
                           SELECT week
                           FROM schedule 
                           WHERE group_id = '1' AND date BETWEEN ? AND ?
                           ''', (start_of_previous_week, end_of_previous_week))

        previous_week = cursor.fetchone()

        if previous_week:
            bot.send_message(
                message.chat.id,
                text=f"Предыдущая неделя:<blockquote>{previous_week[0]}</blockquote>",
                parse_mode='HTML',
                reply_markup=ScheduleKeyboard.show_schedule_kb_MIIT()
            )
            return previous_week
        else:
            bot.send_message(
                message.chat.id,
                text="Не удалось найти текущую неделю в расписании.",
                parse_mode='HTML'
            )
            return None


    #1273

    @bot.callback_query_handler(func=lambda call: call.data == 'current_week_1273')
    def current_week_1273(call):
        message = call.message
        ShowWeek.get_1273_current_week(message)

    @bot.callback_query_handler(func=lambda call: call.data == 'next_week_1273')
    def next_week_MIIT(call):
        message = call.message
        current_date = ShowWeek.get_current_date()
        next_week_date = ShowWeek.change_week(current_date, offset=1)

        start_of_next_week = next_week_date - timedelta(days=next_week_date.weekday())
        end_of_next_week = start_of_next_week + timedelta(days=6)

        cursor.execute('''
                           SELECT week
                           FROM schedule 
                           WHERE group_id = '2' AND date BETWEEN ? AND ?
                           ''', (start_of_next_week, end_of_next_week))

        next_week = cursor.fetchone()

        if next_week:
            bot.send_message(
                message.chat.id,
                text=f"Следующая неделя:<blockquote>{next_week[0]}</blockquote>",
                parse_mode='HTML',
                reply_markup=ScheduleKeyboard.show_schedule_kb_MIIT()
            )
            return next_week
        else:
            bot.send_message(
                message.chat.id,
                text="Не удалось найти текущую неделю в расписании.",
                parse_mode='HTML'
            )
            return None

    @bot.callback_query_handler(func=lambda call: call.data == 'previous_week_1273')
    def next_week_MIIT(call):
        message = call.message
        current_date = ShowWeek.get_current_date()
        previous_week_date = ShowWeek.change_week(current_date, offset=-1)

        start_of_previous_week = previous_week_date - timedelta(days=previous_week_date.weekday())
        end_of_previous_week = start_of_previous_week + timedelta(days=6)

        cursor.execute('''
                               SELECT week
                               FROM schedule 
                               WHERE group_id = '2' AND date BETWEEN ? AND ?
                               ''', (start_of_previous_week, end_of_previous_week))

        previous_week = cursor.fetchone()

        if previous_week:
            bot.send_message(
                message.chat.id,
                text=f"Предыдущая неделя:<blockquote>{previous_week[0]}</blockquote>",
                parse_mode='HTML',
                reply_markup=ScheduleKeyboard.show_schedule_kb_MIIT()
            )
            return previous_week
        else:
            bot.send_message(
                message.chat.id,
                text="Не удалось найти текущую неделю в расписании.",
                parse_mode='HTML'
            )
            return None


class ManualWeek:


    @bot.message_handler(commands=['schedule'])
    def handle_schedule(message):
        inline_keyboard_db_choose_group = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard_db_button_1 = types.InlineKeyboardButton('Гимназия РУТ МИИТ', callback_data='id_1')
        inline_keyboard_db_button_2 = types.InlineKeyboardButton('Школа №1273', callback_data='id_2')
        inline_keyboard_db_choose_group.add(inline_keyboard_db_button_1, inline_keyboard_db_button_2)
        bot.send_message(message.chat.id, text='Выберите вашу группу:', parse_mode='HTML',
                         reply_markup=inline_keyboard_db_choose_group)


    @bot.callback_query_handler(func=lambda call: call.data in ['id_1'])
    def manual_schedule(call):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text=f'Вы выбрали группу Гимназия РУТ МИИТ'
                                                    f'Пожалуйста, введите нужную неделю в формате DD.MM-DD.MM:')
        return 'id_1'

    @bot.callback_query_handler(func=lambda call: call.data in ['id_2'])
    def manual_schedule(call):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text=f'Вы выбрали группу Гимназия РУТ МИИТ'
                                                    f'Пожалуйста, введите нужную неделю в формате DD.MM-DD.MM:')
        return 'id_2'

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        date_pattern = r'\d{2}\.\d{2}-\d{2}\.\d{2}'
        if re.match(date_pattern, message.text):



            if 'id_1':
                cursor.execute('''
                              SELECT weekday, start_time, end_time, classroom, date, location
                              FROM schedule
                              WHERE group_id = '1' AND week BETWEEN ? AND ?
                              ''', (message.text.split('-')[0], message.text.split('-')[1]))

                schedule_data = cursor.fetchall()

                if schedule_data:
                    bot.send_message(message.chat.id, f'Твое расписание'
                                                      f'\n{schedule_data[0]}')
                else:
                    bot.send_message(message.chat.id, f'Такой недели не найдено')
                    return None

            if 'id_2':
                cursor.execute('''
                              SELECT week
                              FROM schedule
                              WHERE group_id = '2' AND date BETWEEN ? AND ?
                              ''', ((message.text.split('-')[0], message.text.split('-')[1])))

                schedule_data = cursor.fetchone()

                if schedule_data:
                    bot.send_message(message.chat.id, f'Твое расписание'
                                                      f'\n{schedule_data}')
                else:
                    bot.send_message(message.chat.id, f'Такой недели не найдено')
                    return None

        elif message.text == '/home':
            bot.send_message(message.chat.id, 'Вы вернулдись на жомашнюю страницу', reply_markup=StartKeyboard.show_start_kb() )


        else:
            bot.send_message(chat_id, f'Некорректный формат даты. Пожалуйста, введите дату в формате DD.MM-DD.MM.'
                                      f'\nЧтобы вернутся на начальную страницу - /home')


bot.infinity_polling()