from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, ContentType

from database.models import User, Theme, Test
from keyboards.main_keyboard import main_kb, send_quiz_kb
from loader import dp
from states import AddQuizTestState
from variables.buttons import but_back, but_create, but_save, but_quiz
from variables.variables import var_send_theme, var_send_quiz, var_recieve_quiz, var_appologize, var_succesful_receive


@dp.message_handler(Text(equals=but_create.values()))
async def settings(message: Message):
    user = await User.get(str(message.from_user.id))
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(but_back.get(user.lang))

    await AddQuizTestState.adding.set()
    await message.answer(var_send_theme.get(user.lang), reply_markup=kb)


@dp.message_handler(Text(equals=but_back.values()), state=AddQuizTestState.adding)
async def settings(message: Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    kb = main_kb(user)
    await message.answer(message.text, reply_markup=kb)
    await state.finish()


@dp.message_handler(lambda m: True, state=AddQuizTestState.adding)
async def send_theme(message: Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    theme = {
        'name': message.text,
        'author_id': str(user.id)
    }
    poll_button = KeyboardButton(text=but_quiz.get(user.lang), request_poll=KeyboardButtonPollType(type="quiz"))
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(poll_button).add(but_save.get(user.lang))

    await AddQuizTestState.quiz.set()
    await state.update_data({'theme': theme, 'quizes': []})
    await message.answer(var_send_quiz.get(user.lang).format(theme=theme.get('name')), reply_markup=kb)


@dp.message_handler(lambda m: True, state=AddQuizTestState.quiz, content_types=[ContentType.POLL])
async def send_theme(message: Message, state: FSMContext):
    user = await User.get(str(message.from_user.id))
    data = await state.get_data()
    poll = message.poll
    options = [i['text'] for i in poll.options]
    quiz = {
        'question': poll.question,
        'options': options,
        'answer': poll.correct_option_id,
    }
    data.get('quizes').append(quiz)
    await state.update_data(quizes=data.get('quizes'))

    kb = send_quiz_kb(user)
    await message.answer(var_recieve_quiz.get(user.lang), reply_markup=kb)


@dp.message_handler(Text(equals=but_save.values()), state=AddQuizTestState.quiz)
async def save_quizes(message: Message, state: FSMContext):
    user = await User.get(id=str(message.from_user.id))
    data = await state.get_data()
    theme = await Theme.create(
        name=data.get('theme').get('name'),
        author_id=data.get('theme').get('author_id')
    )

    for quiz in data.get('quizes'):
        await Test.create(
            question=quiz.get('question'),
            options=quiz.get('options'),
            answer=quiz.get('answer'),
            theme_id=theme.id
        )
    try:
        await state.finish()
        await message.answer(var_succesful_receive.get(user.lang), reply_markup=main_kb(user))
    except:
        await state.reset_state()
        await AddQuizTestState.adding.set()
        kb = ReplyKeyboardMarkup(resize_keyboard=True).add(but_back.get(user.lang))

        await message.answer(var_appologize.user.lang, reply_markup=kb)
