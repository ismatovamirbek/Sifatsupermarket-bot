import logging
import aiohttp
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from data.config import API_URL
from keyboards.inline.chanels_btn import get_channel_buttons
from utils.misc import subscription
from loader import bot

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return

        final_status = True

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/botapi/channels/") as response:
                if response.status == 200:
                    channels = await response.json()
                    for ch in channels:
                        ch_id = ch.get("chanel_id")
                        status = await subscription.check(user_id=user, channel=ch_id)
                        final_status *= status
                else:
                    logging.error(f"Kanallarni olishda xatolik: {response.status}")
                    return

        if not final_status:
            result = "🛡 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling."
            try:
                buttons = await get_channel_buttons(user_id=user)
            except Exception as e:
                logging.error(f"Kanallar uchun tugmalarni yaratishda xatolik: {e}")
                buttons = None
            if update.message:
                await update.message.answer(result, reply_markup=buttons)
            elif update.callback_query:
                await update.callback_query.message.answer(result)
            raise CancelHandler()
