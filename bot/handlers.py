import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, InputFile
from bot.modules import texts, keyboards
from bot.load_all import bot, dp
from bot.modules.filters import Button
from bot.modules.state import UserState
from .modules.MetricsTOJPEG.MTJ import MetricsToPDF

MtP = MetricsToPDF()

from bot.edit_or_send_message import edit_or_send_message


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await UserState.start.set()
    await state.update_data(
        {"messegeToDelete": message.message_id}
    )
    await edit_or_send_message(bot, message, state=state, text=await texts.menu(), kb=keyboards.start_menu,
                               disable_web=True)


@dp.callback_query_handler(Button("start_game"), state="*")
async def set_name(call: CallbackQuery, state: FSMContext):
    msg: types.Message = await edit_or_send_message(bot, call, state=state, text=await texts.set_name(),
                                                    kb=keyboards.reply_main,
                                                    disable_web=True)
    await state.update_data(
        {"messegeToDelete": msg.message_id}
    )
    await UserState.name.set()
    await call.answer()


@dp.callback_query_handler(Button("rules"), state="*")
async def rule(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.rule(),
                               kb=keyboards.back_from_the_rules, disable_web=True)
    await call.answer()


@dp.callback_query_handler(Button("backRules"), state="*")
async def backRule(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await start(call.message, state)
    await call.answer()


# Reply MENU    ["⭐️Главное меню"],["📢 Поделиться"],["🤖 О боте"]
@dp.message_handler(Text(equals="⭐️Главное меню"), state="*")
async def reply_main_menu(message: types.Message, state: FSMContext):
    await state.update_data(
        {"reply": "menu"}
    )
    await bot.send_message(chat_id=message.chat.id, text=await texts.exit(), reply_markup=keyboards.yes_or_no)
    await message.delete()


@dp.message_handler(Text(equals="📢 Поделиться"), state="*")
async def reply_share(message: types.Message, state: FSMContext):
    await state.update_data(
        {"reply": "share"}
    )
    await bot.send_message(chat_id=message.chat.id, text=await texts.exit(), reply_markup=keyboards.yes_or_no)
    await message.delete()


@dp.message_handler(Text(equals="🤖 О боте"), state="*")
async def reply_info(message: types.Message, state: FSMContext):
    await state.update_data(
        {"reply": "info"}
    )
    await bot.send_message(chat_id=message.chat.id, text=await texts.exit(), reply_markup=keyboards.yes_or_no)
    await message.delete()


@dp.callback_query_handler(Button("yes"), state="*")
async def yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    reply = data['reply']
    delete = int(data['messegeToDelete'])
    print(reply, flush=True)
    try:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=delete)
    except:
        pass
    if reply == "menu":
        await start(call.message, state)
    elif reply == "share":
        await share(call.message, state)
    else:
        await info_set(call.message, state)
    await call.answer()


@dp.callback_query_handler(Button("no"), state="*")
async def no(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer()


# Share BOT
async def share(message: types.Message, state: FSMContext):
    msg = await edit_or_send_message(bot, message, state=state, text=await texts.share_bot(bot),
                                     kb=keyboards.back_from_the_rules,
                                     disable_web=False,
                                     delete=False)
    await state.update_data(
        {"messegeToDelete": msg.message_id}
    )


# INFO
async def info_set(message: types.Message, state: FSMContext):
    msg = await edit_or_send_message(bot, message, state=state, text="Какую информацию вы хотите узнать?",
                                     kb=keyboards.info,
                                     disable_web=False,
                                     delete=False)
    await state.update_data(
        {"messegeToDelete": msg.message_id}
    )


@dp.callback_query_handler(Button("creators"), state="*")
async def creators(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.creators(), kb=keyboards.back_from_the_rules,
                               disable_web=True)
    await call.answer()


@dp.callback_query_handler(Button("users"), state="*")
async def users(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.users(), kb=keyboards.back_from_the_rules,
                               disable_web=True)
    await call.answer()


@dp.callback_query_handler(Button("link"), state="*")
async def link(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.link(), kb=keyboards.back_from_the_rules,
                               disable_web=True)
    await call.answer()


@dp.message_handler(state=UserState.name)
async def set_avatar(message: types.Message, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": message.message_id}
    )
    await state.update_data(
        {"name": message.text}
    )
    await state.update_data(
        {"Respect_for_colleagues": 25,
         "Students_love": 25,
         "Loyalty_to_the_administration": 25}
    )
    msg = await edit_or_send_message(bot, message, state=state, text=await texts.set_pers(), kb=keyboards.set_pers,
                                     disable_web=True,
                                     delete=False)
    await state.update_data(
        {"messegeToDelete": msg.message_id}
    )
    await UserState.pers.set()


@dp.callback_query_handler(state=UserState.pers)
async def start_act_1(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"pers": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.start_act_1(), kb=keyboards.act1,
                               disable_web=True)
    await UserState.act1.set()
    await call.answer()


@dp.callback_query_handler(Button("act1"), state=UserState.act1)
async def act1(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.act1(state), kb=keyboards.next,
                               disable_web=True)
    await UserState.recruiting_method.set()
    await call.answer()


# Screen 7
@dp.callback_query_handler(Button("next"), state=UserState.recruiting_method)
async def recruiting_method(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.recruiting_method(state),
                               kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


@dp.callback_query_handler(state=UserState.recruiting_method)
async def set_rec1(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"recruiting_method": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_recruiting_method(), kb=keyboards.next,
                               disable_web=True)
    await UserState.positions_of_people.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.positions_of_people)
async def set_recruiting_method(call: CallbackQuery, state: FSMContext):
    await edit_or_send_message(bot, call, state=state, text=await texts.positions_of_people(state),
                               kb=keyboards.positions_of_people,
                               disable_web=True)
    await call.answer()


# Screen 9
@dp.callback_query_handler(state=UserState.positions_of_people)
async def set_pers1(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"positions_of_people": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_positions_of_people(), kb=keyboards.next,
                               disable_web=True)
    await UserState.strategy.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.strategy)
async def set_pers1(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.strategy(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen 11
@dp.callback_query_handler(state=UserState.strategy)
async def set_pers1(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"strategy": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_strategy(), kb=keyboards.next,
                               disable_web=True)
    await UserState.tactics.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.tactics)
async def tactics(call: CallbackQuery, state: FSMContext):
    await edit_or_send_message(bot, call, state=state, text=await texts.tactics(state), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen 13
@dp.callback_query_handler(state=UserState.tactics)
async def set_tactics(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"tactics": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 0,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_tactics(), kb=keyboards.next,
                               disable_web=True)
    await UserState.delete_item.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.delete_item)
async def delete_item(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.delete_item(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen 15
@dp.callback_query_handler(state=UserState.delete_item)
async def set_delete_item(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"delete_item": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.end_act1(), kb=keyboards.act2, disable_web=True)
    if data['pers'] == "Творческого объединения":
        await UserState.TO.set()
    elif data['pers'] == "Совета по качечтву обучения":
        await UserState.KO.set()
    else:
        await UserState.CC.set()
    await call.answer()


@dp.callback_query_handler(Button("act2"), state=UserState.TO)
async def organizers(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.organizers(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen TO-17
@dp.callback_query_handler(state=UserState.TO)
async def set_organizers(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"organizers": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_organizers(), kb=keyboards.next,
                               disable_web=True)
    await UserState.inactive.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.inactive)
async def inactive(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.inactive(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen TO 19
@dp.callback_query_handler(state=UserState.inactive)
async def set_inactive(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"inactive": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 0,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 0}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_inactive(), kb=keyboards.next,
                               disable_web=True)
    await UserState.strange_number.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.strange_number)
async def strange_number(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.strange_number(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen TO 21
@dp.callback_query_handler(state=UserState.strange_number)
async def set_strange_number(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"strange_number": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 0,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_strange_number(), kb=keyboards.next,
                               disable_web=True)
    await UserState.artistic_director.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.artistic_director)
async def artistic_director(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.artistic_director(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen TO 23
@dp.callback_query_handler(state=UserState.artistic_director)
async def set_artistic_director(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"artistic_director": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_artistic_director(), kb=keyboards.next,
                               disable_web=True)
    await UserState.muslim.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.muslim)
async def muslim(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.muslim(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen TO 25
@dp.callback_query_handler(state=UserState.muslim)
async def set_muslim(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"muslim": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_muslim(), kb=keyboards.next,
                               disable_web=True)
    await UserState.striptease.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.striptease)
async def striptease(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.striptease(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen TO 27
@dp.callback_query_handler(state=UserState.striptease)
async def set_striptease(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"striptease": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_striptease(), kb=keyboards.act3,
                               disable_web=True)
    await UserState.act3.set()
    await call.answer()


# ---------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(Button("act2"), state=UserState.CC)
async def bell(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.bell(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen CC-17
@dp.callback_query_handler(state=UserState.CC)
async def set_bell(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"bell": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_bell(), kb=keyboards.next, disable_web=True)
    await UserState.discrimination.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.discrimination)
async def discrimination(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.discrimination(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen CC 19
@dp.callback_query_handler(state=UserState.discrimination)
async def set_discrimination(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"discrimination": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_discrimination(), kb=keyboards.next,
                               disable_web=True)
    await UserState.interview.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.interview)
async def interview(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.interview(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen CC 21
@dp.callback_query_handler(state=UserState.interview)
async def set_interview(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"interview": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_interview(), kb=keyboards.next,
                               disable_web=True)
    await UserState.petitions.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.petitions)
async def petitions(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.petitions(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen CC 23
@dp.callback_query_handler(state=UserState.petitions)
async def set_petitions(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"petitions": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_petitions(), kb=keyboards.next,
                               disable_web=True)
    await UserState.lazy.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.lazy)
async def lazy(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )

    await edit_or_send_message(bot, call, state=state, text=await texts.lazy(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen CC 25
@dp.callback_query_handler(state=UserState.lazy)
async def set_lazy(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"lazy": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 0,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_lazy(), kb=keyboards.next, disable_web=True)
    await UserState.characteristic.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.characteristic)
async def characteristic(call: CallbackQuery, state: FSMContext):
    await edit_or_send_message(bot, call, state=state, text=await texts.characteristic(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen CC 27
@dp.callback_query_handler(state=UserState.characteristic)
async def set_characteristic(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"characteristic": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 0,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_characteristic(), kb=keyboards.next,
                               disable_web=True)
    await UserState.stock.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.stock)
async def stock(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.characteristic(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen CC 29
@dp.callback_query_handler(state=UserState.stock)
async def set_stock(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"stock": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_stock(), kb=keyboards.act3,
                               disable_web=True)
    await UserState.act3.set()
    await call.answer()


# ------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------


@dp.callback_query_handler(Button("act2"), state=UserState.KO)
async def competitor(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.competitor(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen KO-17
@dp.callback_query_handler(state=UserState.KO)
async def set_competitor(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"competitor": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_competitor(), kb=keyboards.next,
                               disable_web=True)
    await UserState.pandemic.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.pandemic)
async def pandemic(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.pandemic(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen KO 19
@dp.callback_query_handler(state=UserState.pandemic)
async def set_pandemic(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"pandemic": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_pandemic(), kb=keyboards.next,
                               disable_web=True)
    await UserState.remote.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.remote)
async def remote(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.remote(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen KO 21
@dp.callback_query_handler(state=UserState.remote)
async def set_remote(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"remote": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_remote(), kb=keyboards.next,
                               disable_web=True)
    await UserState.reluctantly.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.reluctantly)
async def reluctantly(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.reluctantly(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen KO 23
@dp.callback_query_handler(state=UserState.reluctantly)
async def set_reluctantly(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"reluctantly": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 0,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_reluctantly(), kb=keyboards.next,
                               disable_web=True)
    await UserState.polls.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.polls)
async def polls(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.polls(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen KO 25
@dp.callback_query_handler(state=UserState.polls)
async def set_polls(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"polls": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_polls(), kb=keyboards.next,
                               disable_web=True)
    await UserState.traffic.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.traffic)
async def traffic(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.traffic(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen KO 27
@dp.callback_query_handler(state=UserState.traffic)
async def set_traffic(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"traffic": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_traffic(), kb=keyboards.next,
                               disable_web=True)
    await UserState.meaning.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.meaning)
async def meaning(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.meaning(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen KO 29
@dp.callback_query_handler(state=UserState.meaning)
async def set_meaning(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await state.update_data(
        {"meaning": call.data}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_meaning(), kb=keyboards.act3,
                               disable_web=True)
    await UserState.act3.set()
    await call.answer()


# ------------------------------------------------------------------------------
# print(f"{data['Loyalty_to_the_administration']},{data['Students_love']},{data['Respect_for_colleagues']}")
@dp.callback_query_handler(Button("act3"), state=UserState.act3)
async def meaning(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.management(), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen 32
@dp.callback_query_handler(state=UserState.act3)
async def set_management(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await state.update_data(
        {"management": call.data}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_management(), kb=keyboards.next,
                               disable_web=True)
    await UserState.femki.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.femki)
async def femki(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.femki(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen 34
@dp.callback_query_handler(state=UserState.femki)
async def set_femki(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"femki": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_femki(), kb=keyboards.next,
                               disable_web=True)
    await UserState.ignore.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.ignore)
async def ignore(call: CallbackQuery, state: FSMContext):
    await edit_or_send_message(bot, call, state=state, text=await texts.ignore(state), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen 36
@dp.callback_query_handler(state=UserState.ignore)
async def set_ignore(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"ignore": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_ignore(), kb=keyboards.next,
                               disable_web=True)
    await UserState.event.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.event)
async def event(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.event(state), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen 38
@dp.callback_query_handler(state=UserState.event)
async def set_event(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"event": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_event(), kb=keyboards.next,
                               disable_web=True)
    await UserState.putin.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.putin)
async def putin(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.putin(state), kb=keyboards.threeButton,
                               disable_web=True)
    await call.answer()


# Screen 40
@dp.callback_query_handler(state=UserState.putin)
async def set_putin(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"putin": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.set_putin(), kb=keyboards.next,
                               disable_web=True)
    if data['putin'] == "1":
        await UserState.putinFOREVOR.set()
    elif data['putin'] == "2":
        await UserState.end.set()
    else:
        await UserState.putinLOX.set()
    await call.answer()


# Screen 44
@dp.callback_query_handler(Button("next"), state=UserState.end)
async def end(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.end(), kb=keyboards.end, disable_web=True)
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.putinFOREVOR)
async def putinFOREVOR(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.putinFOREVOR(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen 42/1
@dp.callback_query_handler(state=UserState.putinFOREVOR)
async def set_putinFOREVOR(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"putinFOREVOR": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 1}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 2,
             "Students_love": data["Students_love"] + 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 1}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.end(), kb=keyboards.end, disable_web=True)
    await UserState.end.set()
    await call.answer()


@dp.callback_query_handler(Button("next"), state=UserState.putinLOX)
async def putinLOX(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.putinLOX(), kb=keyboards.fourButton,
                               disable_web=True)
    await call.answer()


# Screen 42/2
@dp.callback_query_handler(state=UserState.putinLOX)
async def set_putinLOX(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"putinLOX": call.data}
    )
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    data = await state.get_data()
    if call.data == "1":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] + 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "2":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 2,
             "Students_love": data["Students_love"] - 1,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 2}
        )
    elif call.data == "3":
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] - 1,
             "Students_love": data["Students_love"] - 2,
             "Respect_for_colleagues": data["Respect_for_colleagues"] - 2}
        )
    else:
        await state.update_data(
            {"Loyalty_to_the_administration": data["Loyalty_to_the_administration"] + 0,
             "Students_love": data["Students_love"] + 0,
             "Respect_for_colleagues": data["Respect_for_colleagues"] + 0}
        )
    await edit_or_send_message(bot, call, state=state, text=await texts.end(), kb=keyboards.end, disable_web=True)
    await UserState.end.set()
    await call.answer()


# Screen 45

@dp.callback_query_handler(Button("end"), state=UserState.end)
async def ALLEND(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await edit_or_send_message(bot, call, state=state, text=await texts.ALLEND(state), kb=keyboards.ALLEND,
                               disable_web=True)
    await call.answer()


@dp.callback_query_handler(Button("new"), state="*")
async def new(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await UserState.start.set()
    await start(call.message, state)
    await call.answer()


# Share BOT
@dp.callback_query_handler(Button("share"), state="*")
async def shareEND(call: types.CallbackQuery, state: FSMContext):
    msg = await edit_or_send_message(bot, call, state=state, text=await texts.share_bot(bot), kb=keyboards.back_metric,
                                     disable_web=False,
                                     delete=False)
    await state.update_data(
        {"messegeToDelete": msg.message_id}
    )
    await call.answer()


# @dp.callback_query_handler(Button("ser"), state="*")
# async def ser_set(call: CallbackQuery, state: FSMContext):
#     msg = await edit_or_send_message(bot, call, state=state,
#                                      text="Как Вас записать в сертификат?\n(Напишите Имя Фамилия)",
#                                      disable_web=True)
#     await state.update_data(
#         {"messegeToDelete": msg.message_id}
#     )
#     await UserState.sertificat.set()
#     await call.answer()


@dp.callback_query_handler(Button("ser"), state="*")
async def ser(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    png_name = f"out{call.message.chat.id}.png"
    new_pdf_name = f"dest{call.message.chat.id}.pdf"
    MtP.add_as_png([data['Students_love'],
                    data['Loyalty_to_the_administration'],
                    data['Respect_for_colleagues']],
                   png_name,
                   new_pdf_name)
    msg = await edit_or_send_message(bot, call, photo=InputFile(MtP.path + png_name), state=state,
                                     text="Хэй, а вот и твой сертификат🎉 Скорее поделись им в сториз со своими друзьями📲",
                                     kb=keyboards.back_metric,
                                     disable_web=True)
    await state.update_data(
        {"messegeToDelete": msg.message_id}
    )
    await call.answer()


@dp.callback_query_handler(Button("back_metric"), state="*")
async def back(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        {"messegeToDelete": call.message.message_id}
    )
    await UserState.end.set()
    await ALLEND(call, state)
    await call.answer()
