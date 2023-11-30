from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from sql.repo import Repo
from states.teacher_states import TeacherStates
from keyboards.inline import generate_classes_keyboard, days_markup

teacher_router = Router()

async def generate_lesson_scheduler(day: int, classroom: str, school:str):
    lessons = await Repo().get_lessons_by_conditions(day=day, school=school, classroom=classroom)
    
    formatted_lessons = ""

    for lesson in lessons:
        room = lesson.edit_room or lesson.room
        name = lesson.edit_lesson or lesson.name

        if "Немає" in name:
            formatted_lessons += f"{lesson.num+1}. {name}"
        else:
            formatted_lessons += f"{lesson.num+1}. {name} {room}\n"

    return formatted_lessons


@teacher_router.callback_query(F.data == "make_edit")
async def get_class_to_edit(call: CallbackQuery, state: FSMContext):
    keyboard = await generate_classes_keyboard("Школа №4", prefix="_edit")
    await state.set_state(TeacherStates.day)
    await call.message.edit_text(text="Оберіть клас", reply_markup=keyboard)
    await call.answer()

@teacher_router.callback_query(F.data.startswith("_edit"))
async def get_day(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    await state.update_data({"classroom": data[-1]})
    await state.set_state(TeacherStates.day)
    await call.message.edit_text("Оберіть день", reply_markup=days_markup)
    await call.answer()


@teacher_router.callback_query(StateFilter(TeacherStates.day), F.data.startswith("day"))
async def get_edit(call: CallbackQuery, state: FSMContext):
    day = call.data.split("_")[-1]
    await state.set_state(TeacherStates.announce)
    await state.update_data({"day": day})
    await call.message.edit_text(text="Напишить уроки в форматі:\n Номер Урок Аудиторія")
    await call.answer()


@teacher_router.message(StateFilter(TeacherStates.announce))
async def add_announce(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    classroom = data["classroom"]
    day = data["day"]
    lessons = message.text.split("\n")
    
    for lesson in lessons:
        info = lesson.split(" ")
        number = int(info[0])-1
        if len(info) == 1:
            await Repo().update_lesson(edit_room=None, edit_lesson=None, classroom=classroom, day=day, num=number)
            await Repo().update_lesson_next(new_next=None, classroom=classroom, day=day, num=number-1)
            continue
        if len(info[-1]) <= 5:
            room = info[-1]
        else:
            room = ""
        if "немає" in lesson.lower():
            await Repo().update_lesson(edit_room="", edit_lesson="Немає", classroom=classroom, day=day, num=number)
            await Repo().update_lesson_next(new_next="Наступного урок немає", classroom=classroom, day=day, num=number-1)
        else:
            await Repo().update_lesson(edit_room=room, edit_lesson=" ".join(info[1:-1]), classroom=classroom, day=day, num=number)
            await Repo().update_lesson_next(new_next=lesson, classroom=classroom, day=day, num=number-1)
    class_num, class_letter = classroom.split("-")
    pupils = await Repo().get_pupils_by_classroom(class_letter=class_letter, class_num=int(class_num))
    days = {"0": "Понеділок",
            "1": "Вівторок",
            "2": "Середа",
            "3": "Четвер",
            "4": "П'ятниця"}
    scheduler = await generate_lesson_scheduler(day=day, classroom=classroom, school="Школа №4")
    
    for pupil in pupils:
        print(pupil[0].id)
        try:
            await bot.send_message(chat_id=pupil[0].id, text=f"{days.get(day)}\n{scheduler}")
        except TelegramBadRequest:
            pass