from sqlalchemy import Boolean, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import Mapped, MappedCollection, mapped_column, DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Lesson(Base):

    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    day: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    next: Mapped[str] = mapped_column(String(250), nullable=False)
    num: Mapped[int] = mapped_column(Integer, nullable=False)
    school_name: Mapped[str] = mapped_column(String(250))
    room: Mapped[str] = mapped_column(String(250), nullable=True)
    classroom: Mapped[str] = mapped_column(String(250))
    edit_lesson: Mapped[str] = mapped_column(String(250), nullable=True)
    edit_room: Mapped[str] = mapped_column(String(250), nullable=True)

class Journal(Base):

    __tablename__ = "journal"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    num: Mapped[int] = mapped_column(Integer, nullable=False)
    start: Mapped[str] = mapped_column(String(250), nullable=False)
    end: Mapped[str] = mapped_column(String(250), nullable=False)
    
class ClassRoom(Base):

    __tablename__ = "classroom"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    school_name: Mapped[str] = mapped_column(String(250))
    number: Mapped[int] = mapped_column(Integer)
    letter: Mapped[str] = mapped_column(String(250))

class Teacher(Base):

    __tablename__ = "teacher"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    class_num: Mapped[int] = mapped_column(Integer, default=None, nullable=True)
    class_letter: Mapped[str] = mapped_column(String(250), default=None, nullable=True)
    head_teacher: Mapped[bool] = mapped_column(Boolean)
    director: Mapped[bool] = mapped_column(Boolean)

class Pupil(Base):

    __tablename__ = "pupil"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    class_num: Mapped[int] = mapped_column(Integer)
    class_letter: Mapped[str] = mapped_column(String(250))
    school_name: Mapped[bool] = mapped_column(Boolean, default=False)
