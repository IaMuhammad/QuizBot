from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from variables.buttons import inline_but_status_mix, inline_but_status_not_mix, inline_but_status_question, \
    inline_but_status_not_answer
from variables.variables import var_language


def lang_inline_keyboard():
    l = []
    for k, v in var_language.items():
        l.append(InlineKeyboardButton(v, callback_data=v.split()[0]))

    keyboard = InlineKeyboardMarkup(row_width=2).add(*l)
    return keyboard


def status_quiz_inline_keyboard(user):
    l = [
        InlineKeyboardButton(inline_but_status_mix.get(user.lang), callback_data='MIX'),
        InlineKeyboardButton(inline_but_status_not_mix.get(user.lang), callback_data='NOT MIX'),
        InlineKeyboardButton(inline_but_status_question.get(user.lang), callback_data='QUESTIONS'),
        InlineKeyboardButton(inline_but_status_not_answer.get(user.lang), callback_data='ANSWERS')
    ]

    keyboard = InlineKeyboardMarkup(row_width=2).add(*l)
    return keyboard


def time_quiz_inline_keyboard(user):
    l = [
        InlineKeyboardButton('10', callback_data='10'),
        InlineKeyboardButton('15', callback_data='15'),
        InlineKeyboardButton('20', callback_data='20'),
        InlineKeyboardButton('30', callback_data='30'),
        InlineKeyboardButton('60', callback_data='60'),
        InlineKeyboardButton('90', callback_data='90'),
        InlineKeyboardButton('120', callback_data='120'),
        InlineKeyboardButton('180', callback_data='180'),
    ]

    keyboard = InlineKeyboardMarkup(row_width=4).add(*l)
    return keyboard
