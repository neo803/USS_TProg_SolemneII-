"""
Script de configuración e instalación del proyecto DataViz Chile
"""

import os
import sys
import subprocess
import platform

def verificar_python():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True

def instalar_dependencias():
    """Instala las dependencias del proyecto"""
    print("📦 Instalando dependencias...")
    
    try:
        # Actualizar pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def crear_estructura_directorios():
    """Crea la estructura de directorios del proyecto"""
    directorios = [
        'utils',
        'ejemplos',
        'data',
        'exports',
        'logs',
        '.streamlit'
    ]
    
    print("📁 Creando estructura de directorios...")
    
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"   ✅ Creado: {directorio}/")
        else:
            print(f"   ℹ️  Ya existe: {directorio}/")

def crear_archivos_configuracion():
    """Crea archivos de configuración necesarios"""
    print("⚙️ Creando archivos de configuración...")
    
    # Archivo .env de ejemplo
    env_content = """# Variables de entorno para DataViz Chile
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# APIs URLs (opcional para configuración avanzada)
MINDICADOR_API_URL=https://mindicador.cl/api
SISMOS_API_URL=https://api.gael.cloud/general/public/sismos

# Configuración de cache
CACHE_TTL=3600
"""
    
    if not os.path.exists('.env.example'):
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("   ✅ Creado: .env.example")
    
    # Archivo .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data files
*.csv
*.xlsx
*.json
data/
exports/
logs/

# Environment variables
.env

# Streamlit
.streamlit/secrets.toml

# OS
.DS_Store
Thumbs.db
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("   ✅ Creado: .gitignore")

def crear_scripts_utilidad():
    """Crea scripts de utilidad para el proyecto"""
    print("🔧 Creando scripts de utilidad...")
    
    # Script de inicio rápido
    run_script = """#!/bin/bash
# Script de inicio rápido para DataViz Chile

echo "🚀 Iniciando DataViz Chile..."

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si no existen
echo "📋 Verificando dependencias..."
pip install -r requirements.txt

# Ejecutar aplicación
echo "🌐 Iniciando aplicación Streamlit..."
streamlit run app.py

echo "✅ DataViz Chile iniciado correctamente"
"""
    
    # Para Windows
    run_script_win = """@echo off
REM Script de inicio rápido para DataViz Chile (Windows)

echo 🚀 Iniciando DataViz Chile...

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\\Scripts\\activate

REM Instalar dependencias
echo 📋 Verificando dependencias...
pip install -r requirements.txt

REM Ejecutar aplicación
echo 🌐 Iniciando aplicación Streamlit...
streamlit run app.py

echo ✅ DataViz Chile iniciado correctamente
pause
"""
    
    if platform.system() != "Windows":
        with open('run.sh', 'w', encoding='utf-8') as f:
            f.write(run_script)
        os.chmod('run.sh', 0o755)
        print("   ✅ Creado: run.sh")
    
    with open('run.bat', 'w', encoding='utf-8') as f:
        f.write(run_script_win)
    print("   ✅ Creado: run.bat")

def verificar_conectividad():
    """Verifica la conectividad a las APIs"""
    print("🌐 Verificando conectividad a APIs...")
    
    import requests
    
    apis = [
        ("MinIndicador", "https://mindicador.cl/api/uf"),
        ("Sismos", "https://api.gael.cloud/general/public/sismos")
    ]
    
    for nombre, url in apis:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {nombre}: Conectado")
            else:
                print(f"   ⚠️  {nombre}: Respuesta {response.status_code}")
        except Exception as e:
            print(f"   ❌ {nombre}: Error de conexión")

def mostrar_instrucciones():
    """Muestra las instrucciones finales"""
    print("\n" + "="*60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print("\n📋 INSTRUCCIONES DE USO:")
    print("\n1️⃣  Para ejecutar la aplicación:")
    
    if platform.system() == "Windows":
        print("   • Doble clic en run.bat")
        print("   • O ejecutar: streamlit run app.py")
    else:
        print("   • Ejecutar: ./run.sh")
        print("   • O ejecutar: streamlit run app.py")
    
    print("\n2️⃣  Para desarrollo:")
    print("   • Activar entorno virtual:")
    if platform.system() == "Windows":
        print("     venv\\Scripts\\activate")
    else:
        print("     source venv/bin/activate")
    
    print("   • Instalar en modo desarrollo:")
    print("     pip install -e .")
    
    print("\n3️⃣  Para análisis por línea de comandos:")
    print("   • python ejemplos/analisis_completo.py")
    print("   • python ejemplos/analisis_completo.py --demo")
    
    print("\n4️⃣  Archivos importantes:")
    print("   • app.py - Aplicación principal Streamlit")
    print("   • requirements.txt - Dependencias del proyecto")
    print("   • README.md - Documentación completa")
    print("   • utils/data_processing.py - Utilidades de procesamiento")
    
    print("\n5️⃣  URLs útiles:")
    print("   • Aplicación local: http://localhost:8501")
    print("   • Documentación Streamlit: https://docs.streamlit.io")
    
    print("\n🚀 ¡El proyecto está listo para usar!")
    print("="*60)

def main():
    """Función principal del setup"""
    print("🔧 CONFIGURACIÓN DEL PROYECTO DATAVIZ CHILE")
    print("="*50)
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Crear estructura
    crear_estructura_directorios()
    
    # Instalar dependencias
    if not instalar_dependencias():
        print("⚠️  Continuando sin instalar dependencias...")
    
    # Crear configuraciones
    crear_archivos_configuracion()
    
    # Crear scripts
    crear_scripts_utilidad()
    
    # Verificar APIs
    verificar_conectividad()
    
    # Mostrar instrucciones
    mostrar_instrucciones()

if __name__ == "__main__":
    main()