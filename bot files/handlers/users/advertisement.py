from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardRemove
import requests
import asyncio
import io

from keyboards.default.menu_buttons import show_admin_menu
from loader import dp, bot
from data.config import API_URL, ADMINS
from states.advert import Advertisement


BATCH_SIZE = 50
advert_contents = {}
advert_message_ids = {}


# Reklama menyusini ko‘rsatish
@dp.message_handler(lambda message: message.from_user.id in ADMINS, text="📢 Reklama")
async def cmd_advert(message: types.Message):
    await message.delete()
    await message.answer("Reklama yuborish xizmati", reply_markup=ReplyKeyboardRemove())

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Ha", callback_data="advert_start_yes"),
        InlineKeyboardButton("❌ Yo'q", callback_data="advert_start_no")
    )

    await message.answer("📢 Reklama yuborishni boshlaysizmi?", reply_markup=markup)


# Reklama yuborishni boshlash yoki bekor qilish
@dp.callback_query_handler(lambda c: c.data in ["advert_start_yes", "advert_start_no"])
async def advert_start_callback_handler(callback_query: types.CallbackQuery):
    admin_id = callback_query.from_user.id

    if admin_id not in ADMINS:
        await callback_query.answer("Sizda ruxsat yo'q!", show_alert=True)
        return

    if callback_query.data == "advert_start_no":
        await callback_query.message.edit_text("❌ Reklama yuborish bekor qilindi.", reply_markup=show_admin_menu)
        return

    await callback_query.message.edit_text("📤 Iltimos, reklama postini yuboring (matn, rasm, video va hokazo):")
    await Advertisement.content.set()


# Reklama kontentini qabul qilish
@dp.message_handler(state=Advertisement.content, content_types=types.ContentType.ANY)
async def process_advert_content(message: types.Message, state: FSMContext):
    admin_id = message.from_user.id
    advert_contents[admin_id] = message

    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"advert_confirm_{admin_id}"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data=f"advert_cancel_{admin_id}")
    )

    sent = await send_advert_content(admin_id, message, markup)
    if sent:
        advert_message_ids[admin_id] = sent.message_id

    await state.finish()


# Reklama kontentini yuboruvchi funksiya
async def send_advert_content(chat_id, message, reply_markup=None):
    content_type = message.content_type
    try:
        if content_type == "text":
            return await bot.send_message(chat_id, message.text, reply_markup=reply_markup)
        elif content_type == "photo":
            return await bot.send_photo(chat_id, message.photo[-1].file_id, caption=message.caption or "",
                                        reply_markup=reply_markup)
        elif content_type == "video":
            return await bot.send_video(chat_id, message.video.file_id, caption=message.caption or "",
                                        reply_markup=reply_markup)
        elif content_type == "document":
            return await bot.send_document(chat_id, message.document.file_id, caption=message.caption or "",
                                           reply_markup=reply_markup)
        elif content_type == "animation":
            return await bot.send_animation(chat_id, message.animation.file_id, caption=message.caption or "",
                                            reply_markup=reply_markup)
        else:
            return await bot.send_message(chat_id, "⚠️ Noma'lum kontent turi", reply_markup=reply_markup)
    except Exception as e:
        print(f"Xatolik kontent yuborishda: {e}")
        return None


# Tugmalar bilan ishlash
@dp.callback_query_handler(lambda c: c.data.startswith(("advert_confirm_", "advert_cancel_", "advert_back_")))
async def advert_callback_handler(callback_query: types.CallbackQuery):
    admin_id = callback_query.from_user.id
    data = callback_query.data

    if "cancel" in data:
        await callback_query.message.edit_text("❌ Reklama bekor qilindi.", reply_markup=show_admin_menu)
        advert_contents.pop(admin_id, None)
        return

    if "confirm" in data:
        await callback_query.answer("Reklama yuborilmoqda...")
        await send_advert_to_all(admin_id, advert_contents.get(admin_id), callback_query.message)
        advert_contents.pop(admin_id, None)


# Reklamani barcha foydalanuvchilarga yuborish
async def send_advert_to_all(admin_id, advert_message, feedback_msg):
    try:
        response = requests.get(f"{API_URL}/botusers/list/", timeout=10)
        response.raise_for_status()
        users = response.json()
    except Exception:
        await feedback_msg.answer("❗ API bilan bog‘lanishda xatolik yuz berdi.")
        return

    sent_count = 0
    error_users = []

    for i in range(0, len(users), BATCH_SIZE):
        for user in users[i:i + BATCH_SIZE]:
            uid = user.get("telegram_id")
            if not uid or uid in ADMINS:
                continue
            try:
                await send_advert_content(uid, advert_message)
                sent_count += 1
            except:
                error_users.append(str(uid))
        await asyncio.sleep(1)

    if error_users:
        error_file = io.BytesIO("\n".join(error_users).encode())
        error_file.name = "error_users.txt"
        await bot.send_document(admin_id, InputFile(error_file),
                                caption="❗ Quyidagi foydalanuvchilarga yuborib bo'lmadi:")

    await feedback_msg.edit_reply_markup()
    await feedback_msg.answer(f"✅ Reklama yuborildi.\nYuborildi: {sent_count}\nXatoliklar: {len(error_users)}",
                              reply_markup=show_admin_menu)
