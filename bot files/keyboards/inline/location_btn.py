from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


location = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Telegram kanal", url="https://t.me/sifatsupermarket"),
            InlineKeyboardButton(text="Instagram sahifa", url="https://www.instagram.com/sifat.supermarket/")
        ],
        [
            InlineKeyboardButton(text="📍 Manzilni ko'rish", callback_data="location")
        ],
        [
            InlineKeyboardButton(text="🗑", callback_data="bin")
        ]
    ]
)