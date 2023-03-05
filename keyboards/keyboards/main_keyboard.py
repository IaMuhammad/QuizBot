from aiogram.types import ReplyKeyboardMarkup, KeyboardButtonPollType, KeyboardButton

from variables.buttons import var_create, var_my_tests, var_settings, var_import_file, var_change_lang, var_back


def main_kb(user):
    # poll = KeyboardButtonPollType(type='quiz')
    poll_button = KeyboardButton(text="Take a poll", request_poll=KeyboardButtonPollType(type="quiz"))
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(var_create.get(user.lang)). \
        add(var_my_tests.get(user.lang), var_settings.get(user.lang)). \
        add(var_import_file.get(user.lang)).add(poll_button)
    return keyboard


def settings_kb(user):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(var_change_lang.get(user.lang)).add(
        var_back.get(user.lang))
    return keyboard
