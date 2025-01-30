import telebot
from Keyboard.keyboards import show_student_kb, show_tutor_kb
from TOKEN import Token

bot = telebot.TeleBot(Token.TOKEN)

def register_callback(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        if call.data == 'student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_student_kb())
        elif call.data == 'tutor':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_tutor_kb())