from aiogram.dispatcher.filters.state import StatesGroup, State

class AddQuizTestState(StatesGroup):
    adding = State()
    quiz = State()
    status = State()
    time = State()

class SettingsState(StatesGroup):
    settings = State()
    lang = State()

class ImportFileState(StatesGroup):
    import_state = State()