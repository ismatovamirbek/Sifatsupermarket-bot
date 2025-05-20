import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import API_URL
from loader import bot


async def get_channel_buttons(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/botapi/channels/") as response:
            if response.status == 200:
                channels = await response.json()
                for channel in channels:
                    channel_id = channel['chanel_id']
                    channel_username = channel['chanel_username']
                    try:
                        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                        if member.status in ['creator', 'administrator', 'member']:
                            continue
                    except:
                        pass

                    btn = InlineKeyboardButton(
                        text=channel['chanel_name'],
                        url=f"https://t.me/{channel_username}"
                    )
                    keyboard.add(btn)
            else:
                keyboard.add(InlineKeyboardButton(text="⚠️ Kanallar topilmadi", callback_data="no_channel"))

            # ✅ Obunani tekshirish tugmasi (callback orqali)
            check_btn = InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subs")
            keyboard.add(check_btn)
    return keyboard
