from aiogram import Bot, F, Router
from aiogram.types import Message,InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


from config import ADMIN_ID
from sql.repo import Repo 
from keyboards.inline import admin_menu, head_teacher_markup
from keyboards.reply import main_markup


basic_router = Router()

async def generate_schools_keyboard():
    schools = await Repo().get_all_school_names()
    keyboard = InlineKeyboardBuilder()

    for school in schools:
        keyboard.add(InlineKeyboardButton(text=f"{school[0]}", callback_data=f"school_{school[0]}"))
        
    return keyboard.as_markup()

async def generate_classes_keyboard(school_name, prefix: str = ""):
    classes = await Repo().get_classes_by_school(school_name=school_name)
    keyboard = InlineKeyboardBuilder()
    for class_info in classes:
        class_text = f"{class_info[0].number}-{class_info[0].letter}"
        callback_data = f"{prefix}class_{class_text}"
        keyboard.add(InlineKeyboardButton(text=class_text, callback_data=callback_data))

    return keyboard.as_markup()



@basic_router.message(F.text == "/start")
async def start(message: Message):
    teacher = await Repo().get_teacher(user_id=int(message.from_user.id))
    if int(ADMIN_ID) == message.from_user.id:
        return await message.answer(text="Вітаю в боті **АДМНІН**", reply_markup=admin_menu)
    elif teacher:
        return await message.answer(text="Вітаю в боті **ЗАВУЧ**", reply_markup=head_teacher_markup)
    elif not await Repo().get_pupil(user_id=message.from_user.id):
        keyboard = await generate_schools_keyboard()
        return await message.answer(text="Оберіть школу", reply_markup=keyboard)
    await message.answer("Вітаю! Чим я можу вам допомогти", reply_markup=main_markup)


@basic_router.callback_query(F.data.startswith("school_"))
async def get_class(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    keyboard = await generate_classes_keyboard(data[-1])
    await state.update_data({"school": data[-1]})
    await call.message.answer(text="Оберіть клас", reply_markup=keyboard)



@basic_router.callback_query(F.data.startswith("class"))
async def select_classroom(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    classroom = call.data.split("_")[-1].split("-")
    print(call.message.from_user.id)
    print(call.message.from_user.id)
    await Repo().add_pupil(user_id=call.from_user.id, class_num=classroom[0], class_letter=classroom[1], school_name=data["school"])
    await state.clear()
    await call.message.answer(text="Ви успішно зареєструвались", reply_markup=main_markup)
    


@basic_router.message(F.text == "Змінити клас")
async def change_classroom(message: Message):
    pupil = await Repo().get_pupil(user_id=message.from_user.id)
    keyboard = await generate_classes_keyboard(school_name=pupil.school_name, prefix="edit")
    await message.answer(text="Оберіть ноаий клас", reply_markup=keyboard)


@basic_router.callback_query(F.data.startswith("edit"))
async def edit_classroom(call: CallbackQuery):
    classroom = call.data.split("_")[-1].split("-")
    await Repo().update_pupil_class(pupil_id=call.from_user.id, new_class_letter=classroom[1], new_class_number=classroom[0])
    await call.message.answer(text="Ваш клас змінено")

