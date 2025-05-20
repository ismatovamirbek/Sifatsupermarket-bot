from loader import dp, bot
from data.config import GROUP_ID, ADMINS
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ContentType
from aiogram.dispatcher import FSMContext
from states.complain import ComplainState
from keyboards.inline.complain_confirm import confirm_complain
from keyboards.default.menu_buttons import show_user_menu, request_contact, show_admin_menu


# Murojaat qilish tugmasi bosilganda
@dp.message_handler(text="📨 Murojaat qilish")
async def start_complaint(msg: types.Message):
    await msg.answer(
        "<b>📨 Murojaat yuborish</b>\n\n"
        "🔒 <b>Maxfiylik muhim!</b>\n"
        "Murojaatlaringizni qabul qilishda sizning shaxsiy ma'lumotlaringizni sir saqlashga e'tibor beramiz.\n\n"
        "📝 Murojaatingizni ko‘rib chiqishimiz uchun quyidagi ma’lumotlarni to‘liq va aniq kiriting:\n\n"
        "👤 <b>Iltimos, to‘liq ismingizni kiriting</b> (Ism va familiyangizni albatta to‘liq yozing, masalan: <i>Ali Valiyev</i>) 👇",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )

    await ComplainState.full_name.set()


# Foydalanuvchi to'liq ismini kiritganda
@dp.message_handler(state=ComplainState.full_name)
async def get_full_name(msg: types.Message, state: FSMContext):
    await state.update_data(full_name=msg.text)
    await msg.answer(
        "📞 Telefon raqamingizni qo'lda kiriting yoki pastdagi tugma orqali yuboring:",
        reply_markup=request_contact
    )
    await ComplainState.phone.set()


# Foydalanuvchi telefon raqamini yuborish tugmasini bosganda
@dp.message_handler(content_types=ContentType.CONTACT, state=ComplainState.phone)
async def get_contact_phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.contact.phone_number)
    await msg.answer("📝 Murojaatingizni yozing:", reply_markup=ReplyKeyboardRemove())
    await ComplainState.complain.set()


# Foydalanuvchi telefon raqamini qo'lda kiritganda
@dp.message_handler(state=ComplainState.phone)
async def get_text_phone(msg: types.Message, state: FSMContext):
    phone_number = msg.text.strip()

    # Telefon raqami formatini tekshirish
    if not phone_number.startswith('+998') or not phone_number[1:].isdigit() or len(phone_number) != 13:
        await msg.answer("Iltimos, telefon raqamingizni to‘g‘ri formatda kiriting. Masalan: +998987654321")
        return

    await state.update_data(phone=phone_number)
    await msg.answer("📝 Murojaatingizni yozing:", reply_markup=ReplyKeyboardRemove())
    await ComplainState.complain.set()


# Foydalanuvchi murojaatini kiritganda
@dp.message_handler(state=ComplainState.complain)
async def get_complaint(msg: types.Message, state: FSMContext):
    complaint = msg.text.strip()

    # Murojaat bo‘sh bo‘lmasligi kerak
    if not complaint:
        await msg.answer("❗ Iltimos, murojaatingizni yozing. Bu maydon bo‘sh bo‘lishi mumkin emas.")
        return

    await state.update_data(complain=complaint)
    data = await state.get_data()

    text = (
        f"✅ Ma'lumotlaringiz:\n\n"
        f"👤 Ism: {data['full_name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"🆔 Username: @{msg.from_user.username if msg.from_user.username else 'username yo‘q'}\n"
        f"📝 Murojaat: {data['complain']}\n\n"
        f"❗ Diqqat: Murojaatingiz administratorlar tomonidan ko‘rib chiqiladi.\n"
        f"Shuning uchun iltimos, aniq va o‘ylab yozganingizga ishonch hosil qiling.\n\n"
        f"Mazkur ma'lumotlarni tasdiqlaysizmi?"
    )

    await msg.answer(text, reply_markup=confirm_complain)
    await ComplainState.confirmation.set()


# Foydalanuvchi murojaatini tasdiqlaganda
@dp.callback_query_handler(text="confirm_complain", state=ComplainState.confirmation)
async def confirm_complaint(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    full_name = call.from_user.full_name if call.from_user.full_name else "no full name"
    username = f"@{call.from_user.username}" if call.from_user.username else "username yo'q"

    group_text = (
        f"📩 Yangi murojaat:\n\n"
        f"👤 Ism: {full_name}\n"
        f"📞 Telefon: {data.get('phone', 'no phone')}\n"
        f"🆔 Username: {username}\n"
        f"📝 Murojaat: {data.get('complain', 'no complain')}"
    )

    await bot.send_message(chat_id=GROUP_ID, text=group_text)
    await call.message.delete()

    if call.from_user.id in ADMINS:
        await call.message.answer("✅ Murojaatingiz qabul qilindi. Murojaatingiz kor'ib chiqiladi va sizga javob beriladi", reply_markup=show_admin_menu)
    else:
        await call.message.answer("✅ Murojaatingiz qabul qilindi. Murojaatingiz kor'ib chiqiladi va sizga javob beriladi", reply_markup=show_user_menu)


    await state.finish()


# Foydalanuvchi murojaatini bekor qilganda
@dp.callback_query_handler(text="cancel_complain", state=ComplainState.confirmation)
async def cancel_complaint(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    if call.from_user.id in ADMINS:
        await call.message.answer("❌ Murojaat bekor qilindi.", reply_markup=show_admin_menu)
    else:
        await call.message.answer("❌ Murojaat bekor qilindi.", reply_markup=show_user_menu)

    await state.finish()