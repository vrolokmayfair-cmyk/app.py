import streamlit as st
import pandas as pd
import random
import datetime
import string
import os
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Academia Consubanco", layout="wide", page_icon="🏦")

# --- VARIABLES DE CONTROL Y PERSISTENCIA ---
DB_FILE = "database_asesores.csv"
MI_NOMBRE_CONTROL = "SUMANO GARCIA JUAN CARLOS"

# --- COLORES INSTITUCIONALES ---
COLOR_AZUL = "#002D72"
COLOR_NARANJA = "#FF6600"
COLOR_FONDO = "#F4F7F9"

st.markdown(f"""
    <style>
    .main {{ background-color: {COLOR_FONDO}; }}
    .stButton>button {{ 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: {COLOR_AZUL}; color: white; font-weight: bold;
        border: none; transition: 0.3s;
    }}
    .stButton>button:hover {{ background-color: {COLOR_NARANJA}; color: white; }}
    .rango-box {{ 
        padding: 20px; border-radius: 15px; 
        border-left: 8px solid {COLOR_NARANJA}; 
        background-color: white; box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    .word-list {{
        background-color: #E8F0FE; padding: 15px; border-radius: 10px;
        border: 1px solid {COLOR_AZUL}; margin-bottom: 15px;
    }}
    h1, h2, h3 {{ color: {COLOR_AZUL}; font-family: 'Arial'; }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE BASE DE DATOS ---
def cargar_datos():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])
    return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'db' not in st.session_state:
    st.session_state.db = cargar_datos()

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# --- FUNCIONES DE JUEGOS ---
def generar_sopa_letras(palabras, tamaño=12):
    grid = [[random.choice(string.ascii_uppercase) for _ in range(tamaño)] for _ in range(tamaño)]
    for palabra in palabras:
        palabra = palabra.upper().replace(" ", "")
        colocada = False
        intentos = 0
        while not colocada and intentos < 100:
            direccion = random.choice([(0,1), (1,0)]) # Horizontal o Vertical
            fila = random.randint(0, tamaño - 1 if direccion == (0,1) else tamaño - len(palabra))
            col = random.randint(0, tamaño - len(palabra) if direccion == (0,1) else tamaño - 1)
            puedo = True
            for i in range(len(palabra)):
                if grid[fila + i*direccion[0]][col + i*direccion[1]] not in (string.ascii_uppercase + palabra[i]):
                    puedo = False
            if puedo:
                for i in range(len(palabra)):
                    grid[fila + i*direccion[0]][col + i*direccion[1]] = palabra[i]
                colocada = True
            intentos += 1
    return grid

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **MODO DE INGRESO:**")
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    
    with st.expander("🔐 Acceso Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Ingresa tu nombre (APELLIDOS PRIMERO) para comenzar.")
else:
    # Lógica Instructor
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    if es_instructor and 'limpieza_hecha' not in st.session_state:
        st.session_state.db = st.session_state.db[st.session_state.db["Nombre"] != MI_NOMBRE_CONTROL]
        guardar_datos(st.session_state.db)
        st.session_state.limpieza_hecha = True

    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    num_intentos = len(hist)
    
    if es_instructor: nivel, rango = "Experto", "Diamante (Admin)"
    elif num_intentos > 0 and hist.iloc[-1]["Calificación"] >= 10:
        nivel, rango = "Avanzado", "Plata"
    else: nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_raw}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    # --- TAB GLOSARIO (CON CAPITAL, CAT, TASA, REQUISITOS) ---
    with tabs[2]:
        if is_admin:
            components.iframe("https://www.canva.com/design/DAHA28GoS8E/4gQn7nxFU_eDZx6KMy5ylQ/view?embed", height=500)
            st.markdown("---")
        
        st.subheader("📚 Glosario y Tips Financieros")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital"):
                st.write("**Definición:** Monto neto recibido por el cliente.")
                st.info("💡 **Tip:** El pago a capital reduce la deuda real mes con mes.")
            with st.expander("📌 CAT"):
                st.write("**Definición:** Costo Anual Total (incluye seguros y comisiones).")
                st.info("💡 **Tip:** Úsalo para demostrar transparencia absoluta.")
        with c2:
            with st.expander("📋 Requisitos"):
                st.write("- INE Vigente, Correo/SIPRE y WhatsApp.")
            with st.expander("📌 Tasa de Interés"):
                st.write("**Definición:** Costo del dinero prestado.")
                st.success("✅ Tasa fija: seguridad total para el pensionado.")

    # --- TAB JUEGOS (AHORA CON INSTRUCCIONES Y LISTA) ---
    with tabs[3]:
        st.subheader("🕹️ Centro de Entrenamiento")
        op_juego = st.radio("Selecciona actividad:", ["Sopa de Letras", "Ahorcado", "Orden del Proceso"])
        
        if op_juego == "Sopa de Letras":
            st.markdown("""
            ### 🔍 Instrucciones:
            Encuentra las palabras clave de Consubanco ocultas en la cuadrícula. 
            Pueden estar en forma **Horizontal** o **Vertical**.
            """)
            
            palabras_sopa = ["CAPITAL", "CAT", "SIPRE", "INSOLUTOS", "TASA"]
            
            # Mostrar lista de palabras a buscar
            st.markdown(f"""
            <div class='word-list'>
                <b>Palabras a buscar:</b> {' | '.join(palabras_sopa)}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generar Nueva Sopa") or 'sopa_grid' not in st.session_state:
                st.session_state.sopa_grid = generar_sopa_letras(palabras_sopa)
            
            st.table(pd.DataFrame(st.session_state.sopa_grid))

        elif op_juego == "Ahorcado":
            pool = {"CAPITAL": "Monto neto recibido", "CAT": "Costo total del crédito", "SIPRE": "Portal de consulta IMSS"}
            if st.button("Cambiar Palabra") or 'ah_pal' not in st.session_state:
                p, pis = random.choice(list(pool.items()))
                st.session_state.ah_pal, st.session_state.ah_pis = p, pis
            st.info(f"Pista: {st.session_state.ah_pis}")
            resp_ah = st.text_input("Palabra completa:", key="ah_input").upper().strip()
            if st.button("Verificar"):
                if resp_ah == st.session_state.ah_pal: st.balloons()
                else: st.error("Intenta de nuevo")

    # --- TAB EVOLUCIÓN (CON BOTÓN EXPORTAR) ---
    with tabs[4]:
        st.subheader("📊 Mi Historial")
        st.dataframe(hist[["Fecha", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.markdown("---")
            st.write("### Panel de Control (Admin)")
            st.dataframe(st.session_state.db)
            st.download_button(
                label="📥 Exportar CSV",
                data=st.session_state.db.to_csv(index=False).encode('utf-8'),
                file_name=f"Reporte_Academia_{datetime.date.today()}.csv",
                mime='text/csv'
            )