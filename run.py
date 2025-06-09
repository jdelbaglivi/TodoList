import subprocess
import sys

def run_command(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    print("▶ Instalando dependencias...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    run_command(f"{sys.executable} -m pip install -r requirements.txt")

    print("▶ Iniciando pruebas unitarias...")
    run_command(f"{sys.executable} -m pytest tests --disable-warnings -q")

    print("▶ Iniciando API REST (puerto 8000)...")
    api_cmd = f"{sys.executable} -m uvicorn app.main:app --reload"
    subprocess.Popen(api_cmd, shell=True)

    print("▶ Iniciando Servidor MCP (esperando conexiones MCP)...")
    mcp_cmd = f"{sys.executable} app/mcp_server.py"
    subprocess.run(mcp_cmd, shell=True)    

if __name__ == "__main__":
    main()
