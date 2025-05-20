from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑", callback_data="bin"),
        ]
    ]
)