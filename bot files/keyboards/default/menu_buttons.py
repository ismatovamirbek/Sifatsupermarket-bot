from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

show_user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="📄 Vakansiya"),
        ],
        [
            KeyboardButton(text="📨 Murojaat qilish"),
            KeyboardButton(text="🆘 Yordam"),
        ],
        [
            KeyboardButton(text="🤖 Bot haqida"),
        ],
    ],
    resize_keyboard=True
)

show_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="📄 Vakansiya"),
        ],
        [
            KeyboardButton(text="📨 Murojaat qilish"),
            KeyboardButton(text="🆘 Yordam"),
        ],
        [
            KeyboardButton(text="🤖 Bot haqida"),
        ],
        [
            KeyboardButton(text="👥 Users"),
            KeyboardButton(text="📢 Reklama"),
        ]
    ],
    resize_keyboard=True
)


request_contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Raqamni jo'natish", request_contact=True),
        ]
    ],
    resize_keyboard=True
)
