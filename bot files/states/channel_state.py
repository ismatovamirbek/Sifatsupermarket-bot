from aiogram.dispatcher.filters.state import State, StatesGroup

class AddChannelStates(StatesGroup):
    waiting_for_confirm = State()
    waiting_for_channel_data = State()
