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

### 2. Ejecutar el proyecto

```bash
python run.py
```

Esto automáticamente:
- Instalará las dependencias necesarias
- Iniciará el servidor API REST
- Iniciará el servidor MCP

## Configuración de Claude Desktop

Para usar las herramientas MCP en Claude Desktop, necesitas configurar el archivo de configuración: 

**NOTA:** Ve hacia Claude Desktop presiona Settings luego Developer y edit Config en caso de que no se encuentre el archivo claude_desktop_config.json

### Ubicación del archivo de configuración

#### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Linux
```
~/.config/Claude/claude_desktop_config.json
```

### Configuración MCP

Agrega la siguiente configuración al archivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "todolist": {
      "command": "python",
      "args": ["/ruta/completa/a/tu/proyecto/TodoList/app/mcp_server.py"],
      "env": {}
    }
  }
}
```

**Importante:** Reemplaza `/ruta/completa/a/tu/proyecto/TodoList/app/mcp_server.py` con la ruta real donde clonaste el repositorio.

### Ejemplos por Sistema Operativo

#### Windows:
```json
{
  "mcpServers": {
    "todolist": {
      "command": "python",
      "args": ["C:/Users/TuUsuario/TodoList/app/mcp_server.py"],
      "env": {}
    }
  }
}
```

#### macOS:
```json
{
  "mcpServers": {
    "todolist": {
      "command": "python3",
      "args": ["/Users/tuusuario/TodoList/app/mcp_server.py"],
      "env": {}
    }
  }
}
```

#### Linux:
```json
{
  "mcpServers": {
    "todolist": {
      "command": "python3",
      "args": ["/home/tuusuario/TodoList/app/mcp_server.py"],
      "env": {}
    }
  }
}
```

### Notas importantes por sistema:

**Windows:** Si el comando `python` no está disponible en tu PATH, usa la ruta completa hacia el ejecutable:
```json
"command": "C:/Users/TU_USUARIO/AppData/Local/Programs/Python/PythonXXX/Scripts/python.exe"
```
Para verificar tu versión de Python: `python --version`

**macOS:** Para encontrar la ubicación exacta de Python, ejecuta en terminal:
```bash
which python3
```
Esto te mostrará la ruta completa (ejemplo: `/usr/bin/python3` o `/opt/homebrew/bin/python3`)

**Linux:** Similar a macOS, usa:
```bash
which python3
```

### Reiniciar Claude Desktop

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
3. Verifica que el archivo `mcp_server.py` exista en la ruta especificada
4. Reinicia Claude Desktop completamente

### Error: "Comando no encontrado" (Python)
- **Windows**: Usa la ruta completa al ejecutable de Python
- **macOS/Linux**: Usa `which python3` para encontrar la ruta correcta

### Error: "Módulo no encontrado"
El script `run.py` instala automáticamente las dependencias, pero si tienes problemas, ejecuta manualmente:
```bash
pip install -r requirements.txt
```

### Error: "Puerto en uso"
Si el puerto 8000 está ocupado, modifica el puerto en `run.py`.

## Soporte

Si tienes problemas con la configuración:

1. Verifica que todos los requisitos estén instalados
2. Revisa que las rutas en la configuración sean correctas
3. Asegúrate de reiniciar Claude Desktop después de cambiar la configuración
4. Consulta los logs de Claude Desktop para errores específicos
5. Usa `which python3` (macOS/Linux) para verificar la ruta correcta de Python