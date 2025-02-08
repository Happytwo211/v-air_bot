from telebot import types
def show_tutor_kb_buttons():
    tutor_keyboard = types.InlineKeyboardMarkup(row_width=2)
    tutor_keyboard_buttons_1 = types.InlineKeyboardButton('Группа МииТ', callback_data='tutor_miit')
    tutor_keyboard_buttons_2 = types.InlineKeyboardButton('Группа 1273', callback_data='tutor_1273')
    tutor_keyboard.add(tutor_keyboard_buttons_1,tutor_keyboard_buttons_2)
    return tutor_keyboard



