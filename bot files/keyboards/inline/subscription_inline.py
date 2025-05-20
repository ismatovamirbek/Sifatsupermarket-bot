from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

delete_text = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑", callback_data="karzinka")
        ]
    ]
)