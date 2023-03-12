from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database.models import User
from keyboards.main_keyboard import main_kb
from loader import dp, bot
from states import SettingsState
from variables.variables import var_language_code, var_succesful_edit_lang, var_greetings


@dp.callback_query_handler(lambda callback_query: var_language_code.get(callback_query.data))
async def choose_lang(callback_query: CallbackQuery):
    user = await User.create(id=str(callback_query.from_user.id),
                             first_name=callback_query.from_user.first_name,
                             last_name=callback_query.from_user.last_name,
                             lang=var_language_code.get(callback_query.data))

    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id, var_greetings.get(user.lang), reply_markup=main_kb(user))


@dp.callback_query_handler(lambda callback_query: var_language_code.get(callback_query.data), state=SettingsState.lang)
async def update_lang_settings(callback_query: CallbackQuery, state: FSMContext):
    await User.update(id=str(callback_query.from_user.id), lang=var_language_code.get(callback_query.data))
    user = await User.get(str(callback_query.from_user.id))
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id
    await state.finish()
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id, var_succesful_edit_lang.get(user.lang), reply_markup=main_kb(user))

@dp.callback_query_handler(lambda callback_query: True)
async def update_lang_start(callback_query: CallbackQuery, state: FSMContext):
    await User.update(id=str(callback_query.from_user.id), lang=var_language_code.get(callback_query.data))
    user = await User.get(str(callback_query.from_user.id))
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id
    await state.finish()
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id, var_succesful_edit_lang.get(user.lang), reply_markup=main_kb(user))

