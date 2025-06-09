from fastapi import APIRouter
from app.models import TodoList, TodoListCreate

router = APIRouter(prefix="/lists", tags=["Lists"])

# Base de datos falsa para pruebas
fake_lists_db = [
    {"id": 1, "name": "Trabajo"},
    {"id": 2, "name": "Casa"}
]

def get_next_id():
    return max(item["id"] for item in fake_lists_db) + 1 if fake_lists_db else 1

@router.get("/", response_model=list[TodoList])
def get_lists():
    return fake_lists_db

@router.post("/", response_model=TodoList, status_code=201)
def create_list(list: TodoListCreate):
    """Crea una nueva lista de tareas."""
    new_list =  {
        "id": get_next_id(),
        "name": list.name.strip()
    }
    if any(l["name"].lower() == new_list["name"].lower() for l in fake_lists_db):
        raise ValueError("Ya existe una lista con este nombre")
    fake_lists_db.append(new_list)
    return new_list
