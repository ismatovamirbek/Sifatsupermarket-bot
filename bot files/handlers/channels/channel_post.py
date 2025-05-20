from aiogram import types

import aiohttp
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import API_URL
from loader import dp
from states.channel_state import AddChannelStates
from data.config import ADMINS
async def send_channel_to_api(chat_id: int, title: str, username: str = None):
    data = {
        "chanel_id": chat_id,
        "chanel_name": title,
        "chanel_username": username
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_URL}/botapi/channels/", json=data) as resp:
                if resp.status == 201:
                    return "✅ Kanal muvaffaqiyatli qo‘shildi!"
                elif resp.status == 400:
                    return "ℹ️ Kanal allaqachon mavjud."
                else:
                    return "❌ Xatolik yuz berdi (API)."
        except Exception as e:
            return "❌ Serverga ulanib bo‘lmadi."


# 1. Start komandasi
@dp.message_handler(commands="addchannel")
async def cmd_add_channel(message: types.Message):
    if not str(message.from_user.id) in ADMINS:
        await message.answer("Siz admin emassiz!")
        return
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="✅ Ha", callback_data="addchannel_yes"),
        InlineKeyboardButton(text="❌ Yo‘q", callback_data="addchannel_no")
    )
    await message.answer("Kanal qo‘shmoqchimisiz?", reply_markup=keyboard)
    await AddChannelStates.waiting_for_confirm.set()


# 2. Tugmalarga javob
@dp.callback_query_handler(lambda c: c.data in ["addchannel_yes", "addchannel_no"],
                           state=AddChannelStates.waiting_for_confirm)
async def process_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "addchannel_yes":
        await callback_query.message.edit_text(
            "Iltimos, kanal ma’lumotlarini quyidagi formatda yuboring:\n\n"
            "Kanal nomi: Mening kanal\n"
            "Kanal id: -1001234567890\n"
            "Kanal user name: @meningkanal"
        )
        await AddChannelStates.waiting_for_channel_data.set()
    else:
        await callback_query.message.edit_text("❌ Bekor qilindi.")
        await state.finish()


# 3. Ma'lumotlarni qabul qilish va jo‘natish
@dp.message_handler(state=AddChannelStates.waiting_for_channel_data)
async def process_channel_data(message: types.Message, state: FSMContext):
    text = message.text

    try:
        # Har bir qatordan qiymatlarni ajratib olamiz
        lines = text.split("\n")
        title_line = next((line for line in lines if "Kanal nomi:" in line), None)
        id_line = next((line for line in lines if "Kanal id:" in line), None)
        username_line = next((line for line in lines if "Kanal user name:" in line), None)

        if not (title_line and id_line and username_line):
            raise ValueError("Kerakli maydon topilmadi.")

        title = title_line.split(":", 1)[1].strip()
        chat_id = int(id_line.split(":", 1)[1].strip())
        username = username_line.split(":", 1)[1].strip().lstrip("@")

        # APIga yuboramiz
        status = await send_channel_to_api(chat_id, title, username)
        await message.answer(status)

    except Exception as e:
        await message.answer(
            "❗ Formatda xatolik bor. Iltimos, quyidagicha yozing:\n\n"
            "Kanal nomi: Mening kanal\n"
            "Kanal id: -1001234567890\n"
            "Kanal user name: @meningkanal"
        )
        return

    await state.finish()
