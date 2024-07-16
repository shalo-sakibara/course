import telebot
from telebot import types
import base_users
from test_lessons import Base_vid
from Token import API_TOKEN

TOKEN = API_TOKEN
bot = telebot.TeleBot(TOKEN)

# Тут каждый делает свою ссылку на файл с видосами
BV = Base_vid('t_lessons.txt')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id, user_name = message.from_user.id, message.from_user.first_name
    if base_users.get_users(user_id, user_name):
        markup = types.ReplyKeyboardMarkup()
        btn1_less = types.KeyboardButton('Уроки по программированию')
        markup.add(btn1_less)
        bot.send_message(
            message.chat.id, "Уже зарегестрированы", protect_content=True, reply_markup=markup)
        # bot.register_next_step_handler(message, lessons)
        bot.register_next_step_handler(message, t_less)

    else:
        bot.send_message(
            message.chat.id, "Регистрация", protect_content=True)
        registr(user_id, user_name)
        if base_users.get_users(user_id, user_name):
            markup = types.ReplyKeyboardMarkup()
            btn1_less = types.KeyboardButton('Уроки по программированию')
            markup.add(btn1_less)
            bot.send_message(
                message.chat.id, "Оплата прошла", protect_content=True, reply_markup=markup)
            # bot.register_next_step_handler(message, lessons)
            bot.register_next_step_handler(message, t_less)

        else:
            bot.send_message(
                message.chat.id, "Возникли проблемы", protect_content=True)


def registr(user_id, user_name):
    """Проверяем оплатил ли он, и потом добавляем в список"""
    if buy_a_course():
        base_users.set_users(user_id, user_name)
        # return 'Вы успешно зарегистрировались на курс'
        return True
    else:
        # return 'Оплата ещё не пришла'
        return False


def buy_a_course():
    # реализовать проверку на оплату
    return True


"""  Метод решения через ссылки
def lessons(message):
    if message.text == 'Уроки по программированию':
        markup = types.InlineKeyboardMarkup()
        less = test_lessons.less()
        for i in less:
            k, v = i, less[i]
            markup.add(types.InlineKeyboardButton(k, url=v))
        bot.send_message(
            message.chat.id, 'Вот все уроки по программированию', reply_markup=markup, protect_content=True)
"""


def t_less(message):
    if message.text == 'Уроки по программированию':
        markup = types.InlineKeyboardMarkup()

        less = BV.get_less('all')
        for i in less:
            name, link = i
            markup.add(types.InlineKeyboardButton(
                name, callback_data=f'{name.split()[0]}'))
        bot.send_message(
            message.chat.id, 'Вот все уроки по программированию', reply_markup=markup, protect_content=True)


# Полностью переделать под обычные видео
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # vid = test_lessons.vidles(int(callback.data))
    if callback.data == "1":
        vid = BV.get_less(1)
        bot.send_message(callback.message.chat.id, vid, protect_content=True)
        return True
    else:
        vid = BV.get_less(2)
        with open(vid, 'rb') as vidi:
            bot.send_video(callback.message.chat.id,
                           vidi, protect_content=True)
            vidi.close()
        return True


bot.polling()
