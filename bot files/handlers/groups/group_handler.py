from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsGroup
from loader import dp

@dp.message_handler(IsGroup(), CommandStart())
async def start_group(message: types.Message):
    await message.reply(
        f"👋 *Assalomu alaykum*, {message.from_user.full_name}!\n\n"
        f"📢 *{message.chat.title}* guruhiga xush kelibsiz!\n"
        f"😊 Bu yerda siz yangiliklar, e'lonlar va foydali ma'lumotlarga ega bo‘lasiz.\n\n"
        f"📌 Qoidalarni buzmaslikni unutmang va faol bo‘ling!\n"
        f"✅ Yaxshi kun tilaymiz!",
        parse_mode="Markdown",
    )
