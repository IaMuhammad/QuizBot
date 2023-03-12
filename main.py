import logging

from aiogram import executor, types

from database.models import User
from keyboards.inline_keyboard import lang_inline_keyboard
from keyboards.main_keyboard import main_kb
from loader import dp
from variables.variables import var_greetings, var_not_working
import handlers

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    try:
        user = await User.get(id=str(message.chat.id))
        await message.answer(var_greetings.get(user.lang), reply_markup=main_kb(user))
    except TypeError as err:
        choose = '''
🇺🇿 Tilni tanlang
🇷🇺 Выберите язык
🏴󠁧󠁢󠁥󠁮󠁧󠁿 Choose languageSorry, our bot is not working properly.
'''
        kb = lang_inline_keyboard()
        await message.answer(choose, reply_markup=kb)
    except:
        s = ''
        for i in var_not_working.values():
            s += i + '\n'
        await message.answer(s)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
