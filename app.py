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
    h1, h2, h3 {{ color: {COLOR_AZUL}; font-family: 'Arial'; }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE DATOS ---
def cargar_datos():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])
    return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'db' not in st.session_state:
    st.session_state.db = cargar_datos()

if 'ejercicio_teoria' not in st.session_state:
    st.session_state.ejercicio_teoria = None

if 'ejercicio_practico' not in st.session_state:
    st.session_state.ejercicio_practico = None

# --- LÓGICA DE EJERCICIOS ---
def generar_teoria(nivel):
    opciones = [
        {"p": "¿Qué siglas definen el costo anual total?", "c": "cat", "r": "Retroalimentación: El CAT incluye tasa, comisiones y seguros en un solo indicador."},
        {"p": "¿Cómo se llama el cobro sobre el capital pendiente?", "c": "saldos insolutos", "r": "Retroalimentación: Los saldos insolutos permiten ahorrar intereses al liquidar antes."},
        {"p": "¿Qué portal valida la capacidad del pensionado IMSS?", "c": "sipre", "r": "Retroalimentación: El SIPRE es la herramienta oficial de validación de descuentos."}
    ]
    return random.choice(opciones)

def generar_practico():
    pago = random.randint(10, 40) * 100
    plazo = random.choice([12, 24, 36, 48, 60])
    total = pago * plazo
    return {
        "p": f"Un cliente tiene un descuento de ${pago:,.0f} a {plazo} meses. ¿Cuál es su Monto Total?",
        "c": str(total),
        "r": f"Retroalimentación: Multiplica Pago Mensual (${pago:,.0f}) x Plazo ({plazo} meses) = ${total:,.0f}."
    }

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    with st.expander("🔐 Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Ingresa tu nombre para comenzar.")
else:
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    nivel = "Experto" if es_instructor else "Básico"
    rango = "Diamante" if es_instructor else "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_raw}</h2><p><b>Rango:</b> {rango} | <b>Nivel:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario", "🕹️ Juegos", "📊 Evolución"])

    with tabs[0]:
        st.subheader("Módulos de Aprendizaje")
        mod_sel = st.radio("Selecciona tu enfoque:", ["Teoría y Conceptos", "Laboratorio de Cálculos"], horizontal=True)
        
        if mod_sel == "Teoría y Conceptos":
            if st.button("Nueva Pregunta Teórica") or st.session_state.ejercicio_teoria is None:
                st.session_state.ejercicio_teoria = generar_teoria(nivel)
            ej = st.session_state.ejercicio_teoria
        else:
            if st.button("Nuevo Ejercicio de Cálculo") or st.session_state.ejercicio_practico is None:
                st.session_state.ejercicio_practico = generar_practico()
            ej = st.session_state.ejercicio_practico
            
        st.info(ej["p"])
        resp = st.text_input("Respuesta:", key=f"ans_{mod_sel}").strip().lower()
        if st.button("Validar"):
            if resp == ej["c"]:
                st.success("¡Correcto!")
            else:
                st.error("Incorrecto")
                st.warning(ej["r"])

    with tabs[1]:
        st.subheader("🎙️ Análisis Método B")
        speech = st.text_area("Escribe tu speech aquí:", height=150)
        if st.button("Evaluar Speech"):
            texto = speech.lower()
            retro = []
            score = 0
            if any(x in texto for x in ["hola", "buen día"]): score += 3
            else: retro.append("- Te faltó un saludo profesional de entrada.")
            
            if any(x in texto for x in ["monto", "plazo", "pago"]): score += 4
            else: retro.append("- Es vital mencionar el monto y el plazo claramente.")
            
            if "consubanco" in texto: score += 3
            else: retro.append("- Recuerda mencionar el respaldo de Consubanco.")
            
            st.metric("Calificación", f"{score}/10")
            if retro:
                for r in retro: st.info(r)
            else: st.success("¡Speech completo y bien estructurado!")

    with tabs[2]:
        st.subheader("📚 Glosario de Venta")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital"):
                st.write("Monto neto recibido. Al pagar a capital, la deuda baja más rápido.")
            with st.expander("📌 CAT"):
                st.write("Costo Total Anual. Herramienta de transparencia para comparar.")
        with c2:
            with st.expander("📋 Requisitos"):
                st.write("INE Vigente, Correo/SIPRE y WhatsApp.")
            with st.expander("📌 Tasa Fija"):
                st.write("Seguridad total: el descuento no sube pase lo que pase.")

    with tabs[4]:
        st.subheader("📊 Mi Progreso")
        st.dataframe(hist[["Fecha", "Calificación"]], use_container_width=True)
        if is_admin:
            st.write("### Panel Admin")
            st.dataframe(st.session_state.db)
            st.download_button("📥 Exportar CSV", st.session_state.db.to_csv(index=False), "Reporte.csv")