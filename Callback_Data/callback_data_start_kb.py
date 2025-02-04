import telebot
import datetime as dt
from Admins.admin_list import admin_id
from Keyboard.keyboards import show_student_kb, show_tutor_kb, choose_group_kb, lesson_materials, show_start_kb
from Show_Week.show_week import send_current_week_message
from TOKEN import Token
from Show_Week.show_week import change_week


bot = telebot.TeleBot(Token.TOKEN)

global_group_id = None

def register_callback_not_handle(bot):
    @bot.message_handler(content_types=['video', 'audio', 'sticker', 'photo', 'document', 'contact', 'emoji'])
    def handle_content_types(message):
        bot.send_message(message.chat.id, f'Бот такое не понимает'

                         f'\nЧто тебе нужно?', reply_markup=choose_group_kb())
def register_callback_start(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['student', 'tutor'])
    def callback_handler(call):
        if call.data == 'student':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_student_kb())
        elif call.data == 'tutor':
            chat_id = call.message.chat.id
            test_tutor = bot.send_message(chat_id, f'Введите индентификатор преподавателя')
            bot.register_next_step_handler(test_tutor, passworld)



def passworld(message):

    if message.from_user.id == 816710725 and message.text == '123123':
        bot.send_message(message.chat.id, f'Вы зашли в качесве преподавателя', reply_markup=show_tutor_kb())
        print(f'Был произведен вход'
              f'{message.from_user.id}')

        return

    else:

        bot.send_message(message.chat.id, f'Вы не препод',
                                  reply_markup=show_student_kb())

        return
            # message = call.message
            # print(message)
            # if message.from_user.id in admin_id:
            #
            #     print(message.from_user.id,admin_id)
            #     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
            #                               reply_markup=show_tutor_kb())
            # else:
            #     print(message.from_user.id, admin_id)
            #     chat_id = call.message.chat.id
            #     bot.send_message(chat_id, f'Вы не препод')
            #     bot.edit_message_reply_markup(chat_id, call.message.message_id,
            #                                   reply_markup=show_student_kb())



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
            # chat_id = call.message.chat.id
            message = call.message
            # chat_id = message.chat.id
            # message_id = message.message_id

            bot.edit_message_text(chat_id = message.chat.id, message_id = call.message.message_id, text ='Вы вернулись в главное меню')
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=show_start_kb())

def register_callback_groups(bot):
    # TODO bug
    @bot.callback_query_handler(func=lambda call: call.data in ['miit', '1273'])
    def wrapped_bot_send_message(call):
        print(f'вызвана wrapped')
        return bot_send_message(call)

@bot.callback_query_handler(func=lambda call: call.data in ['miit', '1273'])
def bot_send_message(call):
    global global_group_id
    today = dt.date.today()
    chat_id = call.message.chat.id
    if call.data == 'miit':
        group_id = 1
        print(f'Вызвана bot_send_message')
        global_group_id = group_id
        return send_current_week_message(today, chat_id, group_id)

    elif call.data == '1273':
        group_id = 2
        print(f'Вызвана bot_send_message')
        global_group_id = group_id
        return send_current_week_message(today, chat_id, group_id)

def handle_callback_group_id(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['miit', '1273'])
    def wrapped_handle_group_id(call):
        print('Вызван wrapped gr id')
        return handle_group_id(call)


def register_callback_switch_week(bot):

    @bot.callback_query_handler(func=lambda call: call.data in ['previous_week', 'current_week', 'next_week'])
    def handle_callback(call):
        call_data = []
        chat_id = call.message.chat.id
        today = dt.date.today()
        print(today)

        if call.data == 'previous_week':
            new_week = change_week(-1)
            send_current_week_message(new_week, chat_id, handle_group_id(call))
            print(f'Вызван pr wekk')


        elif call.data == 'next_week':
            new_week = change_week(1)
            print(f'new week : {new_week}')
            send_current_week_message(new_week, chat_id, handle_group_id(call))
            print(f'выззван next')


        elif call.data == 'current_week':
            test = send_current_week_message(today, chat_id, handle_group_id(call))
            start_of_week = today - dt.timedelta(days=today.weekday())
            end_of_week = start_of_week + dt.timedelta(days=6)
            print(f'test: {test}')
            print(f'Вызван current')

            if test[1] == start_of_week and test[2] == end_of_week:

                print('call data зарегана')
                call_data.append('notification')
                print(call_data[0])

            if call_data[0] == 'notification':

                bot.answer_callback_query(callback_query_id=call.id, text='Вы уже на текущей неделе ')


        else:
            bot.send_message(chat_id, f'Произошла какая то ошибка')
            return


def handle_group_id(call):

    if global_group_id == 1:
        print(global_group_id)
        return 1
    elif global_group_id == 2:
        print(global_group_id)
        return 2


