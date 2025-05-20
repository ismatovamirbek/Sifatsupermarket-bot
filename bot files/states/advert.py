from aiogram.dispatcher.filters.state import State, StatesGroup

class Advertisement(StatesGroup):
    content = State()
