from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import select, UniqueConstraint
from . import Base, create_session
from .course_language import courses_languages
from .course_instructor import courses_instructors


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

    def to_view(self, level=1):
        course = {
            "id": self.id,
            "name": self.name,
            "source_url": self.source_url,
            "image_url": self.image_url,
            "rating": self.rating,
            "complete_time_seconds": self.complete_time_seconds,
            "topic": self.topic,
            "qty_students": self.qty_students,
            "qty_reviews": self.qty_reviews,
            "updated_at": self.updated_at,
            "scraped_at": self.scraped_at,
            "price": self.price,
        }

        if level > 0:
            course["languages"] = list(
                map(lambda l: l.to_view(level - 1), self.languages)
            )

            course["instructors"] = list(
                map(lambda i: i.to_view(level - 1), self.instructors)
            )

        return course
