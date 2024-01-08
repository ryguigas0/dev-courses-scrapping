from sqlalchemy import select
from .. import create_session
from ..course import Course


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


def list_courses(
    topic,
    min_rating,
    max_rating,
    min_complete_time_seconds,
    max_complete_time_seconds,
    min_price,
    max_price,
):
    Session = create_session()
    courses = None
    with Session.begin() as session:
        stmt = (
            select(Course)
            .where(Course.rating >= min_rating)
            .where(Course.complete_time_seconds >= min_complete_time_seconds)
            .where(Course.price >= min_price)
        )

        if not topic is None:
            stmt = stmt.where(Course.topic.ilike(f"%{topic}%"))

        if not max_rating is None:
            stmt = stmt.where(Course.rating <= max_rating)

        if not max_complete_time_seconds is None:
            stmt = stmt.where(Course.complete_time_seconds <= max_complete_time_seconds)

        if not max_price is None:
            stmt = stmt.where(Course.price <= max_price)

        scalars = session.scalars(stmt).all()
        courses = list(map(lambda c: c.to_view(), scalars))
    return courses


def get_course(id):
    Session = create_session()
    course = None
    with Session.begin() as session:
        stmt = select(Course).where(Course.id == id)

        course = session.scalars(stmt).one().to_view()
        return course
