from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///./database.db", echo=True)


def create_session():
    return sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def create_database():
    # imports for populating Base metadata
    from .course import Course
    from .instructor import Instructor
    from .language import Language
    from .course_instructor import courses_instructors
    from .course_language import courses_languages
    Base.metadata.create_all(bind=engine)
