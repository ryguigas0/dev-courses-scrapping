from fastapi import APIRouter
from models.crud import instructor_crud as crud


api_router = APIRouter(prefix="/api/instructors")


@api_router.get("/")
def index():
    return crud.list_instructors()


@api_router.get("/{instructor_id}")
def get(instructor_id: int):
    return crud.get_instrcutor(instructor_id)
