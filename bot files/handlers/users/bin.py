from loader import dp
from aiogram import types


@dp.callback_query_handler(text="bin")
async def bin_clean(call: types.CallbackQuery):
    await call.message.delete()