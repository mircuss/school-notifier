from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sql.repo import Repo
from states.admin_states import AdminStates
from keyboards.inline import days_markup, generate_classes_keyboard

admin_router = Router()


@admin_router.callback_query(F.data == "add_classroom")
async def get_classroom(call: CallbackQuery, state: FSMContext):
    await state.update_data({"school": "Школа №4"})
    await state.set_state(AdminStates.classroom_name)
    await call.message.edit_text(text="Введіть назву класу")
    await call.answer()

@admin_router.message(StateFilter(AdminStates.classroom_name))
async def add_classroom(message: Message, state: FSMContext):
    data = await state.get_data()
    for classroom in message.text.split(" "):
        text = classroom.split("-")
        if not await Repo().is_classroom_exists(school_name=data["school"], letter=text[1], number=int(text[0])):
            await Repo().add_classroom(school_name=data["school"], class_letter=text[1], class_num=int(text[0]))
            await message.answer(text=f"Класс {classroom} додано до школи {data['school']}")
            await state.clear()
        else:
            await message.answer(text=f"Класс {classroom} вже існує в школі {data['school']}")

@admin_router.callback_query(F.data == "add_scheduler")
async def get_day(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    keyboard = await generate_classes_keyboard("Школа №4")
    await state.update_data({"school": "Школа №4"})
    await call.message.edit_text(text="Оберіть клас", reply_markup=keyboard)
    await call.answer()


@admin_router.callback_query(F.data.startswith("_class"))
async def select_classroom(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    await state.update_data({"class": data[-1]})
    await call.message.edit_text(text="Оберіть день", reply_markup=days_markup)
    await call.answer()



@admin_router.callback_query(F.data.startswith("day"))
async def get_lessons(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    await state.set_state(AdminStates.lessons)
    await state.update_data({"day": data[-1]})
    await call.message.edit_text(text="Введіть уроки в совбчик")
    await call.answer()

@admin_router.message(StateFilter(AdminStates.lessons))
async def add_lessons(message: Message, state: FSMContext):
    data = await state.get_data()
    lessons = message.text.split("\n")
    for index, lesson in enumerate(lessons):
        info = lesson.split()
        if len(info[-1]) <= 5:
            room = info[-1]
        else:
            room = ""
        try:
            next_lesson = lessons[index+1]
        except IndexError:
            next_lesson = "Наступного уроку немає"
        lesson_s = await Repo().get_lessons_by_number(num=index, class_name=data["class"], day=data["day"])
        if lesson_s is None:
            await Repo().add_lesson(name=" ".join(info[1:-1]), next_lesson=next_lesson, num=index, school_name=data["school"], day=int(data["day"]), classroom=data["class"], room=room)
        else:
            await Repo().delete_lesson(lesson_id=lesson_s[0].id)
            await Repo().add_lesson(name=" ".join(info[1:-1]), next_lesson=next_lesson, num=index, school_name=data["school"], day=int(data["day"]), classroom=data["class"], room=room)
        await message.answer(f"Урок {lesson} додано")


@admin_router.callback_query(F.data == "add_head_teacher")
async def get_teacher_id(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.head_teacher)
    await call.message.edit_text(text="Введіть айді вчителя")
    await call.answer()


@admin_router.message(StateFilter(AdminStates.head_teacher))
async def add_head_teached(message: Message, state: FSMContext):
    await Repo().add_teacher(user_id=int(message.text), head_teacher=True)
    await message.answer(text="Завуча додано")

