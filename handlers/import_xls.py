import pandas
import pandas as pd

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup

from database.models import User, Test, Theme
from keyboards.main_keyboard import main_kb
from loader import dp, bot
from states import ImportFileState
from variables.buttons import but_back, but_import_file
from variables.variables import var_send_file


@dp.message_handler(Text(equals=but_import_file.values()))
async def settings(message: Message):
    user = await User.get(str(message.from_user.id))
    mes = var_send_file.get(user.lang)
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(but_back.get(user.lang))
    await message.answer(var_send_file.get(user.lang), reply_markup=kb)

    await ImportFileState.import_state.set()


@dp.message_handler(Text(equals=but_back.values()), state=ImportFileState.import_state)
async def settings(message: Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    kb = main_kb(user)
    await message.answer(message.text, reply_markup=kb)
    await state.finish()


@dp.message_handler(lambda m: True, state=ImportFileState.import_state, content_types=[types.ContentType.DOCUMENT])
async def handle_document(message: types.Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    document = message.document

    file_id = document.file_id
    file_name = document.file_name

    file = await bot.download_file_by_id(file_id)
    df = pd.read_excel(file, header=None)
    t = q = False
    for index, row in df.iterrows():
        if not pandas.isna(row.values[0]):
            if not t and row.values[0].lower().startswith('theme'):
                t = True
                continue
            if not q and row.values[0].lower().startswith('question'):
                q = True
                continue

            if t and not q:
                theme = await Theme.create(
                    name=row.values[0],
                    status=row.values[1],
                    time=row.values[2],
                    author_id=user.id
                )
            elif q:
                await Test.create(
                    question=row.values[0],
                    options=row.values[1:],
                    answer=0,
                    theme_id=theme.id
                )
    await state.finish()
    await message.reply(f"Received document '{file_name}' and saved test.", reply_markup=main_kb(user))
