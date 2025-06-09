from fastapi import FastAPI
from app.routes import lists, items


app = FastAPI(title="TodoList API")

app.include_router(lists.router)
app.include_router(items.router)


