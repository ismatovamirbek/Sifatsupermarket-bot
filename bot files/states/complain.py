from aiogram.dispatcher.filters.state import State, StatesGroup


class ComplainState(StatesGroup):
    full_name = State()
    phone = State()
    complain = State()
    confirmation = State()