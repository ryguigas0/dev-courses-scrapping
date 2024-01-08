from fastapi import APIRouter
from models.crud import courses_crud as crud
from typing import Union


api_router = APIRouter(prefix="/api/courses")


@api_router.get("/")
def index(
    topic: Union[str, None] = None,
    max_rating: Union[float, None] = None,
    max_complete_time_seconds: Union[int, None] = None,
    max_price: Union[float, None] = None,
    min_complete_time_seconds: int = 0,
    min_price: float = 0.0,
    min_rating: float = 0.0,
):
    return crud.list_courses(
        topic,
        min_rating,
        max_rating,
        min_complete_time_seconds,
        max_complete_time_seconds,
        min_price,
        max_price,
    )


@api_router.get("/{course_id}")
def get(course_id: int):
    return crud.get_course(course_id)
