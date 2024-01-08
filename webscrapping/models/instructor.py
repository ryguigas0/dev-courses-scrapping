from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from webscrapping.models import Base
from webscrapping.models.course_instructor import courses_instructors

# if TYPE_CHECKING:
#     from .course import Course


class Instructor(Base):
    __tablename__ = "instructor"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    courses: Mapped[List["Course"]] = relationship(
        secondary=courses_instructors, back_populates="instructors"
    )
    __table_args__ = (UniqueConstraint("name", sqlite_on_conflict="IGNORE"),)
