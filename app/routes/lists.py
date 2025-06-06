from fastapi import APIRouter
from app.models import TodoList

router = APIRouter(prefix="/lists", tags=["Lists"])

# Base de datos falsa para pruebas
fake_lists_db = [
    {"id": 1, "name": "Trabajo"},
    {"id": 2, "name": "Casa"}
]

@router.get("/", response_model=list[TodoList])
def get_lists():
    return fake_lists_db
