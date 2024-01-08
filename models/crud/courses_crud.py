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


def list_courses():
    Session = create_session()
    courses = None
    with Session.begin() as session:
        stmt = select(Course)
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
