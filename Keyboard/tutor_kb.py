from telebot import types
def show_tutor_kb_buttons():
    tutor_keyboard = types.InlineKeyboardMarkup(row_width=2)
    tutor_keyboard_buttons_1 = types.InlineKeyboardButton('Группа МииТ', callback_data='tutor_miit')
    tutor_keyboard_buttons_2 = types.InlineKeyboardButton('Группа 1273', callback_data='tutor_1273')
    tutor_keyboard.add(tutor_keyboard_buttons_1,tutor_keyboard_buttons_2)
    return tutor_keyboard


def show_tutor_kb():
    inline_kb_tutor = types.InlineKeyboardMarkup(row_width=2)
    inline_kb_tutor_button_1 = types.InlineKeyboardButton('Отметить посещаемость',
                                                          callback_data='attendance')
    inline_kb_tutor_button_2 = types.InlineKeyboardButton('Получить материалы',
                                                          callback_data='materials')
    inline_kb_tutor_button_3 = types.InlineKeyboardButton('Поменять неделю', callback_data='change_week_tutor')

    inline_kb_tutor.add(inline_kb_tutor_button_1,
                        inline_kb_tutor_button_2, inline_kb_tutor_button_3)
    return inline_kb_tutor

