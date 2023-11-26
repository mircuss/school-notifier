from sqlalchemy import select, delete, update, insert, distinct, func, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sql.db import get_session

from typing import List

from sql.models import Pupil, Lesson, Journal, Teacher, ClassRoom

session: AsyncSession = get_session()

class Repo:
    def __init__(self):
        self.session = session

    async def add_teacher(self, user_id: int, class_num: int|None = None, class_letter: str|None = None, head_teacher: bool=False, director: bool=False) -> Teacher:
        teacher = Teacher(id=user_id, class_num=class_num, class_letter=class_letter, head_teacher=head_teacher, director=director)
        self.session.add(teacher)
        await session.commit()
        return teacher

    async def add_classroom(self, school_name, class_letter: str, class_num: int) -> ClassRoom:
        classroom = ClassRoom(school_name=school_name, letter=class_letter, number=class_num)
        self.session.add(classroom)
        await self.session.commit()
        return classroom


    async def add_pupil(self, user_id: int, class_num: int, class_letter: str, school_name: str) -> Pupil:
        pupil = Pupil(id=user_id, class_num=class_num, class_letter=class_letter, school_name=school_name)
        self.session.add(pupil)
        await self.session.commit()
        return pupil

    async def add_lesson(self, day: int, name: str, next_lesson: str, num: int, school_name: str, classroom: str, room: str) -> Lesson:
        lesson = Lesson(day=day, name=name, next=next_lesson, num=num, school_name=school_name, classroom=classroom, room=room)
        self.session.add(lesson)
        await self.session.commit()
        return lesson

    async def add_journal_entry(self, num: int, start: str, end: str):
        journal_entry = Journal(num=num, start=start, end=end)
        self.session.add(journal_entry)
        await self.session.commit()
        return journal_entry

    async def update_pupil_class(self, pupil_id: int, new_class_number: int, new_class_letter: str):
        update_stmt = (
            update(Pupil)
            .where(Pupil.id == pupil_id)
            .values(class_num=new_class_number, class_letter=new_class_letter)
        )

        await self.session.execute(update_stmt)
        await self.session.commit()


    async def update_lesson(self, edit_lesson: str | None, edit_room: str | None, classroom: str, day: int, num: int):
        update_stmt = (
            update(Lesson)
            .where(and_(Lesson.classroom == classroom, Lesson.day == day, Lesson.num == num))
            .values(edit_lesson=edit_lesson, edit_room=edit_room)
        )
        await self.session.execute(update_stmt)
        await self.session.commit()


    async def delete_teacher(self, user_id: int):
        teacher = (await self.session.execute(select(Teacher).filter(Teacher.id == user_id))).scalar()
        if teacher:
            await self.session.delete(teacher)
            await self.session.commit()
        else:
            raise ValueError("Teacher not found.")

    async def delete_pupil(self, user_id: int):
        pupil = (await self.session.execute(select(Pupil).filter(Pupil.id == user_id))).scalar()
        if pupil:
            await self.session.delete(pupil)
            await self.session.commit()
        else:
            raise ValueError("Pupil not found.")

    async def delete_lesson(self, lesson_id: int):
        lesson = (await self.session.execute(select(Lesson).filter(Lesson.id == lesson_id))).scalar()
        if lesson:
            await self.session.delete(lesson)
            await self.session.commit()
        else:
            raise ValueError("Lesson not found.")

    async def delete_journal_entry(self, journal_entry_id: int):
        journal_entry = (await self.session.execute(select(Journal).filter(Journal.id == journal_entry_id))).scalar()
        if journal_entry:
            await self.session.delete(journal_entry)
            await self.session.commit()
        else:
            raise ValueError("Journal entry not found.")


    async def is_classroom_exists(self, school_name: str, number: int, letter: str):
        query = select(ClassRoom).filter(
            (ClassRoom.school_name == school_name) &
            (ClassRoom.number == number) &
            (ClassRoom.letter == letter)
        )
        result = await self.session.execute(query)
        return result.scalar() is not None



    async def get_teacher(self, user_id: int):
        return (await self.session.execute(select(Teacher).filter(Teacher.id == user_id))).scalar_one_or_none()

    async def get_pupil(self, user_id: int):
        return (await self.session.execute(select(Pupil).filter(Pupil.id == user_id))).scalar_one_or_none()
    
    async def get_lessons_by_number(self, num: int, class_name: str, day: int) -> Lesson | None:
        return (await self.session.execute(select(Lesson).filter(and_(Lesson.num == num, Lesson.classroom == class_name, Lesson.day == day)))).one_or_none()

    async def get_pupils(self) -> List[Pupil]:
        return (await self.session.execute(select(Pupil))).all()

    async def get_all_school_names(self):
        query = select(distinct(ClassRoom.school_name))
        return (await self.session.execute(query)).all()

    async def get_pupils_by_classroom(self, class_letter: str, class_num: int) -> List[Pupil]:
        query = select(Pupil).where(and_(Pupil.class_letter == class_letter, Pupil.class_num==class_num))
        return (await self.session.execute(query)).all()

    async def get_classes_by_school(self, school_name: str):
        query = select(ClassRoom).filter(ClassRoom.school_name == school_name)
        result = await self.session.execute(query)
        return result.all()

