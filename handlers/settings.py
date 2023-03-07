from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from database.models import User
from keyboards.inline_keyboard import lang_inline_keyboard
from keyboards.main_keyboard import settings_kb, main_kb
from loader import dp
from states import SettingsState
from variables.buttons import but_settings, but_change_lang, but_back
from variables.variables import var_choose_lang




@dp.message_handler(Text(equals=but_settings.values()))
async def settings(message: Message):
    user = await User.get(str(message.from_user.id))
    kb = settings_kb(user)
    await SettingsState.settings.set()
    await message.answer(message.text, reply_markup=kb)


@dp.message_handler(Text(equals=but_change_lang.values()), state=SettingsState.settings)
async def settings(message: Message):
    await SettingsState.lang.set()
    user = await User.get(str(message.from_user.id))
    mes = var_choose_lang.get(user.lang)
    kb = lang_inline_keyboard()
    await message.answer(mes, reply_markup=kb)


@dp.message_handler(Text(equals=but_back.values()), state=SettingsState.settings)
async def settings(message: Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    kb = main_kb(user)
    await message.answer(message.text, reply_markup=kb)
    await state.finish()
