from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.inline.bin_btn import bin_button
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = (
        "📋 <b>Buyruqlar ro‘yxati</b>\n\n"
        "▶️ /start – Botni ishga tushirish\n"
        "ℹ️ /help – Yordam menyusi"
    )
    await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=["help", "yordam"])
@dp.message_handler(text="🆘 Yordam")
async def my_help(message: types.Message):
    await message.delete()
    await message.answer(
        """<b>🆘 Yordam bo‘limi</b>

🔹 <b>1. Biz haqimizda</b> – 🏢 Supermarketimiz haqida batafsil ma’lumot oling.

🔹 <b>2. Vakansiya</b> – 📄 Ishga hujjat topshirish va mavjud bo‘sh ish o‘rinlari bilan tanishing.

🔹 <b>3. Murojaat qilish</b> – ✉️ Taklif, shikoyat yoki savollaringizni bizga yuboring.

🔹 <b>4. Yordam</b> – 🤖 Botdan qanday foydalanishni bosqichma-bosqich o‘rganing.

🔹 <b>5. Bot haqida</b> – 📱 Ushbu botning asosiy imkoniyatlari haqida qisqacha ma’lumot.

——————————————

🙌 Umid qilamizki, ushbu ma’lumotlar sizga foydali bo‘ldi!

🛠 Texnik muammolar yoki takliflar uchun bog‘laning: <a href="https://t.me/amirbek_ismatov">@amirbek_ismatov</a>
        """,
        parse_mode="HTML",
        reply_markup=bin_button
    )

