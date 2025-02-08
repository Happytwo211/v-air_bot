#TODO сделать админ панелт для добавления данных в БД

import telebot
from Show_tutors_mat.show_tutor_materials import register_tutor
from Commands.start import register_start
from Admins import admin_list
from TOKEN import Token
# from Show_tutors_mat.show_tutor_materials import register_tutor, register_tutor_buttons
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


#Обработчики сообщений
register_callback_start(bot)
register_callback_student(bot)
register_callback_groups(bot)
register_callback_switch_week(bot)
register_callback_not_handle(bot)

register_tutor(bot)

# register_manual_week(bot)
if __name__ == "__main__":
    bot.polling(none_stop=True)