from loader import dp
from aiogram import types
from keyboards.inline.bin_btn import bin_button


@dp.message_handler(text="🤖 Bot haqida")
async def about_us(message: types.Message):
    full_name = message.from_user.full_name
    username = "amirbek_ismatov"

    await message.delete()
    await message.answer(
        f"""<b>ℹ️ Bot haqida</b>

👋 Assalomu alaykum, <b>{full_name}</b>!
Ushbu bot <b>Sifat Supermarketi</b> tomonidan Qarshi shahridagi mijozlarga yanada qulay xizmat ko‘rsatish maqsadida ishlab chiqilgan.

📲 <b>Bot orqali quyidagi imkoniyatlardan foydalanishingiz mumkin:</b>
• 🏪 Supermarketimiz haqida batafsil ma’lumot olish  
• 📄 Mavjud ish o‘rinlariga hujjat topshirish  
• 📬 Taklif, murojaat va savollarni tez va oson yuborish  
• 🎯 Soddalashtirilgan va tushunarli interfeys

——————————————

👨‍💻 <b>Bot yaratuvchisi:</b> Amirbek Ismatov  
📩 Telegram: <a href="https://t.me/{username}">@{username}</a>

Biz bilan bo‘ling va bizni yanada yaxshilashga yordam bering! 😊
        """,
        parse_mode="HTML",
        reply_markup=bin_button
    )
