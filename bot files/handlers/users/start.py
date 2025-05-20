import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.config import API_URL, ADMINS
from loader import dp
from keyboards.default.menu_buttons import show_user_menu, show_admin_menu


# Botda foydalanuvchi /start tugmasini bosganda apiga saqlanadi
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user = message.from_user

    data = {
        "telegram_id": user.id if user.id else "No telegram_id",
        "first_name": user.first_name if user.first_name else "no first name",
        "last_name": user.last_name if user.last_name else "no last name",
        "username": user.username if user.username else "no username",
    }

    async with aiohttp.ClientSession() as session:
        try:
            # Foydalanuvchini backendga saqlashga harakat qilish
            await session.post(f"{API_URL}/botusers/create/", json=data)

            # Admin yoki oddiy foydalanuvchiligini aniqlash
            if user.id in ADMINS:
                await message.answer("Assalomu alaykum, admin!", reply_markup=show_admin_menu)
            else:
                await message.answer(
                    f"Salom, {user.full_name}! Sifat Supermarketining rasmiy telegram  botiga xush kelibsiz!",reply_markup=show_user_menu
                )

        except Exception as e:
            await message.answer("❌ Backend bilan bog'lanib bo'lmadi.")


