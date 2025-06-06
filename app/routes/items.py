from fastapi import APIRouter, HTTPException, status
from app.models import TodoItem, TodoItemCreate, TodoItemUpdate
from app.routes.lists import fake_lists_db

router = APIRouter(prefix="/lists/{list_id}/items",
                    tags=["Items"],
                    responses={404: {"description": "Not found"}})

# Base de datos falsa para pruebas
fake_items_db = [
    {"id": 1,"list_id": 1, "description": "Portátil de 15 pulgadas", "completed": False},
    {"id": 2,"list_id": 1,  "description": "Smartphone Android", "completed": True},
    {"id": 3,"list_id": 2, "description": "Lavar los platos de la cena", "completed": False},
    {"id": 4,"list_id": 2, "description": "Comprar frutas y verduras", "completed": True}
]

def get_next_id():
    return max(item["id"] for item in fake_items_db) + 1 if fake_items_db else 1

@router.get("/", response_model=list[TodoItem], summary="Obtener todos los ítems de una lista")
def get_items(list_id: int):
    """Obtiene todos los ítems de una lista específica"""
    # Verificar que la lista exista
    if not any(lst["id"] == list_id for lst in fake_lists_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lista con ID {list_id} no encontrada"
        )
    return [item for item in fake_items_db if item["list_id"] == list_id]

@router.post(
    "/",
    response_model=TodoItem,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo ítem en la lista"
)
def create_item(list_id: int, item: TodoItemCreate):
    """Crea un nuevo ítem en una lista específica"""
    # Validar que la lista exista
    if not any(lst["id"] == list_id for lst in fake_lists_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lista con ID {list_id} no encontrada"
        )
    
    # Validar que no exista un ítem con la misma descripción en la lista
    description = item.description.strip()
    if any(i["list_id"] == list_id and i["description"].lower() == description.lower() for i in fake_items_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un ítem con esta descripción en la lista"
        )

    new_item = {
        "id": get_next_id(),
        "list_id": list_id,
        "description": description,
        "completed": False
    }
    fake_items_db.append(new_item)
    return new_item
