from mcp.server.fastmcp import FastMCP

import requests

# Crear servidor MCP
mcp = FastMCP("TodoList")

API_BASE_URL = "http://localhost:8000"


# Función auxiliar para hacer requests seguras
def safe_request(method: str, url: str, data: dict = None):
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "PATCH":
            response = requests.patch(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError(f"Método no soportado: {method}")

        if response.status_code in [200, 201, 204]:
            if response.status_code == 204:
                return {"message": "Operación exitosa", "status": "success"}
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        return {"error": str(e)}


# Tools registrados

@mcp.tool()
def get_lists() -> list:
    """Devuelve todas las listas disponibles"""
    return safe_request("GET", f"{API_BASE_URL}/lists")
@mcp.tool()
def create_list(name: str) -> dict:
    """Crea una nueva lista de tareas"""
    return safe_request("POST", f"{API_BASE_URL}/lists", {"name": name})

@mcp.tool()
def get_items(list_id: int) -> list:
    """Devuelve todos los ítems de una lista específica"""
    return safe_request("GET", f"{API_BASE_URL}/lists/{list_id}/items")


@mcp.tool()
def create_item(list_id: int, description: str) -> dict:
    """Crea un ítem nuevo en una lista"""
    return safe_request("POST", f"{API_BASE_URL}/lists/{list_id}/items", {"description": description})


@mcp.tool()
def update_item(list_id: int, item_id: int, description: str = None, completed: bool = None) -> dict:
    """Actualiza un ítem existente (descripción y/o completado)"""
    data = {}
    if description is not None:
        data["description"] = description
    if completed is not None:
        data["completed"] = completed
    return safe_request("PUT", f"{API_BASE_URL}/lists/{list_id}/items/{item_id}", data)


@mcp.tool()
def complete_item(list_id: int, item_id: int) -> dict:
    """Marca un ítem como completado"""
    return safe_request("PATCH", f"{API_BASE_URL}/lists/{list_id}/items/{item_id}/complete")


@mcp.tool()
def delete_item(list_id: int, item_id: int) -> dict:
    """Elimina un ítem de una lista"""
    return safe_request("DELETE", f"{API_BASE_URL}/lists/{list_id}/items/{item_id}")


# Ejecutar el servidor (solo si se llama directamente)
if __name__ == "__main__":
    mcp.run()
