import pytest
import requests_mock
from app.mcp_server import safe_request as make_api_request
from app.mcp_server import get_lists, get_items, create_item, create_list


class TestMCPServerHelpers:
    """Tests para las funciones auxiliares del servidor MCP"""

    def test_make_api_request_get_success(self):
        with requests_mock.Mocker() as m:
            m.get('http://localhost:8000/test', json={'status': 'ok'})
            result = make_api_request('GET', 'http://localhost:8000/test')
            assert result == {'status': 'ok'}

    def test_make_api_request_post_success(self):
        with requests_mock.Mocker() as m:
            m.post('http://localhost:8000/test', json={'id': 1}, status_code=201)
            result = make_api_request('POST', 'http://localhost:8000/test', {'data': 'test'})
            assert result == {'id': 1}

    def test_make_api_request_delete_success(self):
        with requests_mock.Mocker() as m:
            m.delete('http://localhost:8000/test', status_code=204)
            result = make_api_request('DELETE', 'http://localhost:8000/test')
            assert result == {"message": "Operación exitosa", "status": "success"}

    def test_make_api_request_http_error(self):
        with requests_mock.Mocker() as m:
            m.get('http://localhost:8000/test', status_code=404, json={"detail": "No encontrado"})
            result = make_api_request('GET', 'http://localhost:8000/test')
            assert "error" in result
            assert "Error 404" in result["error"]


class TestMCPTools:
    """Tests para las herramientas MCP (funciones registradas con @mcp.tool())"""

    def test_get_lists_success(self):
        with requests_mock.Mocker() as m:
            m.get('http://localhost:8000/lists', json=[
                {"id": 1, "name": "Trabajo"},
                {"id": 2, "name": "Casa"}
            ])
            result = get_lists()
            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["name"] == "Trabajo"

    def test_get_lists_empty(self):
        with requests_mock.Mocker() as m:
            m.get('http://localhost:8000/lists', json=[])
            result = get_lists()
            assert isinstance(result, list)
            assert result == []

    def test_create_list_success(self):
        with requests_mock.Mocker() as m:
            m.post('http://localhost:8000/lists', json={
                "id": 3,
                "name": "Nueva Lista"
            }, status_code=201)
            result = create_list("Nueva Lista")
            assert isinstance(result, dict)
            assert result["name"] == "Nueva Lista"
            assert result["id"] == 3

    def test_get_items_success(self):
        with requests_mock.Mocker() as m:
            m.get('http://localhost:8000/lists/1/items', json=[
                {"id": 1, "description": "Tarea 1", "completed": False},
                {"id": 2, "description": "Tarea 2", "completed": True}
            ])
            result = get_items(1)
            assert isinstance(result, list)
            assert len(result) == 2

    def test_create_item_success(self):
        with requests_mock.Mocker() as m:
            m.post('http://localhost:8000/lists/1/items', json={
                "id": 5,
                "description": "Nueva tarea",
                "completed": False,
                "list_id": 1
            }, status_code=201)
            result = create_item(1, "Nueva tarea")
            assert isinstance(result, dict)
            assert result["description"] == "Nueva tarea"

    def test_create_item_error(self):
        with requests_mock.Mocker() as m:
            m.post(
                'http://localhost:8000/lists/1/items',
                status_code=400,
                json={"detail": "Ya existe un ítem con esta descripción"}
            )
            result = create_item(1, "Tarea duplicada")
            assert "error" in result
            assert "Error 400" in result["error"] 

# Configuración opcional para pytest
def pytest_configure(config):
    config.addinivalue_line("markers", "integration: marca para tests de integración")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return
    skip_integration = pytest.mark.skip(reason="usar --integration para correr este test")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
