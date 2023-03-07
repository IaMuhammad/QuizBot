from aiogram.types import ReplyKeyboardMarkup, KeyboardButtonPollType, KeyboardButton

from variables.buttons import but_create, but_my_tests, but_settings, but_import_file, but_change_lang, but_back, \
    but_save, but_quiz


def main_kb(user):
    # poll = KeyboardButtonPollType(type='quiz')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(but_create.get(user.lang)). \
        add(but_my_tests.get(user.lang), but_settings.get(user.lang)). \
        add(but_import_file.get(user.lang))
    return keyboard


def settings_kb(user):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(but_change_lang.get(user.lang)).add(
        but_back.get(user.lang))
    return keyboard


def send_quiz_kb(user):
    poll_button = KeyboardButton(text=but_quiz.get(user.lang), request_poll=KeyboardButtonPollType(type="quiz"))
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(poll_button).add(but_save.get(user.lang))

    return keyboard
