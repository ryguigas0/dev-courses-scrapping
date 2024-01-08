from fastapi import APIRouter
from models.crud import courses_crud as crud


api_router = APIRouter(prefix="/api/courses")


@api_router.get("/")
def index():
    return crud.list_courses()


@api_router.get("/{course_id}")
def get(course_id: int):
    return crud.get_course(course_id)
