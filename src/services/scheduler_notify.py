from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sql.models import Pupil, Lesson
from sql.repo import Repo



async def send_lesson(user: int, bot: Bot, text: str):
    await bot.send_message(chat_id=user, text=text)


async def main_scheduler(number, bot: Bot):
    
    lessons = {}
    repo = Repo()
    current_date = datetime.now().weekday()
    current_date = 0
    pupils = await repo.get_pupils()
    
    for pupil in pupils[0]:
        classroom = f"{pupil.class_num}-{pupil.class_letter}"

        if classroom not in lessons:
            class_lessons = await repo.get_lessons_by_number(num=number, class_name=classroom, day=current_date)

            if not class_lessons:
                continue

            lesson = class_lessons[0]

            lesson_name = lesson.edit_lesson if lesson.edit_lesson is not None else lesson.name
            lesson_room = lesson.edit_room if lesson.edit_room is not None else lesson.room

            lessons[classroom] = [lesson_name, lesson_room]
        if lesson.edit_room is not None or lesson.edit_lesson is not None:
            await repo.update_lesson(edit_lesson=None, edit_room=None, classroom=classroom, day=current_date, num=lesson.num)
        text = f"Зараз почнеться урок **{lessons[classroom][0]} {lessons[classroom[1]]}**"
        
        await send_lesson(user=pupil.id, bot=bot, text=text)
        

async def start_sheduler(bot: Bot):
    journal = [{"start": "8:00", "end": "8:45"},
               {"start": "19:47", "end": "9:40"},
               {"start": "10:00", "end": "10:45"},
               {"start": "11:05", "end": "11:50"},
               {"start": "12:00", "end": "12:45"},
               {"start": "12:55", "end": "13:40"},
               {"start": "13:50", "end": "14:35"},
               {"start": "14:45", "end": "15:30"},
               {"start": "15:40", "end": "16:25"}]
    scheduler = AsyncIOScheduler()
    for index, lesson in enumerate(journal):
        start_hour, start_minute = lesson.get("start").split(":")
        scheduler.add_job(main_scheduler, "cron", day_of_week=5, hour=start_hour, minute=start_minute, kwargs={"bot": bot, "number": index})
    scheduler.start()
