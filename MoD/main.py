
# Импортируем библиотеки для работы с ботом, а также файлы

import telebot
import config
from telebot import types
import profiles
import subjects
import utils

# Создаём объект бот - привязываем его к нашему тг боту через токен
tele_bot = telebot.TeleBot(config.token)


def send_suggestion(message, state):
    text = "Новое предложение темы для курсовой!\n\n"
    text += "Автор темы: " + message.from_user.first_name + " " + message.from_user.last_name + "\n\n"
    text += "Описание темы:\n\n"
    if len(state) == 2:
        text += state[1]
    else:
        text += "Тут должно быть описание темы, но в механике бота что-то пошло не так. Стоит проверть"

    tele_bot.send_message(config.master_id, text)


def suggest_subject(text, state):
    markup = types.ReplyKeyboardMarkup()
    if len(text) > 300:
        reply = "Пожалуйста, сократи объём текста. Не используй более 300 символов"
        return reply, state, markup

    if text == 'Назад':
        state.pop()
        markup, reply = utils.get_reply(state, text)
        return reply, state, markup

    state.append(text)
    reply = "Отлично! Итак, давай проверим, всё ли верно. Вот тема, которую ты хочешь предложить:\n\n"
    reply += text
    reply += "\n\n" + "Всё верно, отправлять на согласование?"

    yes = types.KeyboardButton('Подтвердить')
    no = types.KeyboardButton('Попробовать снова')
    cancel = types.KeyboardButton('Отменить')
    markup.row(yes)
    markup.row(no)
    markup.row(cancel)

    return reply, state, markup


def submit_suggestion(message, state):

    text = message.text
    if text == 'Подтвердить':
        send_suggestion(message, state)
        state.clear()
        markup, reply = utils.get_reply(state, text)
        reply = 'Отлично! Уже отправили разрабам'
    elif text == 'Попробовать снова':
        state.pop()
        markup, reply = utils.get_reply(state, text)
    elif text == 'Отменить':
        state.clear()
        markup, reply = utils.get_reply(state, text)
        reply = 'Ну, что же, ты знаешь, где меня найти, если ты передумаешь :)'
    else:
        markup = types.ReplyKeyboardMarkup()
        reply = "Пожалуйста, выбери одну из кнопок"

    return reply, state, markup


@tele_bot.message_handler(content_types=['text'])
def text_message(message):

    state = profiles.get_profile(message.chat.id)
    print(message.text)
    print("State: ")
    print(state)
    print("")

    if message.text == subjects.i_am_lucky_caption and len(state) == 0:
        answer = subjects.i_am_lucky()
        tele_bot.send_message(message.chat.id, answer)
        return

    if len(state) == 1:
        if state[0] == subjects.suggest_subject_caption:
            reply, state, markup = suggest_subject(message.text, state)
            profiles.save_profile(message.chat.id, state)
            tele_bot.send_message(message.chat.id, reply, reply_markup=markup)
            return
    elif len(state) == 2:
        if state[0] == subjects.suggest_subject_caption:
            reply, state, markup = submit_suggestion(message, state)
            profiles.save_profile(message.chat.id, state)
            tele_bot.send_message(message.chat.id, reply, reply_markup=markup)
            return

    if utils.check_text(state, message.text):
        state.append(message.text)
        print(state)
        profiles.save_profile(message.chat.id, state)
    else:
        if message.text == "Назад" and len(state) > 0:
            state.pop()
            profiles.save_profile(message.chat.id, state)
        else:
            print("There is no such key")
            if len(state) > 0:
                tele_bot.send_message(message.chat.id, "Выбери кнопку!", )
                return

    markup, answer = utils.get_reply(state, message.text)
    # if len(answer) == 0:
    #     answer = subjects.start_answer

    tele_bot.send_message(message.chat.id, answer, reply_markup=markup)


tele_bot.polling(none_stop=True)
