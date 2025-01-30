import telebot
from Keyboard.keyboards import show_student_kb, show_tutor_kb, choose_group_kb, lesson_materials, show_start_kb
from TOKEN import Token

bot = telebot.TeleBot(Token.TOKEN)

def register_callback_start(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        if call.data == 'student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_student_kb())
        elif call.data == 'tutor':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_tutor_kb())
        elif call.data == 'schedule_student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=choose_group_kb())
        elif call.data == 'lesson_materials_student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=lesson_materials())
        elif call.data == 'main_menu':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_start_kb())

# def register_callback_student(bot):
#         @bot.callback_query_handler(func=lambda call: True)
#         def callback_handler(call):
#             if call.data == 'schedule_student':
#                 bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
#                                               reply_markup=choose_group_kb())
#             elif call.data == 'lesson_materials_student':
#                 bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=lesson_materials())
#             elif call.data == 'main_menu':
#                 bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
#                                               reply_markup=(show_student_kb()))