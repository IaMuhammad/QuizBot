from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsState(StatesGroup):
    settings = State()
    lang = State()
