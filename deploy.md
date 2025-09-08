# Guía de Despliegue - DataViz Chile

## 🚀 Despliegue en Streamlit Cloud (Recomendado)

### Paso 1: Preparar el repositorio

1. **Subir el código a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Proyecto DataViz Chile - Universidad San Sebastián"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/dataviz-chile.git
   git push -u origin main
   ```

2. **Verificar estructura de archivos**
   ```
   dataviz-chile/
   ├── app.py                    # ✅ Archivo principal
   ├── requirements.txt          # ✅ Dependencias
   ├── README.md                # ✅ Documentación
   ├── .streamlit/
   │   └── config.toml          # ✅ Configuración
   ├── utils/
   │   └── data_processing.py   # ✅ Utilidades
   └── ejemplos/
       └── analisis_completo.py # ✅ Ejemplos
   ```

### Paso 2: Desplegar en Streamlit Cloud

1. **Ir a Streamlit Cloud**
   - Visita: https://share.streamlit.io
   - Inicia sesión con tu cuenta de GitHub

2. **Crear nueva aplicación**
   - Clic en "New app"
   - Selecciona tu repositorio `dataviz-chile`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL (opcional): `dataviz-chile` o tu nombre preferido

3. **Configuración avanzada (opcional)**
   ```toml
   # En .streamlit/config.toml ya incluido
   [theme]
   primaryColor = "#1f77b4"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   ```

4. **Deploy**
   - Clic en "Deploy!"
   - Esperar a que se complete la instalación
   - Tu app estará disponible en: `https://tu-app.streamlit.app`

## 🐳 Despliegue con Docker

### Paso 1: Construir la imagen

```bash
# Construir imagen Docker
docker build -t dataviz-chile .

# Ejecutar contenedor
docker run -p 8501:8501 dataviz-chile
```

### Paso 2: Docker Compose (opcional)

```yaml
# docker-compose.yml
version: '3.8'
services:
  dataviz-chile:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_ENABLE_CORS=false
    volumes:
      - ./data:/app/data
      - ./exports:/app/exports
```

```bash