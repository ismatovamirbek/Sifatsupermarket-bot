from aiogram import types

import aiohttp

from data.config import API_URL
from keyboards.inline.chanels_btn import get_channel_buttons
from loader import dp, bot
from utils.misc import subscription



@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()
    user_id = call.from_user.id
    result = ""
    all_subscribed = True

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/botapi/channels/") as response:
            if response.status == 200:
                channels = await response.json()
                for ch in channels:
                    ch_id = ch.get("chanel_id")
                    ch_name = ch.get("chanel_name")
                    try:
                        status = await subscription.check(user_id=user_id, channel=ch_id)
                        channel = await bot.get_chat(ch_id)

                        if status:
                            result += f"✅ <b>{ch_name}</b> kanaliga obuna bo‘lgansiz.\n\n"
                        else:
                            all_subscribed = False
                            result += (f"❌ <b>{ch_name}</b> kanaliga obuna bo‘lmagansiz.\n")
                    except Exception as e:
                        result += f"⚠️ <b>{ch.get('chanel_name')}</b> tekshirib bo‘lmadi: {str(e)}\n\n"
            else:
                result = "❌ Kanallar ro'yxatini olishda xatolik yuz berdi."
                all_subscribed = False

    if all_subscribed:
        result = "🎉 Siz barcha kanallarga obuna bo‘lgansiz!\n\nBotdan foydalanishingiz mumkin ✅"
        await call.message.answer(result, disable_web_page_preview=True)
    else:
        buttons = await get_channel_buttons(user_id=user_id)

        await call.message.answer(result, reply_markup=buttons, disable_web_page_preview=True)
