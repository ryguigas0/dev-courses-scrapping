from sqlalchemy import Table, Column, ForeignKey
from . import Base

courses_languages = Table(
    "courses_languages",
    Base.metadata,
    Column("course_id", ForeignKey("course.id"), primary_key=True),
    Column("language_id", ForeignKey("language.id"), primary_key=True),
)
