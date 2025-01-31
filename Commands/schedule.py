import telebot
from Keyboard.keyboards import choose_group_kb
from TOKEN import Token


bot = telebot.TeleBot(Token.TOKEN)

def register_schedule(bot):
    @bot.message_handler(commands=['schedule'])
    def send_start(message):
        bot.send_message(message.chat.id, text= f'Выбери свою группу', reply_markup=choose_group_kb())

