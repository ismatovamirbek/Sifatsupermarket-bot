from loader import dp
from aiogram import types
from keyboards.inline.location_btn import location
from keyboards.inline.bin_btn import bin_button


# Handler for the "Biz haqimizda" button
@dp.message_handler(text="ℹ️ Biz haqimizda")
async def about_us(message: types.Message):
    await message.delete()
    image = open("images/sifatmarket.jpg", "rb")

    text = """
<b>🛒 Sifat SuperMarket</b> — sizning barcha ehtiyojlaringiz uchun eng yaxshi joy!

📍 <b>Manzil:</b> Qarshi shahar, Mexanizator bosh ko‘chasi
🕖 <b>Ish vaqti:</b> 07:00 - 00:00
📞 <b>Aloqa:</b> 93-933-30-33

📦 Keng assortimentdagi mahsulotlar:
• 🍞 Oziq-ovqat
• 🥤 Ichimliklar
• 🧼 Maishiy tovarlar va boshqalar

🎯 Bizning maqsad — sifatli mahsulotlarni <b>arzon narxlarda</b> taqdim etish!
🛍 Sizni do‘konimizda kutib qolamiz!

📍 <b>Manzilni ko‘rish uchun pastdagi tugmadan foydalaning 👇</b>
"""

    await message.answer_photo(photo=image, caption=text, parse_mode="HTML", reply_markup=location)


# Callback query handler for location button
@dp.callback_query_handler(text="location")
async def send_location(call: types.CallbackQuery):
    latitude = 38.8479434
    longitude = 65.7805849

    await call.message.answer_location(latitude=latitude, longitude=longitude, reply_markup=bin_button)
    await call.answer()