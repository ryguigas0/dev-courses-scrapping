from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from . import Base
from .course_language import courses_languages

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

    def to_view(self, level=1):
        language = {"id": self.id, "name": self.name}

        if level > 0:
            language["courses"] = list(
                map(lambda c: c.to_view(level - 1), self.courses)
            )

        return language
