from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from variables.variables import var_language



def lang_inline_keyboard():
    l = []
    for k, v in var_language.items():
        l.append(InlineKeyboardButton(v, callback_data=v.split()[0]))

    keyboard = InlineKeyboardMarkup(row_width=2).add(*l)
    return keyboard
