import asyncio
import aiogram
from aiogram import Bot, Dispatcher, executor
from config import API_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)

if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp)