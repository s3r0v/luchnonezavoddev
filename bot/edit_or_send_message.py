import os

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from universal_analytics import Tracker, HTTPRequest, HTTPBatchRequest, AsyncHTTPRequest


async def send_to_ga(tg_id, type_, category, action=None):
    http = AsyncHTTPRequest()
    tracker = Tracker(os.getenv("GOOGLE_ID"), http, client_id=f"{tg_id}")
    print(tracker.account, tracker.params, flush=True)
    await tracker.send(type_, category, action)
    await http.session.aclose()


async def edit_or_send_message(bot, message_or_call, state=None, parse_mode='HTML', kb=None, text=None, photo=None, anim=None, chat_id=None, disable_web=False,delete=True):
    message = message_or_call if isinstance(message_or_call, types.Message) else message_or_call.message
    st = await state.get_state()
    value = ((await state.get_data()).get(st.split(":")[-1] if st and st.find(":") else None))
    if not value:
        value = "."
    await send_to_ga(message.chat.id, "pageview", f"{st}={value}!" + (
        str(message_or_call.data) if isinstance(message_or_call, types.CallbackQuery) else ""))
    msg = None
    if photo or anim:
        try:
            msg = await bot.edit_message_caption(
                chat_id=message.chat.id if not chat_id else chat_id,
                message_id=message.message_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=kb,
            )
        except Exception as e:
            if type(e) == MessageNotModified:
                pass
            elif anim:
                await message.delete()
                msg = await bot.send_animation(
                    chat_id=message.chat.id if not chat_id else chat_id,
                    animation=anim,
                    caption=text,
                    parse_mode=parse_mode,
                    reply_markup=kb,
                )
            else:
                try:
                    if delete:
                        await message.delete()
                except:
                    pass
                msg = await bot.send_photo(
                    chat_id=message.chat.id if not chat_id else chat_id,
                    photo=photo,
                    caption=text,
                    parse_mode=parse_mode,
                    reply_markup=kb,
                )
    else:
        try:
            msg = await bot.edit_message_text(
                chat_id=message.chat.id if not chat_id else chat_id,
                message_id=message.message_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=kb,
                disable_web_page_preview=disable_web
            )
        except Exception as e:
            if type(e) == MessageNotModified:
                pass
            else:
                try:
                    if delete:
                        await message.delete()
                except:
                    pass
                msg = await bot.send_message(
                    chat_id=message.chat.id if not chat_id else chat_id,
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=kb,
                    disable_web_page_preview=disable_web
                )
    return msg
