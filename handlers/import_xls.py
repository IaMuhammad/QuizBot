from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup

from database.models import User
from keyboards.main_keyboard import main_kb
from loader import dp, bot
from states import ImportFileState
from variables.buttons import but_back
from variables.variables import var_send_file


@dp.message_handler(Text(contains='📥'))
async def settings(message: Message):
    user = await User.get(str(message.from_user.id))
    mes = var_send_file.get(user.lang)
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(but_back.get(user.lang))
    await message.answer(var_send_file.get(user.lang), reply_markup=kb)

    await ImportFileState.import_state.set()


@dp.message_handler(Text(contains='⬅️'), state=ImportFileState.import_state)
async def settings(message: Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    kb = main_kb(user)
    await message.answer(message.text, reply_markup=kb)
    await state.finish()


@dp.message_handler(lambda m: True, state=ImportFileState.import_state, content_types=[types.ContentType.DOCUMENT])
async def handle_document(message: types.Message):
    document = message.document

    file_id = document.file_id
    file_name = document.file_name

    file = await bot.download_file_by_id(file_id)

    with open(file.file_path, 'r') as f:
        content = f.read()

    await message.reply(f"Received document '{file_name}' with content:\n{content}")

@dp.message_handler(lambda m: True, state=ImportFileState.import_state)
async def settings(message: Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(but_back.get(user.lang))
    mes = var_send_file.get(user.lang)
    await message.answer(mes, reply_markup=kb)
