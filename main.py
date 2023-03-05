import logging

from aiogram import executor, types

from database.models import User
from keyboards.inline.keyboard import lang_inline_keyboard
from keyboards.keyboards.main_keyboard import main_kb
from loader import dp, bot
from variables.variables import var_greetings
import handlers

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    try:
        user = await User.get(id=str(message.chat.id))
        await message.answer(var_greetings.get(user.lang), reply_markup=main_kb(user))
    except:
        choose = '''
🇺🇿 Tilni tanlang
🇷🇺 Выберите язык
🏴󠁧󠁢󠁥󠁮󠁧󠁿 Choose language
'''
        kb = lang_inline_keyboard()
        await message.answer(choose, reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
