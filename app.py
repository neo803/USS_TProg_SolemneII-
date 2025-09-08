import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="DataViz Chile - Análisis de Datos Públicos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">📊 DataViz Chile - Análisis de Datos Públicos</h1>', unsafe_allow_html=True)

# Funciones para obtener datos de APIs
@st.cache_data(ttl=3600)  # Cache por 1 hora
def obtener_indicadores_economicos(indicador, año='2024'):
    """Obtiene indicadores económicos desde mindicador.cl"""
    try:
        url = f'https://mindicador.cl/api/{indicador}/{año}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "serie" in data:
            df = pd.DataFrame(data["serie"])
            df["fecha"] = pd.to_datetime(df["fecha"])
            df = df.sort_values("fecha")
            return df, data.get("nombre", indicador)
        else:
            return None, None
    except Exception as e:
        st.error(f"Error al obtener datos de {indicador}: {str(e)}")
        return None, None

@st.cache_data(ttl=3600)
def obtener_sismos():
    """Obtiene datos de sismos desde la API de Gael Cloud"""
    try:
        url = 'https://api.gael.cloud/general/public/sismos'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data)
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df
    except Exception as e:
        st.error(f"Error al obtener datos de sismos: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def obtener_datos_gobierno():
    """Obtiene datos desde el portal de datos del gobierno de Chile"""
    try:
        # Ejemplo con datos de COVID-19 del gobierno
        url = 'https://api.covid19.cl/api/totales/2024-01-01/2024-12-31'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            if 'fecha' in df.columns:
                df['fecha'] = pd.to_datetime(df['fecha'])
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.warning(f"Datos de gobierno no disponibles: {str(e)}")
        return pd.DataFrame()

# Sidebar para navegación
st.sidebar.title("🔧 Panel de Control")
seccion = st.sidebar.selectbox(
    "Selecciona una sección:",
    ["🏠 Inicio", "💰 Indicadores Económicos", "🌍 Sismos en Chile", "📈 Análisis Comparativo", "📊 Dashboard Interactivo"]
)

if seccion == "🏠 Inicio":
    st.markdown("## Bienvenido al Sistema de Análisis de Datos Públicos de Chile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Objetivos del Proyecto
        - **Integración con APIs REST**: Conexión con fuentes de datos públicas
        - **Análisis de Datos**: Procesamiento y análisis estadístico
        - **Visualización Interactiva**: Gráficos dinámicos y dashboards
        - **Aplicación Web**: Interface intuitiva con Streamlit
        """)
        
        st.markdown("""
        ### 📊 Fuentes de Datos
        - **MinIndicador.cl**: Indicadores económicos de Chile
        - **Gael Cloud**: Datos sísmicos actualizados
        - **Datos.gob.cl**: Portal oficial del gobierno
        """)
    
    with col2:
        st.markdown("### 🔍 Datos Disponibles")
        
        # Mostrar métricas rápidas
        try:
            # Obtener UF del día
            df_uf, _ = obtener_indicadores_economicos('uf')
            if df_uf is not None and not df_uf.empty:
                uf_actual = df_uf['valor'].iloc[-1]
                st.metric("UF Actual", f"${uf_actual:,.0f}", delta=None)
            
            # Obtener dólar del día
            df_dolar, _ = obtener_indicadores_economicos('dolar')
            if df_dolar is not None and not df_dolar.empty:
                dolar_actual = df_dolar['valor'].iloc[-1]
                st.metric("Dólar Actual", f"${dolar_actual:,.0f}", delta=None)
            
            # Datos de sismos
            df_sismos = obtener_sismos()
            if not df_sismos.empty:
                st.metric("Sismos Registrados", len(df_sismos), delta=None)
                
        except Exception as e:
            st.info("Cargando métricas...")

elif seccion == "💰 Indicadores Económicos":
    st.markdown("## 💰 Indicadores Económicos de Chile")
    
    # Selector de indicador
    indicadores = {
        'uf': 'Unidad de Fomento (UF)',
        'dolar': 'Dólar Observado',
        'euro': 'Euro',
        'ipc': 'Índice de Precios al Consumidor',
        'utm': 'Unidad Tributaria Mensual',
        'tpm': 'Tasa de Política Monetaria',
        'bitcoin': 'Bitcoin'
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        indicador_seleccionado = st.selectbox(
            "Selecciona un indicador:",
            list(indicadores.keys()),
            format_func=lambda x: indicadores[x]
        )
    
    with col2:
        año = st.selectbox("Año:", ["2024", "2023", "2022", "2021"])
    
    with col3:
        tipo_grafico = st.selectbox("Tipo de gráfico:", ["Línea", "Area", "Barras"])
    
    if st.button("📊 Analizar Indicador", type="primary"):
        with st.spinner(f"Obteniendo datos de {indicadores[indicador_seleccionado]}..."):
            df, nombre_indicador = obtener_indicadores_economicos(indicador_seleccionado, año)
            
            if df is not None and not df.empty:
                st.success(f"✅ Datos obtenidos exitosamente: {len(df)} registros")
                
                # Métricas principales
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Valor Actual", f"${df['valor'].iloc[-1]:,.2f}")
                
                with col2:
                    promedio = df['valor'].mean()
                    st.metric("Promedio", f"${promedio:,.2f}")
                
                with col3:
                    maximo = df['valor'].max()
                    st.metric("Máximo", f"${maximo:,.2f}")
                
                with col4:
                    minimo = df['valor'].min()
                    st.metric("Mínimo", f"${minimo:,.2f}")
                
                # Gráfico principal
                st.markdown("### 📈 Evolución Temporal")
                
                if tipo_grafico == "Línea":
                    fig = px.line(df, x='fecha', y='valor', 
                                title=f'Evolución de {nombre_indicador or indicadores[indicador_seleccionado]} - {año}')
                elif tipo_grafico == "Area":
                    fig = px.area(df, x='fecha', y='valor',
                                title=f'Evolución de {nombre_indicador or indicadores[indicador_seleccionado]} - {año}')
                else:
                    fig = px.bar(df.tail(30), x='fecha', y='valor',
                               title=f'Últimos 30 registros - {nombre_indicador or indicadores[indicador_seleccionado]}')
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Análisis estadístico
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Estadísticas Descriptivas")
                    stats = df['valor'].describe()
                    st.dataframe(stats)
                
                with col2:
                    st.markdown("### 📈 Análisis de Tendencia")
                    # Calcular variación porcentual
                    if len(df) > 1:
                        variacion = ((df['valor'].iloc[-1] - df['valor'].iloc[0]) / df['valor'].iloc[0]) * 100
                        st.metric("Variación del período", f"{variacion:.2f}%")
                        
                        # Volatilidad
                        volatilidad = df['valor'].std()
                        st.metric("Desviación Estándar", f"${volatilidad:.2f}")
                
                # Tabla de datos
                with st.expander("🔍 Ver datos detallados"):
                    st.dataframe(df.tail(20))
            
            else:
                st.error("❌ No se pudieron obtener datos para el indicador seleccionado")

elif seccion == "🌍 Sismos en Chile":
    st.markdown("## 🌍 Monitoreo Sísmico de Chile")
    
    with st.spinner("Obteniendo datos sísmicos..."):
        df_sismos = obtener_sismos()
        
        if not df_sismos.empty:
            st.success(f"✅ {len(df_sismos)} sismos registrados")
            
            # Filtros
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'Magnitud' in df_sismos.columns:
                    mag_min = st.slider("Magnitud mínima:", 
                                      float(df_sismos['Magnitud'].min()), 
                                      float(df_sismos['Magnitud'].max()), 
                                      float(df_sismos['Magnitud'].min()))
                    df_filtrado = df_sismos[df_sismos['Magnitud'] >= mag_min]
                else:
                    df_filtrado = df_sismos
            
            with col2:
                if 'Profundidad' in df_sismos.columns:
                    prof_max = st.slider("Profundidad máxima (km):", 
                                       0, 
                                       int(df_sismos['Profundidad'].max()), 
                                       int(df_sismos['Profundidad'].max()))
                    df_filtrado = df_filtrado[df_filtrado['Profundidad'] <= prof_max]
            
            with col3:
                mostrar_ultimos = st.number_input("Mostrar últimos N sismos:", 1, len(df_filtrado), min(50, len(df_filtrado)))
                df_filtrado = df_filtrado.tail(mostrar_ultimos)
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            
            if 'Magnitud' in df_filtrado.columns:
                with col1:
                    st.metric("Sismos filtrados", len(df_filtrado))
                with col2:
                    st.metric("Magnitud promedio", f"{df_filtrado['Magnitud'].mean():.1f}")
                with col3:
                    st.metric("Magnitud máxima", f"{df_filtrado['Magnitud'].max():.1f}")
                with col4:
                    if 'Profundidad' in df_filtrado.columns:
                        st.metric("Profundidad promedio", f"{df_filtrado['Profundidad'].mean():.0f} km")
            
            # Gráficos
            if 'Magnitud' in df_filtrado.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Distribución por Magnitud")
                    fig1 = px.histogram(df_filtrado, x='Magnitud', nbins=20,
                                      title="Distribución de Magnitudes")
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    if 'Profundidad' in df_filtrado.columns:
                        st.markdown("### 🕳️ Magnitud vs Profundidad")
                        fig2 = px.scatter(df_filtrado, x='Profundidad', y='Magnitud',
                                        title="Relación Magnitud-Profundidad")
                        st.plotly_chart(fig2, use_container_width=True)
            
            # Timeline de sismos
            if 'Fecha' in df_filtrado.columns and 'Magnitud' in df_filtrado.columns:
                st.markdown("### ⏰ Timeline de Sismos")
                fig3 = px.line(df_filtrado.sort_values('Fecha'), x='Fecha', y='Magnitud',
                             title="Evolución temporal de magnitudes")
                st.plotly_chart(fig3, use_container_width=True)
            
            # Tabla de datos
            with st.expander("🔍 Ver datos detallados"):
                st.dataframe(df_filtrado)
        
        else:
            st.error("❌ No se pudieron obtener datos sísmicos")

elif seccion == "📈 Análisis Comparativo":
    st.markdown("## 📈 Análisis Comparativo de Indicadores")
    
    st.markdown("### Compara múltiples indicadores económicos")
    
    # Selección de indicadores para comparar
    col1, col2 = st.columns(2)
    
    with col1:
        indicadores_disponibles = ['uf', 'dolar', 'euro', 'ipc']
        indicador1 = st.selectbox("Primer indicador:", indicadores_disponibles, key="ind1")
    
    with col2:
        indicador2 = st.selectbox("Segundo indicador:", 
                                [x for x in indicadores_disponibles if x != indicador1], 
                                key="ind2")
    
    año_comparacion = st.selectbox("Año para comparación:", ["2024", "2023"], key="año_comp")
    
    if st.button("🔄 Comparar Indicadores", type="primary"):
        with st.spinner("Obteniendo datos para comparación..."):
            # Obtener datos de ambos indicadores
            df1, nombre1 = obtener_indicadores_economicos(indicador1, año_comparacion)
            df2, nombre2 = obtener_indicadores_economicos(indicador2, año_comparacion)
            
            if df1 is not None and df2 is not None and not df1.empty and not df2.empty:
                # Normalizar fechas para merge
                df1_norm = df1.copy()
                df2_norm = df2.copy()
                
                # Crear gráfico de comparación dual
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Scatter(x=df1_norm['fecha'], y=df1_norm['valor'], name=nombre1 or indicador1),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(x=df2_norm['fecha'], y=df2_norm['valor'], name=nombre2 or indicador2),
                    secondary_y=True,
                )
                
                fig.update_xaxes(title_text="Fecha")
                fig.update_yaxes(title_text=nombre1 or indicador1, secondary_y=False)
                fig.update_yaxes(title_text=nombre2 or indicador2, secondary_y=True)
                
                fig.update_layout(title_text=f"Comparación: {nombre1 or indicador1} vs {nombre2 or indicador2}")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Análisis de correlación si las fechas coinciden
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### 📊 Estadísticas {nombre1 or indicador1}")
                    stats1 = df1['valor'].describe()
                    st.dataframe(stats1)
                
                with col2:
                    st.markdown(f"### 📊 Estadísticas {nombre2 or indicador2}")
                    stats2 = df2['valor'].describe()
                    st.dataframe(stats2)
                
            else:
                st.error("❌ No se pudieron obtener datos para la comparación")

elif seccion == "📊 Dashboard Interactivo":
    st.markdown("## 📊 Dashboard Interactivo")
    
    # Obtener múltiples datos
    with st.spinner("Cargando dashboard..."):
        df_uf, _ = obtener_indicadores_economicos('uf', '2024')
        df_dolar, _ = obtener_indicadores_economicos('dolar', '2024')
        df_sismos = obtener_sismos()
        
        # Layout del dashboard
        if df_uf is not None and not df_uf.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 💰 UF")
                uf_actual = df_uf['valor'].iloc[-1]
                uf_anterior = df_uf['valor'].iloc[-2] if len(df_uf) > 1 else uf_actual
                delta_uf = uf_actual - uf_anterior
                st.metric("Valor UF", f"${uf_actual:,.0f}", f"{delta_uf:+.0f}")
                
                # Gráfico pequeño UF
                fig_uf = px.line(df_uf.tail(30), x='fecha', y='valor', title="UF - Últimos 30 días")
                fig_uf.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig_uf, use_container_width=True)
            
            if df_dolar is not None and not df_dolar.empty:
                with col2:
                    st.markdown("### 💵 Dólar")
                    dolar_actual = df_dolar['valor'].iloc[-1]
                    dolar_anterior = df_dolar['valor'].iloc[-2] if len(df_dolar) > 1 else dolar_actual
                    delta_dolar = dolar_actual - dolar_anterior
                    st.metric("Valor Dólar", f"${dolar_actual:,.0f}", f"{delta_dolar:+.0f}")
                    
                    # Gráfico pequeño Dólar
                    fig_dolar = px.line(df_dolar.tail(30), x='fecha', y='valor', title="Dólar - Últimos 30 días")
                    fig_dolar.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig_dolar, use_container_width=True)
            
            if not df_sismos.empty and 'Magnitud' in df_sismos.columns:
                with col3:
                    st.markdown("### 🌍 Sismos")
                    sismos_recientes = len(df_sismos.tail(7))  # Últimos 7 registros
                    mag_promedio = df_sismos['Magnitud'].tail(10).mean()
                    st.metric("Sismos recientes", sismos_recientes)
                    st.metric("Mag. promedio", f"{mag_promedio:.1f}")
                    
                    # Gráfico sismos
                    fig_sismos = px.histogram(df_sismos.tail(50), x='Magnitud', title="Distribución Magnitudes")
                    fig_sismos.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig_sismos, use_container_width=True)
        
        # Sección de resumen
        st.markdown("---")
        st.markdown("### 📋 Resumen del Proyecto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔧 Tecnologías Utilizadas:**
            - Python 3.x
            - Streamlit para la interfaz web
            - Requests para consumo de APIs
            - Pandas para análisis de datos
            - Plotly para visualizaciones interactivas
            - APIs REST públicas de Chile
            """)
        
        with col2:
            st.markdown("""
            **📊 Funcionalidades Implementadas:**
            - Conexión a múltiples APIs REST
            - Análisis estadístico de datos
            - Visualizaciones interactivas
            - Dashboard en tiempo real
            - Comparación de indicadores
            - Filtros dinámicos
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎓 Proyecto Final - DataViz Python | Universidad San Sebastián</p>
    <p>Desarrollado por CNJ usando Streamlit y APIs públicas de Chile</p>
</div>
""", unsafe_allow_html=True)