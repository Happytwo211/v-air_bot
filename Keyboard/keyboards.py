from telebot import types


def show_start_kb():
    inline_keyboard_student_admin = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard_student_admin_button_1 = types.InlineKeyboardButton(
        'Я ученик',
        callback_data='student')
    inline_keyboard_student_admin_button_2 = types.InlineKeyboardButton(
        'Я преподаватель',
        callback_data='tutor')
    inline_keyboard_student_admin.add(inline_keyboard_student_admin_button_1).add(
        inline_keyboard_student_admin_button_2)
    return inline_keyboard_student_admin


def show_student_kb():
    inline_keyboard_student = types.InlineKeyboardMarkup()
    inline_keyboard_student_button_1 = types.InlineKeyboardButton(
        'Узнать расписание cвоей группы',
        callback_data='schedule_student',
        one_time_keyboard=True)
    inline_keyboard_student_button_2 = types.InlineKeyboardButton(
        'Получить материалы уроков',
        callback_data='lesson_materials_student',
        one_time_keyboard=True)
    inline_keyboard_student_button_3 = types.InlineKeyboardButton(
        'Вернуться в главное меню',
        callback_data='main_menu',
        one_time_keyboard=True)
    inline_keyboard_student.add(inline_keyboard_student_button_1).add(
        inline_keyboard_student_button_2).add(
        inline_keyboard_student_button_3)
    return inline_keyboard_student


def show_schedule_kb():
    inline_keyboard_schedule = types.InlineKeyboardMarkup(row_width=3)
    inline_keyboard_schedule_button_1 = types.InlineKeyboardButton('⬅️',
                                                                  callback_data='previous_week')
    inline_keyboard_schedule_button_2 = types.InlineKeyboardButton('🏠',
                                                                  callback_data='current_week')
    inline_keyboard_schedule_button_3 = types.InlineKeyboardButton('➡️',
                                                                  callback_data='next_week')
    inline_keyboard_schedule.row(
        inline_keyboard_schedule_button_1,
        inline_keyboard_schedule_button_2,
        inline_keyboard_schedule_button_3
    )

    return inline_keyboard_schedule

def show_tutor_kb():
    pass

