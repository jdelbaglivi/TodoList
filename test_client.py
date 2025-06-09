#!/usr/bin/env python3
"""
Cliente de pruebas para el servidor MCP TodoList
Simula prompts naturales y los convierte en llamadas a las herramientas MCP
"""

import requests
import json
import re
from typing import Dict, Any, Optional

class TodoListMCPClient:
    def __init__(self, mcp_server_url: str = "http://localhost:8001"):
        self.mcp_server_url = mcp_server_url
        self.available_tools = {}
        self.load_tools()
    
    def load_tools(self):
        """Carga las herramientas disponibles desde el servidor MCP."""
        try:
            response = requests.get(f"{self.mcp_server_url}/.well-known/mcp.json")
            if response.status_code == 200:
                mcp_info = response.json()
                for tool in mcp_info.get("tools", []):
                    self.available_tools[tool["name"]] = tool
                print(f"✅ Herramientas MCP cargadas: {list(self.available_tools.keys())}")
            else:
                print(f"❌ Error al cargar herramientas MCP: {response.status_code}")
        except Exception as e:
            print(f"❌ Error de conexión con servidor MCP: {e}")
    
    def parse_natural_command(self, prompt: str) -> Dict[str, Any]:
        """Convierte un prompt natural en una llamada a herramienta MCP."""
        prompt_lower = prompt.lower().strip()
        
        # Patrones para diferentes comandos
        patterns = [
            # Crear ítem
            (r"crear?\s+(?:un\s+)?(?:ítem|item|tarea)\s+en\s+(?:la\s+)?lista\s+['\"]?(\w+)['\"]?\s+con\s+(?:la\s+)?descripci[oó]n\s+['\"]([^'\"]+)['\"]?", 
             "create_item", ["list_name", "description"]),
            (r"a[ñn]adir?\s+['\"]([^'\"]+)['\"]?\s+a\s+(?:la\s+)?lista\s+['\"]?(\w+)['\"]?", 
             "create_item", ["description", "list_name"]),
            
            # Obtener ítems
            (r"(?:mostrar|obtener|ver)\s+(?:los\s+)?(?:ítems?|items?|tareas?)\s+de\s+(?:la\s+)?lista\s+['\"]?(\w+)['\"]?", 
             "get_items", ["list_name"]),
            (r"¿?qu[eé]\s+hay\s+en\s+(?:la\s+)?lista\s+['\"]?(\w+)['\"]?", 
             "get_items", ["list_name"]),
            
            # Completar ítem
            (r"(?:marcar\s+como\s+)?completar?\s+(?:el\s+)?(?:ítem|item|tarea)\s+(\d+)\s+de\s+(?:la\s+)?lista\s+['\"]?(\w+)['\"]?", 
             "complete_item", ["item_id", "list_name"]),
            (r"terminar?\s+(?:el\s+)?(?:ítem|item|tarea)\s+(\d+)\s+en\s+['\"]?(\w+)['\"]?", 
             "complete_item", ["item_id", "list_name"]),
            
            # Eliminar ítem
            (r"eliminar?\s+(?:el\s+)?(?:ítem|item|tarea)\s+(\d+)\s+de\s+(?:la\s+)?lista\s+['\"]?(\w+)['\"]?", 
             "delete_item", ["item_id", "list_name"]),
            (r"borrar?\s+(?:el\s+)?(?:ítem|item|tarea)\s+(\d+)\s+de\s+['\"]?(\w+)['\"]?", 
             "delete_item", ["item_id", "list_name"]),
            
            # Actualizar ítem
            (r"actualizar?\s+(?:el\s+)?(?:ítem|item|tarea)\s+(\d+)\s+de\s+(?:la\s+)?lista\s+['\"]?(\w+)['\"]?\s+con\s+descripci[oó]n\s+['\"]([^'\"]+)['\"]?", 
             "update_item", ["item_id", "list_name", "description"]),
            
            # Ver listas
            (r"(?:mostrar|obtener|ver)\s+(?:las\s+)?listas?", "get_lists", []),
            (r"¿?qu[eé]\s+listas?\s+hay", "get_lists", []),
        ]
        
        for pattern, tool_name, param_names in patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                params = {}
                groups = match.groups()
                
                for i, param_name in enumerate(param_names):
                    if i < len(groups) and groups[i]:
                        value = groups[i].strip()
                        # Convertir a entero si es necesario
                        if param_name in ["item_id"]:
                            try:
                                value = int(value)
                            except ValueError:
                                continue
                        params[param_name] = value
                
                return {
                    "tool": tool_name,
                    "parameters": params
                }
        
        return {"tool": None, "parameters": {}, "error": "No se pudo interpretar el comando"}
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una herramienta MCP."""
        if tool_name not in self.available_tools:
            return {"error": f"Herramienta '{tool_name}' no disponible"}
        
        try:
            # Mapear herramientas a endpoints
            endpoint_map = {
                "create_item": "/tools/create_item",
                "get_items": "/tools/get_items",
                "update_item": "/tools/update_item",
                "complete_item": "/tools/complete_item",
                "delete_item": "/tools/delete_item",
                "get_lists": "/tools/get_lists"
            }
            
            endpoint = endpoint_map.get(tool_name)
            if not endpoint:
                return {"error": f"Endpoint no encontrado para herramienta '{tool_name}'"}
            
            url = f"{self.mcp_server_url}{endpoint}"
            
            # Realizar petición según el tipo de herramienta
            if tool_name == "get_items":
                response = requests.get(url, params=parameters)
            elif tool_name == "get_lists":
                response = requests.get(url)
            else:
                # POST para crear/actualizar/completar/eliminar
                response = requests.post(url, params=parameters)
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                error_msg = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get('detail', error_msg)
                except:
                    pass
                return {"success": False, "error": error_msg}
        
        except Exception as e:
            return {"success": False, "error": f"Error de conexión: {str(e)}"}
    
    def process_prompt(self, prompt: str) -> str:
        """Procesa un prompt natural y devuelve una respuesta."""
        print(f"\n🤖 Procesando: '{prompt}'")
        
        # Parsear el comando
        parsed = self.parse_natural_command(prompt)
        
        if not parsed.get("tool"):
            return f"❌ {parsed.get('error', 'No se pudo interpretar el comando')}"
        
        tool_name = parsed["tool"]
        parameters = parsed["parameters"]
        
        print(f"🔧 Herramienta: {tool_name}")
        print(f"📋 Parámetros: {parameters}")
        
        # Ejecutar la herramienta
        result = self.execute_tool(tool_name, parameters)
        
        if result.get("success"):
            return self.format_success_response(tool_name, result["data"])
        else:
            return f"❌ Error: {result.get('error', 'Error desconocido')}"
    
    def format_success_response(self, tool_name: str, data: Any) -> str:
        """Formatea la respuesta exitosa según el tipo de herramienta."""
        if tool_name == "create_item":
            item = data
            return f"✅ Ítem creado exitosamente:\n   ID: {item['id']}\n   Descripción: {item['description']}\n   Lista: {item['list_id']}\n   Completado: {'Sí' if item['completed'] else 'No'}"
        
        elif tool_name == "get_items":
            if not data:
                return "📋 La lista está vacía"
            
            response = "📋 Ítems en la lista:\n"
            for item in data:
                status = "✅" if item['completed'] else "⏳"
                response += f"   {status} {item['id']}: {item['description']}\n"
            return response.strip()
        
        elif tool_name == "get_lists":
            if not data:
                return "📁 No hay listas disponibles"
            
            response = "📁 Listas disponibles:\n"
            for lista in data:
                response += f"   • {lista['name']} (ID: {lista['id']})\n"
            return response.strip()
        
        elif tool_name == "complete_item":
            item = data
            return f"✅ Ítem completado:\n   ID: {item['id']}\n   Descripción: {item['description']}\n   Estado: Completado"
        
        elif tool_name == "update_item":
            item = data
            return f"✅ Ítem actualizado:\n   ID: {item['id']}\n   Descripción: {item['description']}\n   Completado: {'Sí' if item['completed'] else 'No'}"
        
        elif tool_name == "delete_item":
            return "✅ Ítem eliminado exitosamente"
        
        else:
            return f"✅ Operación exitosa: {data}"

def main():
    """Función principal para probar el cliente MCP."""
    print("🚀 Cliente TodoList MCP - Pruebas con Prompts Naturales")
    print("=" * 60)
    
    client = TodoListMCPClient()
    
    if not client.available_tools:
        print("❌ No se pudieron cargar las herramientas MCP.")
        print("   Asegúrate de que el servidor MCP esté ejecutándose en http://localhost:8001")
        return
    
    # Comandos de prueba
    test_commands = [
        "¿Qué listas hay?",
        "Mostrar los ítems de la lista Trabajo",
        "Crear un ítem en la lista 'Trabajo' con la descripción 'Terminar informe mensual'",
        "Añadir 'Llamar al cliente' a la lista Trabajo",
        "¿Qué hay en la lista Casa?",
        "Completar el ítem 3 de la lista Casa",
        "Eliminar el ítem 1 de la lista Trabajo",
        "Actualizar el ítem 2 de la lista Trabajo con descripción 'Smartphone iPhone actualizado'",
        "Ver los ítems de la lista Trabajo",
    ]
    
    print("\n🧪 Ejecutando comandos de prueba:")
    print("-" * 40)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n[{i}/{len(test_commands)}]")
        response = client.process_prompt(command)
        print(response)
        print("-" * 40)
    
    print("\n🎯 Modo interactivo:")
    print("Escribe comandos naturales (o 'salir' para terminar)")
    print("Ejemplos:")
    print("  - 'Crear un ítem en la lista Casa con la descripción Comprar leche'")
    print("  - 'Mostrar los ítems de la lista Trabajo'")
    print("  - 'Completar el ítem 1 de la lista Casa'")
    print()
    
    while True:
        try:
            user_input = input("💬 Tu comando: ").strip()
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if user_input:
                response = client.process_prompt(user_input)
                print(response)
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()