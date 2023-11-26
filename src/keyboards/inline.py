from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sql.repo import Repo

async def generate_classes_keyboard(school_name, prefix=""):
    classes = await Repo().get_classes_by_school(school_name=school_name)
    keyboard = InlineKeyboardBuilder()
    for class_info in classes:
        class_text = f"{class_info[0].number}-{class_info[0].letter}"
        callback_data = f"{prefix}_class_{class_text}"
        keyboard.add(InlineKeyboardButton(text=class_text, callback_data=callback_data))

    return keyboard.as_markup()

admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Додати клас", callback_data="add_classroom")
    ],
    [
        InlineKeyboardButton(text="Додати завуча", callback_data="add_head_teacher")
    ],
    [
        InlineKeyboardButton(text="Додати розклад", callback_data="add_scheduler")
    ]
])


days_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Понеділок", callback_data="day_0"),
        InlineKeyboardButton(text="Вівторок", callback_data="day_1")
    ],
    [
        InlineKeyboardButton(text="Середа", callback_data="day_2"),
        InlineKeyboardButton(text="Четвер", callback_data="day_3"),
        InlineKeyboardButton(text="П'ятниця", callback_data="day_4")
    ]
])

head_teacher_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Зміни в розкладі", callback_data="make_edit")
    ]
])