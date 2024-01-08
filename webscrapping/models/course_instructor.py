from sqlalchemy import Table, Column, ForeignKey
from webscrapping.models import Base

courses_instructors = Table(
    "courses_instructors",
    Base.metadata,
    Column("course_id", ForeignKey("course.id"), primary_key=True),
    Column("instructor_id", ForeignKey("instructor.id"), primary_key=True),
)
