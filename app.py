from aiogram import executor
from bot.load_all import bot



async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    # await bot.send_message(338141569, "Я запущен!")
    pass

if __name__ == '__main__':
    from bot.handlers import dp
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)