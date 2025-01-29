import telebot
from telebot import types

import Keyboard.keyboards
from TOKEN import Token
from Keyboard import keyboards

bot = telebot.TeleBot(Token.TOKEN)

def register_start(bot):
    @bot.message_handler(commands=['start'])
    def send_start(message):
        bot.send_photo(message.chat.id, photo='https://imgur.com/a/4kg6OIp',
                       caption='Это бот проекта ~V-Air~'
                       f'\n', reply_markup=Keyboard.keyboards.StartKeyboard.show_start_kb())

