#TODO сделать админ панелт для добавления данных в БД

import telebot
# from Show_tutors_mat.show_tutor_materials import register_tutor
from Show_tutors_mat.tutor import register_tutor_group_id, register_tutor, change_week_tutor, change_group_tutor
from Commands.start import register_start, test_11
from Admins import admin_list
from TOKEN import Token
from Callback_Data.callback_data_start_kb import (register_callback_start,
                                                  register_callback_student,
                                                  register_callback_switch_week,
                                                  register_callback_groups,
                                                  register_callback_not_handle)



# from Manual_week.show_manual_week import register_manual_week

#Подключение БД

# connection = sqlite3.connect('v_air_db',check_same_thread=False)
# cursor = connection.cursor()

#Настройки бота и инициализвация

bot = telebot.TeleBot(Token.TOKEN)
admins = admin_list.admin_id

#commands
register_start(bot)
test_11(bot)

#Обработчики сообщений
register_callback_start(bot)
register_callback_student(bot)
register_callback_groups(bot)
register_callback_switch_week(bot)
register_callback_not_handle(bot)

#Функции препода
# register_tutor(bot)
register_tutor(bot)
register_tutor_group_id(bot)
change_week_tutor(bot)
change_group_tutor(bot)


# register_manual_week(bot)
if __name__ == "__main__":
    bot.polling(none_stop=True)