import telebot
from Keyboard.keyboards import show_student_kb, show_tutor_kb, choose_group_kb, lesson_materials, show_start_kb
from Show_Week.show_week import send_current_week_message
from TOKEN import Token


bot = telebot.TeleBot(Token.TOKEN)

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
    @bot.callback_query_handler(func=lambda call: call.data in ['schedule_student', 'lesson_materials_student', 'main_menu'])
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
        # elif call.data == 'miit':
        #     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        #     bot.register_next_step_handler(call.message, register_callback_miit)

def register_callback_groups(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['miit', '1273'])
    def bot_send_message(call):
        if call.data == 'miit':
            chat_id = call.message.chat.id
            send_current_week_message(chat_id, 1)
        elif call.data == '1273':
            chat_id = call.message.chat.id
            send_current_week_message(chat_id, 2)



