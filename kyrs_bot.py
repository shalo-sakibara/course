import telebot
from telebot import types
import base_users
from test_lessons import Base_vid
from private_data import *
import base_video as bv

TOKEN = API_TOKEN
bot = telebot.TeleBot(TOKEN)


def btn_user(role):
    admin_funcs = ['Уроки', 'Добавить урок в список', 'Удаление урока из списка',
                   'Изменить название урока', 'Заменить видео в уроке']
    if role == 'admin':
        markup = types.ReplyKeyboardMarkup()
        for name_func in admin_funcs:
            btn_less = types.KeyboardButton(name_func)
            markup.add(btn_less)
        return markup
    else:
        markup = types.ReplyKeyboardMarkup()
        btn1_less = types.KeyboardButton('Уроки по программированию')
        markup.add(btn1_less)
        pass


@bot.message_handler(commands=['start'])
def send_welcome(message):

    user_id, user_name = message.from_user.id, message.from_user.first_name
    if user_id in admins.keys() and user_name in admins.values():
        bot.send_message(
            message.chat.id, f'Приветствую, {user_name}', protect_content=True, reply_markup=btn_user('admin'))

    elif base_users.get_users(user_id, user_name):
        bot.send_message(
            message.chat.id, f"Приветствую {user_name}", protect_content=True, reply_markup=btn_user('user'))
        return True
    else:
        bot.send_message(
            message.chat.id, "Регистрация", protect_content=True)
        registr(user_id, user_name)
        if base_users.get_users(user_id, user_name):
            bot.send_message(
                message.chat.id, "Оплата прошла", protect_content=True, reply_markup=btn_user('user'))

        else:
            bot.send_message(
                message.chat.id, "Возникли проблемы", protect_content=True)

        return True


def registr(user_id, user_name):
    """Проверяем оплатил ли он, и потом добавляем в список"""
    if buy_a_course():
        base_users.set_users(user_id, user_name)
        return True
    else:
        return False


def buy_a_course():
    # реализовать проверку на оплату
    return True


@bot.message_handler()
def distribution(message):
    id_chat = message.chat.id
    mes_txt = message.text
    user_id, user_name = message.from_user.id, message.from_user.first_name
    if user_id in admins.keys() and admins[user_id] == user_name:
        funcs = {'Уроки': [t_less],
                 'Добавить урок в список': [
            'Введите: Отправьте видео с его названием', add_vid],
            'Удаление урока из списка': ['Введите номер урока', del_vid],
            'Изменить название урока': ['Введите номер урока и его новое название, через пробел', edit_vid],
            'Заменить видео в уроке': ['Отправьте новое видео указав номер урока', edit_vid]}
        if mes_txt in funcs.keys():
            if len(funcs[mes_txt]) > 1:
                bot.send_message(
                    id_chat, funcs[mes_txt][0], protect_content=True)
                bot.register_next_step_handler(message, funcs[mes_txt][1])
            else:
                bot.register_next_step_handler(message, funcs[mes_txt][0])
        return True
    else:
        funcs = {'Уроки по программированию': t_less}
        if mes_txt in funcs.keys():
            funcs[mes_txt](message)
        return True


def add_vid(message):
    mess = message.caption
    mess = mess.split()
    # Получаем файл видео
    file_info = bot.get_file(message.video.file_id)
    # Скачиваем файл
    downloaded_file = bot.download_file(file_info.file_path)
    path_name = ''.join(mess[1:])
    path_file = f'{path_to_dir_lessons}/{path_name}'
    bv.write_video(path_file, downloaded_file)
    path_file = path_file.replace('/', '\\')
    id = int(mess[0])
    name = ' '.join(mess[1:])
    bv.set_less(id, name, path_file + '.mp4')
    bot.reply_to(message, "Видео успешно загружино на курс!")
    return True


def edit_vid(message):
    mess = message.text.split()
    number, name = mess[0], ' '.join(mess[1:])
    bv.edit_less(id=int(number), name=name, link=None)
    bot.reply_to(message, "Название видео изменено")

    return True


def del_vid(message):
    if bv.del_less(int(message.text)):
        bot.reply_to(message, 'Видео удалено')
    else:
        bot.reply_to(message, 'Видео с данным номером не найдено')
    return True


def t_less(message):
    # Создается список уроков и отпавляется пользователю
    markup = types.InlineKeyboardMarkup()
    less = bv.get_less(0)
    for i in less:
        number = i[0]
        name = i[1]
        markup.add(types.InlineKeyboardButton(
            f"{number}) {name}", callback_data=f'{number}'))
    bot.send_message(message.chat.id, 'Вот все уроки по программированию',
                     reply_markup=markup, protect_content=True)
    return True


@ bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    name, vid = bv.get_less(int(callback.data))
    with open(vid, 'rb') as vidi:
        bot.send_video(callback.message.chat.id,
                       vidi, protect_content=True, caption=name)
        vidi.close()
    return True


bot.polling()
