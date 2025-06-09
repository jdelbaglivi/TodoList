# TodoList MCP - Gestión de Tareas con Model Context Protocol

Este proyecto implementa un sistema de gestión de tareas que integra una API REST con herramientas MCP (Model Context Protocol), permitiendo su uso directo desde clientes como Claude Desktop.

## Características

- **API REST completa** con endpoints para gestión de tareas
- **Servidor MCP** con herramientas compatibles con Claude Desktop
- **Base de datos SQLite** para persistencia de datos
- **Tests automáticos** con pytest
- **Configuración simple** en un solo paso

## Requisitos Previos

- **Python 3.11 o superior**
- **Git**
- **Claude Desktop** (para usar las herramientas MCP)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/jdelbaglivi/TodoList.git
cd TodoList
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el proyecto

```bash
python run.py
```

Esto iniciará tanto el servidor API REST como el servidor MCP.

## Configuración de Claude Desktop

Para usar las herramientas MCP en Claude Desktop, necesitas configurar el archivo de configuración:

### Windows
1. Abre el archivo de configuración de Claude Desktop ubicado en:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

### macOS
1. Abre el archivo de configuración de Claude Desktop ubicado en:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

### Linux
1. Abre el archivo de configuración de Claude Desktop ubicado en:
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

### 2. Agregar la configuración MCP

Si el archivo no existe, créalo. Agrega o modifica el contenido para incluir:

```json
{
  "mcpServers": {
    "todolist": {
      "command": "python",
      "args": ["/ruta/completa/a/tu/proyecto/TodoList/mcp_server.py"],
      "env": {}
    }
  }
}
```

**Importante:** Reemplaza `/ruta/completa/a/tu/proyecto/TodoList/mcp_server.py` con la ruta real donde clonaste el repositorio.

**Ejemplo para Windows:**
```json
{
  "mcpServers": {
    "todolist": {
      "command": "python",
      "args": ["C:\\Users\\TuUsuario\\TodoList\\mcp_server.py"],
      "env": {}
    }
  }
}
```

**Ejemplo para macOS/Linux:**
```json
{
  "mcpServers": {
    "todolist": {
      "command": "python",
      "args": ["/home/tuusuario/TodoList/mcp_server.py"],
      "env": {}
    }
  }
}
```

### 3. Reiniciar Claude Desktop

Después de guardar la configuración, reinicia completamente Claude Desktop para que los cambios tomen efecto.

## Uso

### Desde Claude Desktop

Una vez configurado, puedes usar los siguientes comandos en Claude Desktop:

- **Ver todas las listas**: "Muéstrame todas mis listas"
- **Crear una lista**: "Crea una lista llamada 'Compras'"
- **Ver items de una lista**: "Muéstrame los items de la lista Trabajo"
- **Agregar item**: "Agrega 'Comprar leche' a la lista Compras"
- **Completar item**: "Marca como completado el item 'Comprar leche'"
- **Eliminar item**: "Elimina el item 'Comprar leche' de la lista Compras"

### Herramientas MCP Disponibles

- `get_lists()` - Obtiene todas las listas
- `create_list(name)` - Crea una nueva lista
- `get_items(list_id)` - Obtiene items de una lista específica
- `create_item(list_id, description)` - Crea un nuevo item
- `update_item(list_id, item_id, description, completed)` - Actualiza un item
- `complete_item(list_id, item_id)` - Marca un item como completado
- `delete_item(list_id, item_id)` - Elimina un item

### API REST

El servidor también expone una API REST en `http://localhost:8000`:

- `GET /lists` - Listar todas las listas
- `POST /lists` - Crear nueva lista
- `GET /lists/{list_id}/items` - Obtener items de una lista
- `POST /lists/{list_id}/items` - Crear nuevo item
- `PUT /lists/{list_id}/items/{item_id}` - Actualizar item
- `DELETE /lists/{list_id}/items/{item_id}` - Eliminar item

## Ejecutar Tests

```bash
pytest tests/
```

## Estructura del Proyecto

```
TodoList/
├── api/
│   ├── __init__.py
│   ├── models.py
│   ├── database.py
│   └── routes.py
├── mcp/
│   ├── __init__.py
│   └── server.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_mcp.py
├── mcp_server.py
├── run.py
├── requirements.txt
└── README.md
```

## Verificación de la Instalación

### 1. Verificar que el servidor esté corriendo
Después de ejecutar `python run.py`, deberías ver:
```
Servidor API iniciado en http://localhost:8000
Servidor MCP iniciado
```

### 2. Verificar la conexión MCP en Claude Desktop
1. Abre Claude Desktop
2. Inicia una nueva conversación
3. Pregunta: "¿Qué listas de tareas tengo?"
4. Si está configurado correctamente, Claude debería responder usando las herramientas MCP

### 3. Verificar la API REST
Visita `http://localhost:8000/docs` en tu navegador para ver la documentación interactiva de la API.

## Solución de Problemas

### Error: "No se puede conectar al servidor MCP"
1. Verifica que la ruta en `claude_desktop_config.json` sea correcta
2. Asegúrate de que Python esté en tu PATH
3. Verifica que las dependencias estén instaladas
4. Reinicia Claude Desktop completamente

### Error: "Módulo no encontrado"
```bash
pip install -r requirements.txt
```

### Error: "Puerto en uso"
Si el puerto 8000 está ocupado, modifica el puerto en `run.py`.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Si tienes problemas con la configuración:

1. Verifica que todos los requisitos estén instalados
2. Revisa que las rutas en la configuración sean correctas
3. Asegúrate de reiniciar Claude Desktop después de cambiar la configuración
4. Consulta los logs de Claude Desktop para errores específicos
