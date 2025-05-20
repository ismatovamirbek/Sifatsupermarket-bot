from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


confirm_complain = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_complain"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_complain")
        ]
    ]
)