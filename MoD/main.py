
# Импортируем библиотеки для работы с ботом, а также файлы

import telebot
import config
from telebot import types
import database
import subjects


# Создаём объект бот - привязываем его к нашему тг боту через токен
tele_bot = telebot.TeleBot(config.token)


# Получаем локальное поддерево кнопок и ответов, на основе текущего "положения" собеседника
def get_local_database(state):
    temp = subjects.database
    for key in state:
        temp = temp[0][key]

    return temp


def get_reply(state, text):

    temp = get_local_database(state)
    # print(temp)
    markup = types.ReplyKeyboardMarkup()

    try:
        keys = temp[0].keys()
        answer = temp[1]
        for key in keys:
            button = types.KeyboardButton(key)
            markup.row(button)
    except AttributeError:
        keys = temp
        answer = temp

    if(len(state) > 0):
        back = types.KeyboardButton('Назад')
        markup.row(back)
    return markup, answer


def check_text(state, text):

    temp = get_local_database(state)
    # print(temp)
    # result = temp.get(text, default=False)
    if isinstance(temp, str):
        print("Bottom line")
        return False
    try:
        result = temp[0][text]
    except KeyError:
        result = False
    return result


@tele_bot.message_handler(content_types=['text'])
def text_message(message):

    state = database.get_profile(message.chat.id)
    print(message.text)
    print("State: ")
    print(state)
    print("")

    if message.text == subjects.i_am_lucky_caption and len(state) == 0:
        answer = subjects.i_am_lucky()
        tele_bot.send_message(message.chat.id, answer)
        return

    if check_text(state, message.text):
        state.append(message.text)
        print(state)
        database.save_profile(message.chat.id, state)
    else:
        if message.text == "Назад" and len(state) > 0:
            state.pop()
            database.save_profile(message.chat.id, state)
        else:
            print("There is no such key")
            if len(state) > 0:
                tele_bot.send_message(message.chat.id, "Выбери кнопку!", )

                return

    markup, answer = get_reply(state, message.text)
    if len(answer) == 0:
        answer = subjects.start_answer

    tele_bot.send_message(message.chat.id, answer, reply_markup=markup)


tele_bot.polling(none_stop=True)
