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

# --- COLORES INSTITUCIONALES CONSUBANCO ---
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
    h1, h2, h3 {{ color: {COLOR_AZUL}; font-family: 'Arial'; }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE BASE DE DATOS ---
def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])
    return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'db' not in st.session_state:
    st.session_state.db = cargar_datos()

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# --- FUNCIONES TÉCNICAS ---
def generar_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(10, 30) * 100
        plazo = random.choice([12, 18, 24, 36, 48, 60])
        return {"p": f"PAGO TOTAL: El descuento mensual es de ${pago:,.0f} a un plazo de {plazo} meses. ¿Cuál es el Monto Total?", "c": str(pago * plazo)}
    elif nivel == "Avanzado":
        opcion = random.choice(["cat", "insolutos"])
        if opcion == "cat": return {"p": "¿Qué siglas definen el costo total del crédito?", "c": "cat"}
        else: return {"p": "¿Cómo se llama el esquema donde el interés disminuye conforme se paga?", "c": "saldos insolutos"}
    else:
        return {"p": "¿Por qué en Consubanco el cliente NUNCA genera interés compuesto?", "c": "tasa fija"}

# --- INTERFAZ DE USUARIO ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **MODO DE INGRESO:**")
    st.write("1. APELLIDOS\n2. NOMBRE(S)")
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    
    with st.expander("🔐 Acceso Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Por favor, ingresa tu nombre (APELLIDOS PRIMERO) en la barra lateral.")
else:
    # Lógica de Instructor (Limpieza y Acceso Total)
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    if es_instructor and 'limpieza_hecha' not in st.session_state:
        st.session_state.db = st.session_state.db[st.session_state.db["Nombre"] != MI_NOMBRE_CONTROL]
        guardar_datos(st.session_state.db)
        st.session_state.limpieza_hecha = True

    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    num_intentos = len(hist)
    
    # Nivel para la pestaña de Evaluación
    if es_instructor:
        nivel, rango = "Experto", "Diamante (Admin)"
    elif num_intentos > 0 and hist.iloc[-1]["Calificación"] >= 10:
        ultimo_nv = hist.iloc[-1]["Nivel"]
        nivel = "Avanzado" if ultimo_nv == "Básico" else "Experto"
        rango = "Plata" if ultimo_nv == "Básico" else "Oro"
    else:
        nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_raw}</h2><p><b>Rango Actual:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    # Pestañas habilitadas globalmente
    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay Modelo B", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    with tabs[0]:
        st.subheader("Evaluación de Conocimientos")
        if st.button("Nueva Pregunta") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        st.info(st.session_state.ejercicio_actual["p"])
        resp = st.text_input("Tu respuesta:", key="eval_ans").strip().lower()
        if st.button("Validar"):
            calif = 10.0 if resp == st.session_state.ejercicio_actual["c"] else 0.0
            log = {"Nombre": nombre_raw, "Nivel": nivel, "Calificación": calif, "Intentos": num_intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            guardar_datos(st.session_state.db)
            st.session_state.ejercicio_actual = None
            st.rerun()

    with tabs[1]:
        st.subheader("🎙️ Práctica de Guion")
        st.info("Escribe tu speech para validar que incluyas los pilares del Modelo B.")
        st.text_area("Caja de texto para el guion de llamada...", height=200)

    with tabs[2]:
        st.subheader("📚 Material de Estudio")
        # El Canva solo se ve si puso la clave de admin en la sidebar
        if is_admin:
            canva_url = "https://www.canva.com/design/DAHA28GoS8E/4gQn7nxFU_eDZx6KMy5ylQ/view?embed"
            components.iframe(canva_url, height=600, scrolling=True)
        else:
            st.info("💡 El material visual interactivo se habilita durante la sesión con el instructor.")
        
        st.markdown("---")
        st.write("**Conceptos Fundamentales:**")
        with st.expander("Glosario"):
            st.write("- **Saldos Insolutos:** El interés se cobra sobre lo que debes, no sobre el monto original.")
            st.write("- **Tasa Fija:** Tu descuento no cambia durante toda la vida del crédito.")

    with tabs[3]:
        st.subheader("🕹️ Centro de Juegos (Refuerzo)")
        st.write("Practica de forma divertida antes de tu evaluación.")
        st.button("Sopa de Letras")
        st.button("Ahorcado Financiero")

    with tabs[4]:
        st.subheader("📊 Mi Progreso")
        st.dataframe(hist, use_container_width=True)
        if is_admin:
            st.markdown("---")
            st.write("Admin: Base de datos completa")
            st.dataframe(st.session_state.db)