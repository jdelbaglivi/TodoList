import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestLists:
    def test_get_lists(self):
        """Test obtener todas las listas"""
        response = client.get("/lists/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # Tenemos 2 listas por defecto
        assert data[0]["name"] == "Trabajo"
        assert data[1]["name"] == "Casa"

    def test_create_list_valid(self):
        """Test crear una lista válida"""
        list_data = {
            "name": "Nueva Lista"
        }
        response = client.post("/lists/", json=list_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Nueva Lista"
        assert "id" in data

class TestItems:
    def test_get_items_valid_list(self):
        """Test obtener ítems de una lista válida"""
        response = client.get("/lists/1/items/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_items_invalid_list(self):
        """Test obtener ítems de una lista inexistente"""
        response = client.get("/lists/999/items/")
        assert response.status_code == 404
        assert "Lista con ID 999 no encontrada" in response.json()["detail"]
    
    def test_create_item_valid(self):
        """Test crear un ítem válido"""
        item_data = {
            "description": "Test item",
            "completed": False
        }
        response = client.post("/lists/1/items/", json=item_data)
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Test item"
        assert data["completed"] == False
        assert data["list_id"] == 1
        assert "id" in data
    
    def test_create_item_invalid_list(self):
        """Test crear ítem en lista inexistente"""
        item_data = {
            "description": "Test item",
            "completed": False
        }
        response = client.post("/lists/999/items/", json=item_data)
        assert response.status_code == 404
    
    def test_create_item_duplicate_description(self):
        """Test crear ítem con descripción duplicada"""
        item_data = {
            "description": "Duplicate item",
            "completed": False
        }
        # Crear el primer ítem
        response1 = client.post("/lists/1/items/", json=item_data)
        assert response1.status_code == 201
        
        # Intentar crear el segundo con la misma descripción
        response2 = client.post("/lists/1/items/", json=item_data)
        assert response2.status_code == 400
        assert "Ya existe un ítem con esta descripción" in response2.json()["detail"]
    
    def test_create_item_invalid_description(self):
        """Test crear ítem con descripción inválida"""
        # Descripción muy corta
        item_data = {
            "description": "Hi",  # Menos de 3 caracteres
            "completed": False
        }
        response = client.post("/lists/1/items/", json=item_data)
        assert response.status_code == 422  # Validation error
    
    def test_update_item_valid(self):
        """Test actualizar un ítem válido"""
        # Primero crear un ítem
        create_data = {
            "description": "Item to update",
            "completed": False
        }
        create_response = client.post("/lists/1/items/", json=create_data)
        item_id = create_response.json()["id"]
        
        # Actualizar el ítem
        update_data = {
            "description": "Updated item",
            "completed": True
        }
        response = client.put(f"/lists/1/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated item"
        assert data["completed"] == True
    
    def test_update_item_invalid(self):
        """Test actualizar ítem inexistente"""
        update_data = {
            "description": "Updated item"
        }
        response = client.put("/lists/1/items/999", json=update_data)
        assert response.status_code == 404
    
    def test_complete_item_valid(self):
        """Test marcar ítem como completado"""
        # Crear un ítem
        create_data = {
            "description": "Item to complete",
            "completed": False
        }
        create_response = client.post("/lists/1/items/", json=create_data)
        item_id = create_response.json()["id"]
        
        # Completar el ítem
        response = client.patch(f"/lists/1/items/{item_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == True
    
    def test_delete_item_valid(self):
        """Test eliminar un ítem válido"""
        # Crear un ítem
        create_data = {
            "description": "Item to delete",
            "completed": False
        }
        create_response = client.post("/lists/1/items/", json=create_data)
        item_id = create_response.json()["id"]
        
        # Eliminar el ítem
        response = client.delete(f"/lists/1/items/{item_id}")
        assert response.status_code == 204
        
        # Verificar que fue eliminado
        get_response = client.get(f"/lists/1/items/")
        items = get_response.json()
        assert not any(item["id"] == item_id for item in items)
    
    def test_delete_item_invalid(self):
        """Test eliminar ítem inexistente"""
        response = client.delete("/lists/1/items/999")
        assert response.status_code == 404

# Fixtures para limpiar datos entre tests si es necesario
@pytest.fixture(autouse=True)
def reset_db():
    """Reset the fake database before each test"""
    from app.routes.items import fake_items_db
    # Guardar estado inicial y restaurar después del test
    original_items = fake_items_db.copy()
    yield
    fake_items_db.clear()
    fake_items_db.extend(original_items)