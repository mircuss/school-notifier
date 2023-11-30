from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from sql.repo import Repo



async def send_lesson(user: int, bot: Bot, text: str):
    try:
        await bot.send_message(chat_id=user, text=text)
    except TelegramBadRequest:
        pass

async def main_scheduler(number, bot: Bot):
    
    lessons = {}
    repo = Repo()
    current_date = datetime.now().weekday()
    if current_date == 5 or current_date == 6:
        return
    pupils = await repo.get_pupils()
    print(pupils)
    for pupil in pupils:
        pupil = pupil[0]
        classroom = f"{pupil.class_num}-{pupil.class_letter}"

        if classroom not in lessons:
            class_lessons = await repo.get_lessons_by_number(num=number, class_name=classroom, day=current_date)

            if not class_lessons:
                continue
            
            lesson = class_lessons[0]

            lesson_name = lesson.edit_lesson if lesson.edit_lesson is not None else lesson.name
            lesson_room = lesson.edit_room if lesson.edit_room is not None else lesson.room

            lessons[classroom] = [lesson_name, lesson_room]
            await repo.update_lesson(edit_lesson=None, edit_room=None, classroom=classroom, day=current_date, num=lesson.num)
        text = f"Зараз почнеться урок **{lessons[classroom][0]} {lessons[classroom][1]}**"
        
        await send_lesson(user=pupil.id, bot=bot, text=text)
        

async def start_sheduler(bot: Bot):
    journal = [{"start": "7:55", "end": "8:45"},
               {"start": "8:45", "end": "9:40"},
               {"start": "9:40", "end": "10:45"},
               {"start": "10:45", "end": "11:50"},
               {"start": "11:50", "end": "12:45"},
               {"start": "12:45", "end": "13:40"},
               {"start": "13:42", "end": "14:35"},
               {"start": "14:35", "end": "15:30"},
               {"start": "15:30", "end": "16:25"}]
    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    for index, lesson in enumerate(journal):
        start_hour, start_minute = lesson.get("start").split(":")
        scheduler.add_job(main_scheduler, "cron", hour=start_hour, minute=start_minute, kwargs={"bot": bot, "number": index})
    scheduler.start()
