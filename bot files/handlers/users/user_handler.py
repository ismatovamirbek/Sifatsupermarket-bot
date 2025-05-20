from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import API_URL, ADMINS
from loader import dp
from keyboards.inline.subscription_inline import delete_text
import requests

PAGE_SIZE = 20  # Har bir sahifada 20 ta foydalanuvchi
API_ENDPOINT = f"{API_URL}/botusers/list/"


def format_user_text(users, page, total_users, start_index=1):
    text = f"📄 Sahifa: {page} | 👥 Jami: {total_users}\n\n"

    for i, user in enumerate(users, start=start_index):
        raw_name = user.get('first_name', '')
        # Unicode bo‘sh joylarni ham hisobga olib, tozalash
        first_name = raw_name.strip()
        first_name = first_name if first_name and not first_name.isspace() else "no first name"

        username = f"@{user['username']}" if user.get('username') else "no username"
        telegram_id = user.get('telegram_id', 'no telegram_id')

        text += (
            f"📍#{i}\n"
            f"🧑‍💼 Name: {first_name}\n"
            f"🆔 Chat ID: {telegram_id}\n"
            f"👤 Username: {username}\n\n"
        )

    return text


def get_navigation_buttons(page, total_users, page_size):
    buttons = []

    if page > 1:
        buttons.append(InlineKeyboardButton(text="«", callback_data=f"users_page:{page - 1}"))

    if page * page_size < total_users:
        buttons.append(InlineKeyboardButton(text="»", callback_data=f"users_page:{page + 1}"))

    return buttons


async def send_users_page(message: types.Message, page: int = 1):
    response = requests.get(API_ENDPOINT)

    if response.status_code != 200:
        await message.answer("❌ API bilan bog‘lanishda xatolik.")
        return

    try:
        users = response.json()
    except Exception:
        await message.answer("❌ JSON format noto‘g‘ri.")
        return

    total_users = len(users)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    paginated_users = users[start:end]

    if not paginated_users:
        await message.answer("❌ Bu sahifada foydalanuvchilar yo‘q.")
        return

    text = format_user_text(paginated_users, page, total_users, start_index=start + 1)

    # Navigatsiya va o‘chirish tugmalarini birlashtirish
    nav_buttons = get_navigation_buttons(page, total_users, PAGE_SIZE)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        nav_buttons,  # Sahifalash
        delete_text.inline_keyboard[0]  # 🗑 O‘chirish tugmasi
    ])

    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(text="👥 Users", user_id=ADMINS)
async def all_users(message: types.Message):
    await message.delete()
    await send_users_page(message, page=1)


@dp.callback_query_handler(lambda c: c.data.startswith("users_page:"))
async def paginate_users(call: types.CallbackQuery):
    page = int(call.data.split(":")[1])
    await call.message.delete()
    await send_users_page(call.message, page)


@dp.callback_query_handler(text="karzinka")  # delete_text tugmasining callback_data
async def handle_delete_button(call: types.CallbackQuery):
    await call.message.delete()