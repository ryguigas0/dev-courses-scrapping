from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from webscrapping.models import Base
from webscrapping.models.course_language import courses_languages

# if TYPE_CHECKING:
#     from .course import Course


class Language(Base):
    __tablename__ = "language"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    courses: Mapped[List["Course"]] = relationship(
        secondary=courses_languages, back_populates="languages"
    )
    __table_args__ = (UniqueConstraint("name", sqlite_on_conflict="IGNORE"),)
