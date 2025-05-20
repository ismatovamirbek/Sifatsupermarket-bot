import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType,InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp
from data.config import GROUP_ID, ADMINS, API_URL
from keyboards.inline.job_btn import (
    vacancy_options, sex_options, family_options, education_options,
    convicted_options, rus_lang_options, job_duration_options,
    confirmation_keyboard, military_certificate_options
)
from keyboards.default.menu_buttons import show_admin_menu, show_user_menu, request_contact
from states.vacancy import Vacancy
import re
import datetime
from data.text import (
    SEX_DICT, FAMILY_DICT, EDU_DICT, CONVICTED_DICT,
    RUS_DICT, DURATION_DICT, VACANCY_DICT
)


# 1. Foydalanuvchi vakansiya tugmasini bosganda
@dp.message_handler(text="📄 Vakansiya")
async def vacancy_start(message: Message, state: FSMContext):
    await message.delete()

    sent_msg = await message.answer(
        "👤 Iltimos, to'liq ism, familiyangiz va otangizning ismini kiriting.\n\n"
        "Masalan: Aliyev Ali Aliyevich", reply_markup=ReplyKeyboardRemove()
    )
    # Shu xabarni saqlab qo'yamiz
    await state.update_data(prompt_msg_id=sent_msg.message_id)
    await Vacancy.fullname.set()

# 1. Foydalanuvchi to'liq ism, familiya va otasining ismini kiritishi
@dp.message_handler(state=Vacancy.fullname)
async def process_fullname(message: Message, state: FSMContext):
    fullname = message.text.strip()
    if len(fullname.split()) < 3:
        await message.answer("❌ Iltimos, to'liq ism, familiya va otangiz ismini to'liq kiriting.")
        return

    # Foydalanuvchi kiritgan xabarni o'chiramiz
    await message.delete()

    # Oldingi prompt xabarni ham o'chiramiz
    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, prompt_msg_id)
        except Exception as e:
            print(f"Xabarni o‘chirishda xatolik: {e}")

    # Yangi bosqich
    await state.update_data(fullname=fullname)
    new_prompt = await message.answer("📞 Iltimos, telefon raqamingizni qo'lda yoki tugma orqali yuboring.", reply_markup=request_contact)
    await state.update_data(prompt_msg_id=new_prompt.message_id)
    await Vacancy.phone.set()


# Yosh tanlash uchun inline tugmalar tayyorlash (misol uchun 18-30 yosh oralig'ida)
def age_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=5)
    buttons = [InlineKeyboardButton(text=str(i), callback_data=f"age_{i}") for i in range(18, 41)]
    keyboard.add(*buttons)
    return keyboard


# CONTACT orqali yuborilgan raqam
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Vacancy.phone)
async def process_phone_contact(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()

    # Eski promptni o'chirish
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    phone_number = message.contact.phone_number
    if not phone_number.startswith("+998"):
        if phone_number.startswith("998"):
            phone_number = "+" + phone_number
        else:
            await message.answer("❌ Telefon raqam formati noto‘g‘ri. Masalan: +998901234567",
                                 reply_markup=ReplyKeyboardRemove())
            return

    if not re.fullmatch(r"^\+998\d{9}$", phone_number):
        await message.answer("❌ Telefon raqam formati noto‘g‘ri. Masalan: +998901234567",
                             reply_markup=ReplyKeyboardRemove())
        return

    await state.update_data(phone=phone_number)

    # Yoshni so'rash uchun inline tugmalar bilan xabar yuborish
    new_prompt = await message.answer(
        "🔢 Iltimos, yoshingizni tanlang.",
        reply_markup=age_keyboard()
    )
    await state.update_data(prompt_msg_id=new_prompt.message_id)
    await Vacancy.age.set()


# QO‘LDA yozilgan raqam
@dp.message_handler(content_types=types.ContentType.TEXT, state=Vacancy.phone)
async def process_phone_text(message: Message, state: FSMContext):
    phone_number = message.text.strip()
    if not phone_number.startswith("+998"):
        if phone_number.startswith("998"):
            phone_number = "+" + phone_number
        else:
            await message.answer("❌ Telefon raqam formati noto‘g‘ri. Masalan: +998901234567")
            return

    if not re.fullmatch(r"^\+998\d{9}$", phone_number):
        await message.answer("❌ Telefon raqam formati noto‘g‘ri. Masalan: +998901234567")
        return

    data = await state.get_data()

    # Eski promptni o'chirish
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    await state.update_data(phone=phone_number)

    # Yoshni so'rash uchun inline tugmalar bilan xabar yuborish
    new_prompt = await message.answer(
        "🔢 Iltimos, yoshingizni tanlang.",
        reply_markup=age_keyboard()
    )
    await state.update_data(prompt_msg_id=new_prompt.message_id)
    await Vacancy.age.set()


@dp.callback_query_handler(lambda c: c.data.startswith("age_"), state=Vacancy.age)
async def process_age_selection(call: CallbackQuery, state: FSMContext):
    age_str = call.data.replace("age_", "")

    if not age_str.isdigit():
        await call.answer("Iltimos, yoshingizni faqat raqam orqali kiriting.", show_alert=True)
        return

    age = int(age_str)

    if age < 18:
        await call.answer("Yosh 18 dan kichik bo‘lishi mumkin emas.", show_alert=True)
        return

    await state.update_data(age=age)

    # Eski promptni o'chirish
    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

    # Jins tanlash xabarini yuborish va yangi prompt_msg_id saqlash
    new_prompt = await call.message.answer("⚧ Iltimos, jinsingizni tanlang.", reply_markup=sex_options)
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.sex.set()
    await call.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("sex_"), state=Vacancy.sex)
async def process_sex_selection(call: CallbackQuery, state: FSMContext):
    sex = call.data.replace("sex_", "")
    await state.update_data(sex=sex)

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")

    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

    new_prompt = await call.message.answer(
        "🏠 Hozirgi yashash manzilingizni kiriting.\nMasalan: Qarshi shahar, Guliston MFY O'zbekiston ko'chasi 88-uy"
    )
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.location.set()
    await call.answer()


# 4. Yashash manzilini kiritish
@dp.message_handler(state=Vacancy.location)
async def process_location(message: Message, state: FSMContext):
    await message.delete()  # Foydalanuvchi xabarini o‘chirish
    location = message.text.strip()

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    if len(location) < 5:
        new_prompt = await message.answer(
            "❌ Manzil juda qisqa. Iltimos, to‘liq yozing.\n"
            "Masalan: Qarshi shahar, Mexanizator bosh ko‘chasi"
        )
        await state.update_data(prompt_msg_id=new_prompt.message_id)
        return

    await state.update_data(location=location)

    new_prompt = await message.answer(
        "📅 Tug‘ilgan sanangizni kiriting (kun.oy.yil), masalan: 25.12.2004"
    )
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.birthday.set()


# 5. Tug‘ilgan sanani kiritish
@dp.message_handler(state=Vacancy.birthday)
async def process_birthday(message: Message, state: FSMContext):
    await message.delete()
    birthday_text = message.text.strip()

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    try:
        # Foydalanuvchi kiritgan sanani tekshiramiz
        birthday = datetime.datetime.strptime(birthday_text, "%d.%m.%Y")
    except ValueError:
        new_prompt = await message.answer(
            "❌ Sana formati noto‘g‘ri.\n"
            "Iltimos, tug‘ilgan sanangizni to‘g‘ri kiriting (kun.oy.yil), masalan: 25.12.2004"
        )
        await state.update_data(prompt_msg_id=new_prompt.message_id)
        return

    # API formatiga mos: YYYY-MM-DD
    birthday_api_format = birthday.strftime("%Y-%m-%d")

    await state.update_data(birthday=birthday_api_format)

    new_prompt = await message.answer("💍 Oilaliymisiz?", reply_markup=family_options)
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.family.set()



# 6. Oilaviy holatni tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("family_"), state=Vacancy.family)
async def process_family(call: CallbackQuery, state: FSMContext):
    family = call.data.replace("family_", "")
    await state.update_data(family=family)

    await call.message.edit_reply_markup()

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    new_prompt = await call.message.answer("🎓 Ma'lumotingizni tanlang:", reply_markup=education_options)
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.education.set()

# 7. Ma'lumotni tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("edu_"), state=Vacancy.education)
async def process_education(call: CallbackQuery, state: FSMContext):
    education = call.data.replace("edu_", "")
    await state.update_data(education=education)

    await call.message.edit_reply_markup()

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    new_prompt = await call.message.answer("⚖️ Sudlanganmisiz?", reply_markup=convicted_options)
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.convicted.set()

# 8. Sudlanganlikni tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("convicted_"), state=Vacancy.convicted)
async def process_convicted(call: CallbackQuery, state: FSMContext):
    convicted = call.data.replace("convicted_", "")
    await state.update_data(convicted=convicted)

    await call.message.edit_reply_markup()

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    new_prompt = await call.message.answer("🇷🇺 Rus tilini bilish darajangizni tanlang:", reply_markup=rus_lang_options)
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.rus_lang.set()

# 9. Rus tilini bilish darajasini tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("rus_lang_"), state=Vacancy.rus_lang)
async def process_rus_lang(call: CallbackQuery, state: FSMContext):
    rus_lang = call.data.replace("rus_lang_", "")
    await state.update_data(rus_lang=rus_lang)

    await call.message.edit_reply_markup()

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    new_prompt = await call.message.answer("🖼️ Iltimos, o'zingizning rasmingizni yuboring.")
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.picture.set()

# Faqat rasmni qabul qiluvchi handler
@dp.message_handler(content_types=ContentType.PHOTO, state=Vacancy.picture)
async def process_picture(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file_id = photo.file_id
    await state.update_data(picture=photo_file_id)

    # Eski promptni o‘chirish
    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    # Keyingi prompt
    new_prompt = await message.answer("✅ Rasmingiz qabul qilindi.\n"
                                      "🔎 Qachon qayerda qancha vaqt ishlagansiz va nima sabab ishdan bo'shagansiz?")
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.previous_job.set()


# Rasm bo'lmagan xabarlar uchun
@dp.message_handler(lambda message: True, state=Vacancy.picture)
async def reject_non_photo(message: Message):
    await message.reply("❌ Iltimos, faqatgina rasm yuboring.")

# 10. Oldingi ish joyi haqida ma'lumot kiritish
@dp.message_handler(state=Vacancy.previous_job)
async def process_previous_job(message: Message, state: FSMContext):
    previous_job_info = message.text.strip()

    if len(previous_job_info) < 5:
        await message.answer("❌ Iltimos, ish joyi va ish tajribangizni batafsil yozing.")
        return

    await state.update_data(previous_job=previous_job_info)

    # Eski prompt xabarni o'chirish
    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    # Yangi prompt yuborish
    new_prompt = await message.answer("💼 Mavjud ish o'rnini tanlang:", reply_markup=vacancy_options)
    await state.update_data(prompt_msg_id=new_prompt.message_id)

    await Vacancy.job.set()

# 11. Ish o'rnini tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("job_"), state=Vacancy.job)
async def process_job_selection(call: CallbackQuery, state: FSMContext):
    job_selected = call.data.replace("job_", "")
    await state.update_data(job=job_selected)

    # Eski prompt xabarni o'chirish
    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except:
            pass


    if job_selected == "oxrana":
        prompt = await call.message.answer("🪖 Harbiy guvohnomangiz bormi?", reply_markup=military_certificate_options)
        await state.update_data(prompt_msg_id=prompt.message_id)
        await Vacancy.military_certificate.set()

    else:
        prompt = await call.message.answer("⏳ Iltimos, Supermarketimizda qancha vaqt ishlash muddatini tanlang.", reply_markup=job_duration_options)
        await state.update_data(prompt_msg_id=prompt.message_id)
        await Vacancy.job_duration.set()


# 12. Harbiy guvohnoma borligini tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("military_"), state=Vacancy.military_certificate)
async def process_military_check(call: CallbackQuery, state: FSMContext):
    certificate_status = call.data.replace("military_", "")
    await state.update_data(military_certificate=certificate_status)

    # Eski prompt xabarni o'chirish
    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except:
            pass

    job_data = data.get("job")

    if certificate_status == "yes":
        await call.message.answer("🪖 Iltimos, harbiy guvohnomangizni fayl yoki rasm sifatida yuboring.")
        await Vacancy.waiting_for_military.set()

    else:
        if job_data == "oxrana":
            await call.message.answer("❌ Oxranalik uchun harbiy guvohnoma talab qilinadi. Arizangiz qabul qilinmadi.", reply_markup=show_user_menu)
            await state.finish()
        else:
            prompt = await call.message.answer("⏳ Iltimos, Supermarketimizda qancha vaqt ishlash muddatini tanlang", reply_markup=job_duration_options)
            await state.update_data(prompt_msg_id=prompt.message_id)
            await Vacancy.job_duration.set()


# 13. Harbiy guvohnoma faylini qabul qilish
@dp.message_handler(content_types=types.ContentType.ANY, state=Vacancy.waiting_for_military)
async def receive_military_certificate_file(message: types.Message, state: FSMContext):
    if message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = "photo"
    else:
        await message.reply("❌ Iltimos, harbiy guvohnomangizni rasm yoki hujjat ko‘rinishida yuboring.")
        return

    await state.update_data(
        military_certificate_id=file_id,
        military_certificate_type=file_type
    )

    prompt = await message.answer("⏳ Iltimos, ishlash muddatini tanlang.", reply_markup=job_duration_options)
    await state.update_data(prompt_msg_id=prompt.message_id)
    await Vacancy.job_duration.set()



# Ishlash muddatini tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("duration_"), state=Vacancy.job_duration)
async def process_job_duration(call: CallbackQuery, state: FSMContext):
    duration = call.data.replace("duration_", "")
    await state.update_data(job_duration=duration)

    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")

    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except Exception:
            pass

    user = call.from_user

    sex = SEX_DICT.get(data.get('sex'), 'Noma\'lum')
    family = FAMILY_DICT.get(data.get('family'), 'Noma\'lum')
    education = EDU_DICT.get(data.get('education'), 'Noma\'lum')
    convicted = CONVICTED_DICT.get(data.get('convicted'), 'Noma\'lum')
    rus_lang = RUS_DICT.get(data.get('rus_lang'), 'Noma\'lum')
    job_position = VACANCY_DICT.get(data.get('job'), 'Noma\'lum')
    job_duration = DURATION_DICT.get(duration, 'Noma\'lum')
    military = "Mavjud" if data.get('military_certificate_id') else "Mavjud emas"
    age = data.get('age', 'Noma\'lum')

    info = (
        f"👤 <b>To‘liq ism:</b> {data.get('fullname')}\n"
        f"📞 <b>Telefon:</b> {data.get('phone')}\n"
        f"📱 <b>Username:</b> @{user.username if user.username else 'yo‘q'}\n"
        f"⚧ <b>Jinsi:</b> {sex}\n"
        f"📍 <b>Yashash joyi:</b> {data.get('location')}\n"
        f"🎂 <b>Tug‘ilgan sana:</b> {data.get('birthday')}\n"
        f"🔢 <b>Yosh:</b> {age}\n"
        f"💍 <b>Oilaviy holat:</b> {family}\n"
        f"🎓 <b>Ma’lumoti:</b> {education}\n"
        f"⚖️ <b>Sudlanganlik:</b> {convicted}\n"
        f"🇷🇺 <b>Rus tili darajasi:</b> {rus_lang}\n"
        f"💼 <b>Tanlangan ish o‘rni:</b> {job_position}\n"
        f"🕒 <b>Ishlash muddati:</b> {job_duration}\n"
        f"🔎 <b>Oldingi ish tajribasi:</b> {data.get('previous_job', 'Mavjud emas')}\n"
        f"🪖 <b>Harbiy guvohnoma:</b> {military}\n"
    )

    await call.message.answer_photo(
        photo=data.get("picture"),
        caption=f"<b>Ma’lumotlaringizni tasdiqlang</b>\n\n{info}",
        reply_markup=confirmation_keyboard,
        parse_mode="HTML"
    )

    await Vacancy.confirmation.set()


@dp.callback_query_handler(lambda c: c.data in ["confirm_yes", "cancel"], state=Vacancy.confirmation)
async def process_confirmation(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = call.from_user

    await call.message.delete()

    prompt_msg_id = data.get("prompt_msg_id")
    if prompt_msg_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=prompt_msg_id)
        except Exception:
            pass

    sex = SEX_DICT.get(data.get('sex'), 'Noma\'lum')
    family = FAMILY_DICT.get(data.get('family'), 'Noma\'lum')
    education = EDU_DICT.get(data.get('education'), 'Noma\'lum')
    convicted = CONVICTED_DICT.get(data.get('convicted'), 'Noma\'lum')
    rus_lang = RUS_DICT.get(data.get('rus_lang'), 'Noma\'lum')
    job_position = VACANCY_DICT.get(data.get('job'), 'Noma\'lum')
    job_duration = DURATION_DICT.get(data.get('job_duration'), 'Noma\'lum')
    age = data.get('age', 'Noma\'lum')

    if call.data == "confirm_yes":
        payload = {
            "telegram_id": user.id,
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "username": user.username if user.username else None,
            "sex": data.get("sex"),
            "location": data.get("location"),
            "birthday": data.get("birthday"),
            "age": age,
            "family": data.get("family"),
            "education": data.get("education"),
            "convicted": data.get("convicted"),
            "rus_lang": data.get("rus_lang"),
            "job": data.get("job"),
            "job_duration": data.get("job_duration"),
            "previous_job": data.get("previous_job"),
            "military_certificate_id": data.get("military_certificate_id"),
            "military_certificate_type": data.get("military_certificate_type"),
            "picture": data.get("picture"),
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{API_URL}/botusers/vacancy-applications/", json=payload) as resp:
                    if resp.status == 201:
                        # Faqat yangi foydalanuvchilar uchun yuboriladi:
                        info = (
                            f"🆕 <b>Yangi ariza:</b>\n\n"
                            f"👤 <b>To‘liq ism:</b> {data.get('fullname')}\n"
                            f"📞 <b>Telefon:</b> {data.get('phone')}\n"
                            f"📱 <b>Username:</b> @{user.username if user.username else 'yo‘q'}\n"
                            f"⚧ <b>Jinsi:</b> {sex}\n"
                            f"📍 <b>Yashash joyi:</b> {data.get('location')}\n"
                            f"🎂 <b>Tug‘ilgan sana:</b> {data.get('birthday')}\n"
                            f"🔢 <b>Yosh:</b> {age}\n"
                            f"💍 <b>Oilaviy holat:</b> {family}\n"
                            f"🎓 <b>Ma’lumoti:</b> {education}\n"
                            f"⚖️ <b>Sudlanganlik:</b> {convicted}\n"
                            f"🇷🇺 <b>Rus tili darajasi:</b> {rus_lang}\n"
                            f"💼 <b>Tanlangan ish o‘rni:</b> {job_position}\n"
                            f"🕒 <b>Ishlash muddati:</b> {job_duration}\n"
                            f"🔎 <b>Oldingi ish tajribasi:</b> {data.get('previous_job', 'Mavjud emas')}\n"
                            f"🪖 <b>Harbiy guvohnoma:</b> {'Mavjud' if data.get('military_certificate_id') else 'Mavjud emas'}\n"
                        )

                        if data.get("picture"):
                            await call.bot.send_photo(
                                chat_id=GROUP_ID,
                                photo=data.get("picture"),
                                caption=info,
                                parse_mode="HTML"
                            )
                        else:
                            await call.bot.send_message(
                                chat_id=GROUP_ID,
                                text=info,
                                parse_mode="HTML"
                            )

                        military_file_id = data.get("military_certificate_id")
                        military_file_type = data.get("military_certificate_type")

                        if military_file_id and military_file_type:
                            if military_file_type == "document":
                                await call.bot.send_document(
                                    chat_id=GROUP_ID,
                                    document=military_file_id,
                                    caption="🪖 Harbiy guvohnoma"
                                )
                            elif military_file_type == "photo":
                                await call.bot.send_photo(
                                    chat_id=GROUP_ID,
                                    photo=military_file_id,
                                    caption="🪖 Harbiy guvohnoma"
                                )

                        response_text = "✅ Ma’lumotlaringiz qabul qilindi. Biz siz bilan aloqaga chiqamiz."
                        markup = show_admin_menu if user.id in ADMINS else show_user_menu
                        await call.message.answer(response_text, reply_markup=markup)
                    elif resp.status == 400:
                        # Ehtimol foydalanuvchi allaqachon topshirgan
                        response_text = "❗️ Siz allaqachon ishga hujjat topshirgansiz. Qayta topshira olmaysiz."
                        markup = show_admin_menu if user.id in ADMINS else show_user_menu
                        await call.message.answer(response_text, reply_markup=markup)
                    else:
                        await call.message.answer("❌ Arizani saqlashda xatolik yuz berdi. Keyinroq urinib ko‘ring.")
            except Exception:
                await call.message.answer("❌ Server bilan bog‘lanishda xatolik yuz berdi. Keyinroq urinib ko‘ring.")

        await state.finish()
    else:
        response_text = "❌ Ariza topshirish bekor qilindi."
        markup = show_admin_menu if user.id in ADMINS else show_user_menu
        await call.message.answer(response_text, reply_markup=markup)
        await state.finish()
