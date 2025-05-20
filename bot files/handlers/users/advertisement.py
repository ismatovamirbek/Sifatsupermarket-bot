from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from data.config import API_URL, ADMINS
from states.advert import Advertisement
import requests
import asyncio

BATCH_SIZE = 50
advert_contents = {}
advert_message_ids = {}  # admin_id -> message_id


@dp.message_handler(lambda message: message.from_user.id in ADMINS, text="📢 Reklama")
async def cmd_advert(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Ha", callback_data="advert_start_yes"),
        InlineKeyboardButton("❌ Yo'q", callback_data="advert_start_no")
    )
    await message.answer("📢 Reklama yuborishni boshlaysizmi?", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data in ["advert_start_yes", "advert_start_no"])
async def advert_start_callback_handler(callback_query: types.CallbackQuery):
    admin_id = callback_query.from_user.id

    if admin_id not in ADMINS:
        await callback_query.answer("Sizda ruxsat yo'q!", show_alert=True)
        return

    if callback_query.data == "advert_start_no":
        await callback_query.message.edit_text("❌ Reklama yuborish bekor qilindi.")
        await callback_query.answer()
        return

    await callback_query.message.edit_text("📤 Iltimos, reklama postini yuboring (matn, rasm, video va hokazo):")
    await Advertisement.content.set()
    await callback_query.answer()


@dp.message_handler(state=Advertisement.content, content_types=types.ContentType.ANY)
async def process_advert_content(message: types.Message, state: FSMContext):
    admin_id = message.from_user.id
    advert_contents[admin_id] = message

    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"advert_confirm_{admin_id}"))
    markup.insert(InlineKeyboardButton("❌ Bekor qilish", callback_data=f"advert_cancel_{admin_id}"))

    m = message
    sent = None
    if m.content_type == "text":
        sent = await message.answer(m.text, reply_markup=markup)
    elif m.content_type == "photo":
        sent = await message.answer_photo(m.photo[-1].file_id, caption=m.caption or "", reply_markup=markup)
    elif m.content_type == "video":
        sent = await message.answer_video(m.video.file_id, caption=m.caption or "", reply_markup=markup)
    elif m.content_type == "document":
        sent = await message.answer_document(m.document.file_id, caption=m.caption or "", reply_markup=markup)
    elif m.content_type == "animation":
        sent = await message.answer_animation(m.animation.file_id, caption=m.caption or "", reply_markup=markup)
    else:
        sent = await message.answer("⚠️ Reklama uchun noma'lum kontent turi.", reply_markup=markup)

    # Saqlab qolamiz, keyin o‘chirish uchun
    if sent:
        advert_message_ids[admin_id] = sent.message_id

    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith(("advert_confirm_", "advert_cancel_")))
async def advert_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    admin_id = callback_query.from_user.id

    if admin_id not in ADMINS:
        await callback_query.answer("Sizda ruxsat yo'q!", show_alert=True)
        return

    prefix, callback_admin_id = data.split("_")[0], int(data.split("_")[-1])
    if admin_id != callback_admin_id:
        await callback_query.answer("Bu reklama sizga tegishli emas!", show_alert=True)
        return

    if prefix == "advert_cancel":
        await callback_query.message.edit_text("❌ Reklama bekor qilindi.")
        if admin_id in advert_contents:
            advert_contents.pop(admin_id)
        if admin_id in advert_message_ids:
            try:
                await bot.delete_message(chat_id=admin_id, message_id=advert_message_ids[admin_id])
            except:
                pass
            advert_message_ids.pop(admin_id, None)
        await callback_query.answer("Reklama bekor qilindi.")
        return

    await callback_query.answer("Reklama yuborilmoqda...")

    try:
        response = requests.get(f"{API_URL}/botusers/list/", timeout=5)
        response.raise_for_status()
        users = response.json()
    except Exception:
        await callback_query.answer("API dan foydalanuvchilarni olishda xatolik!", show_alert=True)
        return

    advert_message = advert_contents.get(admin_id)
    if not advert_message:
        await callback_query.answer("Reklama kontenti topilmadi!", show_alert=True)
        return

    count = 0
    error_count = 0
    total_users = len(users)

    for i in range(0, total_users, BATCH_SIZE):
        batch = users[i:i + BATCH_SIZE]
        for user in batch:
            uid = user.get("telegram_id")
            if uid in ADMINS:
                continue
            try:
                m = advert_message
                if m.content_type == "text":
                    await bot.send_message(uid, m.text)
                elif m.content_type == "photo":
                    await bot.send_photo(uid, m.photo[-1].file_id, caption=m.caption or "")
                elif m.content_type == "video":
                    await bot.send_video(uid, m.video.file_id, caption=m.caption or "")
                elif m.content_type == "document":
                    await bot.send_document(uid, m.document.file_id, caption=m.caption or "")
                elif m.content_type == "animation":
                    await bot.send_animation(uid, m.animation.file_id, caption=m.caption or "")
                else:
                    await bot.send_message(uid, "📢 Reklama kontenti")
                count += 1
            except Exception:
                error_count += 1
        await asyncio.sleep(1)

    # Kontent chiqgan xabarni o‘chiramiz
    if admin_id in advert_message_ids:
        try:
            await bot.delete_message(chat_id=admin_id, message_id=advert_message_ids[admin_id])
        except:
            pass
        advert_message_ids.pop(admin_id, None)

    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer(
        f"✅ Reklama yuborildi.\n"
        f"Yuborilgan foydalanuvchilar: {count}\n"
        f"Xatoliklar: {error_count}"
    )
    advert_contents.pop(admin_id, None)
