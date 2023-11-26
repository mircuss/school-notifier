import asyncio
from aiogram import Bot, Dispatcher
from handlers.basic import basic_router
from handlers.admin_menu import admin_router
from handlers.teacher_menu import teacher_router
from config import TOKEN

from services.scheduler_notify import start_sheduler

async def main():
    bot = Bot(token=TOKEN)
    await start_sheduler(bot=bot)
    dp = Dispatcher()
    dp.include_router(basic_router)
    dp.include_router(teacher_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
