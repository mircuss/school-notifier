from aiogram.fsm.state import State, StatesGroup

class TeacherStates(StatesGroup):
    day = State()
    lessons = State()
    announce = State()