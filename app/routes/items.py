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
    """Obtiene todos los ítems de una lista específica por su ID."""
    # Verificar que la lista exista
    if not any(lst["id"] == list_id for lst in fake_lists_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lista con ID {list_id} no encontrada"
        )
    return [item for item in fake_items_db if item["list_id"] == list_id]

@router.post("/", response_model=TodoItem, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo ítem en la lista")
def create_item(list_id: int, item: TodoItemCreate):
    """Crea un nuevo ítem con su descripcion y el bool completed en una lista específica por su ID."""
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
        "completed": item.completed  # Usar el valor del modelo
    }
    fake_items_db.append(new_item)
    return new_item

@router.put("/{item_id}", response_model=TodoItem, summary="Actualizar un ítem de la lista")
def update_item(list_id: int, item_id: int, item_update: TodoItemUpdate):
    """Actualiza un ítem existente en una lista específica por su ID."""
    # Verificar que la lista exista
    if not any(lst["id"] == list_id for lst in fake_lists_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lista con ID {list_id} no encontrada"
        )
    # Buscar el ítem y su índice de una vez
    item_index = None
    item = None
    for i, current_item in enumerate(fake_items_db):
        if current_item["id"] == item_id and current_item["list_id"] == list_id:
            item_index = i
            item = current_item
            break
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ítem con ID {item_id} no encontrado en la lista {list_id}"
        )
    # Validar que al menos uno de los campos a actualizar esté presente
    update_data = item_update.model_dump(exclude_unset=True)  # Cambiado de dict() a model_dump()
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar"
        )
    
    # Validar descripción duplicada si se está actualizando
    if "description" in update_data:
        new_description = update_data["description"].strip()
        # Verificar que no exista otro ítem con la misma descripción en la lista excluyendo el actual
        if any(i["list_id"] == list_id and i["description"].lower() == new_description.lower() for i in fake_items_db if i["id"] != item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un ítem con esta descripción en la lista"
            )
        update_data["description"] = new_description

    # Actualizar el ítem
    fake_items_db[item_index].update(update_data)
    return fake_items_db[item_index] 

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un ítem de la lista")
def delete_item(list_id: int, item_id: int):
    """Elimina un ítem existente en una lista específica por su ID."""
    # Verificar que la lista exista
    if not any(lst["id"] == list_id for lst in fake_lists_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lista con ID {list_id} no encontrada"
        )
    # Buscar el ítem y su índice de una vez
    item_index = None
    for i, item in enumerate(fake_items_db):
        if item["id"] == item_id and item["list_id"] == list_id:
            item_index = i
            break
    if item_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ítem con ID {item_id} no encontrado en la lista {list_id}"
        )
    # Eliminar el ítem
    del fake_items_db[item_index]

@router.patch("/{item_id}/complete", response_model=TodoItem, summary="Marcar un ítem como completado")
def complete_item(list_id: int, item_id: int):
    """Marca un ítem existente como completado en una lista específica por su ID."""
    # Verificar que la lista exista
    if not any(lst["id"] == list_id for lst in fake_lists_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lista con ID {list_id} no encontrada"
        )
    # Buscar el ítem y su índice de una vez
    item_index = None
    for i, item in enumerate(fake_items_db):
        if item["id"] == item_id and item["list_id"] == list_id:
            item_index = i
            break
    if item_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ítem con ID {item_id} no encontrado en la lista {list_id}"
        )
    # Marcar el ítem como completado
    fake_items_db[item_index]["completed"] = True
    return fake_items_db[item_index]