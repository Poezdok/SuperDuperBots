import config
from telebot import types
import profiles
import subjects


# Получаем локальное поддерево кнопок и ответов, на основе текущего "положения" собеседника
def get_local_database(state):
    temp = subjects.database
    for key in state:
        temp = temp[0][key]

    return temp


def get_reply(state):

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

    if len(state) > 0:
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
