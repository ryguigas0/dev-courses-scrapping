from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import select, UniqueConstraint
from webscrapping.models import Base, create_session
from webscrapping.models.course_language import courses_languages
from webscrapping.models.course_instructor import courses_instructors


class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    source_url: Mapped[str]
    image_url: Mapped[str]
    rating: Mapped[float]
    complete_time_seconds: Mapped[int]
    topic: Mapped[str]
    qty_students: Mapped[int]
    qty_reviews: Mapped[int]
    updated_at: Mapped[datetime]
    scraped_at: Mapped[datetime] = mapped_column(default=datetime.now())
    price: Mapped[float] = mapped_column(default=0)
    languages: Mapped[List["Language"]] = relationship(
        secondary=courses_languages, back_populates="courses"
    )
    instructors: Mapped[List["Instructor"]] = relationship(
        secondary=courses_instructors, back_populates="courses"
    )
    __table_args__ = (UniqueConstraint("source_url", sqlite_on_conflict="REPLACE"),)


def insert_courses(courses):
    Session = create_session()
    with Session.begin() as session:
        session.add_all(courses)
        session.commit()


def insert_course(course):
    Session = create_session()
    with Session.begin() as session:
        session.add(course)
        session.commit()


def list_courses():
    Session = create_session()
    with Session.begin() as session:
        stmt = select(Course)
        return session.scalars(stmt).all()


def get_course(id):
    Session = create_session()
    with Session.begin() as session:
        stmt = select(Course).where(Course.id == id)
        return session.scalars(stmt).one()
