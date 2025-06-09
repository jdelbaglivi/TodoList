# TodoList + MCP Tools

Este proyecto extiende una API REST de gestión de tareas incorporando herramientas compatibles con el protocolo [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol), permitiendo su uso desde clientes como Claude Desktop.

## Funcionalidades

- API REST con endpoints para:
  - Crear ítems en listas
  - Actualizar ítems
  - Completar ítems
  - Eliminar ítems
- Servidor MCP con tools compatibles (`get_lists`, `create_item`, `complete_item`, etc.)
- Tests automáticos con `pytest`
- Ejecución unificada en un solo paso

## Requisitos

- Python 3.11 o superior
- Git

## Instalación y ejecución

Cloná el repositorio y ejecutá todo con un solo comando:

```bash
git clone https://github.com/tu_usuario/todolist-mcp.git
cd todolist-mcp
python run.py
