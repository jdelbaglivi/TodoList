from pydantic import BaseModel, Field
from typing import Optional

class TodoList(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)

class TodoListCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class TodoItemBase(BaseModel):
    description: str = Field(..., min_length=3, max_length=200)
    completed: bool = False

class TodoItemCreate(TodoItemBase):
    pass

class TodoItemUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=3, max_length=200)
    completed: Optional[bool] = None

class TodoItem(TodoItemBase):
    id: int
    list_id: int