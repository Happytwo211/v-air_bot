import telebot
import datetime as dt
import sqlite3
from Keyboard.keyboards import show_student_kb, show_tutor_kb, choose_group_kb, lesson_materials, show_start_kb
from Show_Week.show_week import send_current_week_message
from TOKEN import Token
from Show_Week.show_week import change_week


bot = telebot.TeleBot(Token.TOKEN)
connection = sqlite3.connect('db_groups.db',check_same_thread=False)



def register_callback_start(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['student', 'tutor'])
    def callback_handler(call):
        if call.data == 'student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_student_kb())
        elif call.data == 'tutor':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_tutor_kb())

def register_callback_student(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['schedule_student', 'lesson_materials_student',
                                                                'main_menu'])
    def callback_handler(call):

        if call.data == 'schedule_student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=choose_group_kb())
        elif call.data == 'lesson_materials_student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=lesson_materials())
        elif call.data == 'main_menu':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_start_kb())

def register_callback_groups(bot):
    # TODO bug
    @bot.callback_query_handler(func=lambda call: call.data in ['miit', '1273'])
    def wrapped_bot_send_message(call):

        return bot_send_message(call)



@bot.callback_query_handler(func=lambda call: call.data in ['miit', '1273'])
def bot_send_message(call):
    today = dt.date.today()
    chat_id = call.message.chat.id
    if call.data == 'miit':
        group_id = 1
        return send_current_week_message(today, chat_id, group_id)


    elif call.data == '1273':
        group_id = 2
        return send_current_week_message(today, chat_id, group_id)

    else:
        bot.send_message(chat_id, f'error')

def handle_callback_group_id(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['miit', '1273'])
    def wrapped_handle_group_id(call):
        return handle_group_id(call)




def register_callback_switch_week(bot):

    @bot.callback_query_handler(func=lambda call: call.data in ['previous_week', 'current_week', 'next_week'])
    def handle_callback(call):
        chat_id = call.message.chat.id
        today = dt.date.today()

        if call.data == 'previous_week':
            new_week = change_week(-1)
            send_current_week_message(new_week,chat_id, handle_group_id(call))


        elif call.data == 'next_week':
            new_week = change_week(1)
            send_current_week_message(new_week, chat_id, handle_group_id(call))

        elif call.data == 'current_week':

            send_current_week_message(today, chat_id, handle_group_id(call))

        else:
            bot.send_message(chat_id, f'Произошла какая то ошибка')
            return

def handle_group_id(call):
    group_id = None
    result = bot_send_message(call)
    if result == 'miit':
        group_id = 1
    elif result == '1273':
        group_id = 2
    return group_id