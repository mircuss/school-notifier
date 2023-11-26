from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    school_name = State()
    classroom_name = State()
    lessons = State()
    set_school = State()
    head_teacher = State()