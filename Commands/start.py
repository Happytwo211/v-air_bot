import telebot
from TOKEN import Token
from Keyboard.keyboards import show_start_kb
from Show_tutors_mat.tutor import show_group_by_date

bot = telebot.TeleBot(Token.TOKEN)

def register_start(bot):
    @bot.message_handler(commands=['start'])
    def send_start(message):
        bot.send_photo(message.chat.id, photo='https://imgur.com/a/4kg6OIp',
                       caption='Это бот проекта ~V-Air~'
                       f'\n', reply_markup=show_start_kb())


def test_11(bot):
    @bot.message_handler(commands=['test'])
    def handle(message):
        bot.register_next_step_handler(message, show_group_by_date)

