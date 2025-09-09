# Taller de Programación II - Análisis de Datos Públicos 📊

## Descripción del Proyecto

Este proyecto desarrolla una aplicación web interactiva utilizando Python y Streamlit para el análisis y visualización de datos públicos de Chile. La aplicación consume múltiples APIs REST para obtener información actualizada sobre indicadores económicos, datos sísmicos y otros datos gubernamentales.

## 🎯 Objetivos del Proyecto

1. **Integración y aplicación de conocimientos**: Aplicar conocimientos de Python en un contexto práctico
2. **Interacción con APIs REST**: Demostrar habilidad en la utilización de APIs públicas
3. **Análisis de datos**: Utilizar Python para procesar y analizar información
4. **Presentación de resultados**: Crear una aplicación web interactiva con visualizaciones

## 🔧 Tecnologías Utilizadas

- **Python 3.x**
- **Streamlit**: Framework para aplicaciones web
- **Requests**: Consumo de APIs REST
- **Pandas**: Análisis y manipulación de datos
- **Plotly**: Visualizaciones interactivas
- **Matplotlib/Seaborn**: Gráficos estadísticos

## 📊 Fuentes de Datos

1. **MinIndicador.cl** - Indicadores económicos de Chile (UF, Dólar, Euro, IPC, etc.)
2. **Gael Cloud** - Datos sísmicos en tiempo real
3. **Datos.gob.cl** - Portal oficial de datos del gobierno de Chile

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/neo803/USS_TProg_SolemneII-
   cd dataviz-chile
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

5. **Abrir en el navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:8501`
   - Si no se abre automáticamente, visita la URL manualmente
   - También esta disponible en: https://solemne2uss.streamlit.app/

## 📱 Funcionalidades

### 🏠 Página de Inicio
- Descripción del proyecto y objetivos
- Métricas rápidas de indicadores principales
- Información sobre fuentes de datos

### 💰 Indicadores Económicos
- Visualización de UF, Dólar, Euro, IPC, UTM, TPM, Bitcoin
- Análisis estadístico completo
- Gráficos interactivos (línea, área, barras)
- Métricas de tendencia y volatilidad

### 🌍 Sismos en Chile
- Monitoreo sísmico en tiempo real
- Filtros por magnitud y profundidad
- Análisis de distribución y correlaciones
- Timeline de eventos sísmicos

### 📈 Análisis Comparativo
- Comparación entre múltiples indicadores
- Gráficos de doble eje
- Análisis de correlación
- Estadísticas comparativas

### 📊 Dashboard Interactivo
- Vista consolidada de múltiples fuentes
- Métricas en tiempo real
- Resumen ejecutivo del proyecto

## 🏗️ Estructura del Proyecto

```
dataviz-chile/
│
├── app.py                 # Aplicación principal de Streamlit
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación del proyecto
├── api_examples/         # Ejemplos de uso de APIs
│   ├── indicador.py      # API de indicadores básica
│   ├── indicador3.py     # API de indicadores mejorada
│   ├── sismos.py         # API de sismos
│   └── weather.py        # API del clima
└── docs/                 # Documentación adicional
    └── proyecto_final.pdf # Especificaciones del proyecto
```

## 🔄 APIs Utilizadas

### 1. MinIndicador.cl
- **URL**: `https://mindicador.cl/api/{indicador}/{año}`
- **Indicadores disponibles**: uf, dolar, euro, ipc, utm, tpm, bitcoin
- **Formato**: JSON
- **Actualización**: Diaria

### 2. Gael Cloud - Sismos
- **URL**: `https://api.gael.cloud/general/public/sismos`
- **Datos**: Magnitud, profundidad, ubicación, fecha
- **Formato**: JSON
- **Actualización**: Tiempo real

### 3. Datos del Gobierno (datos.gob.cl)
- **Múltiples endpoints** según el dataset
- **Formato**: JSON/CSV
- **Actualización**: Variable según fuente

## 📈 Análisis Implementados

1. **Estadísticas Descriptivas**
   - Media, mediana, desviación estándar
   - Valores máximos y mínimos
   - Percentiles y cuartiles

2. **Análisis de Tendencias**
   - Variación porcentual
   - Crecimiento/decrecimiento
   - Volatilidad

3. **Visualizaciones**
   - Gráficos de línea temporal
   - Histogramas de distribución
   - Gráficos de dispersión
   - Mapas de calor

4. **Análisis Comparativo**
   - Correlaciones entre variables
   - Análisis de múltiples series temporales
   - Comparación de tendencias

## 🎨 Características de la Interfaz

- **Diseño Responsivo**: Se adapta a diferentes tamaños de pantalla
- **Navegación Intuitiva**: Sidebar con secciones claramente definidas
- **Visualizaciones Interactivas**: Gráficos con zoom, hover y filtros
- **