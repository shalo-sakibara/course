import telebot
from telebot import types
import base_users
from test_lessons import Base_vid
from private_data import *

TOKEN = API_TOKEN
bot = telebot.TeleBot(TOKEN)
BV = Base_vid(link_to_the_video_file, path_to_dir_lessons)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id, user_name = message.from_user.id, message.from_user.first_name
    if base_users.get_users(user_id, user_name):
        markup = types.ReplyKeyboardMarkup()
        btn1_less = types.KeyboardButton('Уроки по программированию')
        markup.add(btn1_less)
        bot.send_message(
            message.chat.id, "Уже зарегестрированы", protect_content=True, reply_markup=markup)
        return True
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

        else:
            bot.send_message(
                message.chat.id, "Возникли проблемы", protect_content=True)

        return True


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    admin_id, admin_name = message.from_user.id, message.from_user.first_name
    admin_funcs = ['Добавить урок в список', 'Удаление урока из списка',
                   'Изменить название урока', 'Заменить видео в уроке']
    if admin_id in admins.keys() and admins[admin_id] == admin_name:
        markup = types.ReplyKeyboardMarkup()
        for name_func in admin_funcs:
            btn_less = types.KeyboardButton(name_func)
            markup.add(btn_less)
        bot.send_message(
            message.chat.id, 'Вот ваша панель управления курсом', protect_content=True, reply_markup=markup)
        return True
    else:
        bot.send_message(
            message.chat.id, "Вас нет в списке администраторов", protect_content=True)
        return False


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


@bot.message_handler()
def distribution(message):
    # Вызывает функции администраторов в зависимости от сообщения
    id_chat = message.chat.id
    mes_txt = message.text
    user_id, user_name = message.from_user.id, message.from_user.first_name
    if user_id in admins.keys() and admins[user_id] == user_name:
        funcs = {'Уроки по программированию': ['Запуск от администратора', t_less],
                 'Добавить урок в список': [
            'Введите: Отправьте видео с его названием', add_vid],
            'Удаление урока из списка': ['Введите номер урока', del_vid],
            'Изменить название урока': ['Введите номер урока и его новое название, через пробел', edit_vid],
            'Заменить видео в уроке': ['Отправьте новое видео указав номер урока', edit_vid]}
        if mes_txt in funcs.keys():
            bot.send_message(
                id_chat, funcs[mes_txt][0], protect_content=True)
            # funcs[mes_txt][1](message)
            bot.register_next_step_handler(message, funcs[mes_txt][1])
        return True
    else:
        funcs = {'Уроки по программированию': t_less}
        if mes_txt in funcs.keys():
            funcs[mes_txt](message)
        return True


def add_vid(message):
    name = message.caption
    # Получаем файл видео
    file_info = bot.get_file(message.video.file_id)
    # Скачиваем файл
    downloaded_file = bot.download_file(file_info.file_path)
    BV.set_less(name, downloaded_file)
    bot.reply_to(message, "Видео успешно загружино на курс!")
    return True


def edit_vid(message):
    number, name = message.text.split()
    BV.edit_name_less(number=int(number), new_name=name)
    bot.reply_to(message, "Название видео изменено")
    # print('Изменение')
    # print(message.text)
    # print('Считывание текста, или видео')
    return True


def del_vid(message):
    if BV.del_less(int(message.text)):
        bot.reply_to(message, 'Видео удалено')
    else:
        bot.reply_to(message, 'Видео с данным номером не найдено')
    return True


def t_less(message):
    # Создается список уроков и отпавляется
    markup = types.InlineKeyboardMarkup()
    less = BV.get_less('all')
    for i in less:
        number = i
        name = less[i][0]
        markup.add(types.InlineKeyboardButton(
            f"{number}) {name}", callback_data=f'{number}'))
    bot.send_message(message.chat.id, 'Вот все уроки по программированию',
                     reply_markup=markup, protect_content=True)
    return True


@ bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    name, vid = BV.get_less(int(callback.data))
    with open(vid, 'rb') as vidi:
        bot.send_video(callback.message.chat.id,
                       vidi, protect_content=True, caption=name)
        vidi.close()
    return True


bot.polling()
