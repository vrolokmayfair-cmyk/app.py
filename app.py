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
    .instrucciones-box {{
        background-color: #E8F0FE; padding: 15px; border-radius: 10px;
        border: 1px solid {COLOR_AZUL}; margin-bottom: 20px;
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
def generar_teoria():
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
        "p": f"CÁLCULO: Un cliente tiene un descuento de ${pago:,.0f} a {plazo} meses. ¿Cuál es su Monto Total?",
        "c": str(total),
        "r": f"Retroalimentación: Multiplica Pago Mensual (${pago:,.0f}) x Plazo ({plazo} meses) = ${total:,.0f}."
    }

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    
    # --- SECCIÓN DE INSTRUCCIONES ---
    st.markdown("""
    <div class='instrucciones-box'>
    <b>📋 INSTRUCCIONES DE ACCESO:</b><br><br>
    1. <b>Registro:</b> Ingresa tu nombre completo empezando por APELLIDOS.<br>
    2. <b>Navegación:</b> Usa las pestañas superiores para alternar entre evaluación, glosario y juegos.<br>
    3. <b>Evaluación:</b> Selecciona el módulo (Teoría o Cálculo) y presiona 'Generar' para iniciar.<br>
    4. <b>Progreso:</b> Tus resultados se guardan automáticamente para tu supervisor.
    </div>
    """, unsafe_allow_html=True)

    st.error("⚠️ **INGRESO DE USUARIO:**")
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    
    with st.expander("🔐 Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Por favor, sigue las instrucciones del panel lateral e ingresa tu nombre.")
else:
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    nivel = "Experto" if es_instructor else "Básico"
    rango = "Diamante" if es_instructor else "Bronce"

    st.markdown(f"<div class='rango-box'><h2>Bienvenido, {nombre_raw}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    # --- TAB EVALUACIÓN EN DOS MÓDULOS ---
    with tabs[0]:
        st.subheader("Módulos de Evaluación Dinámica")
        mod_sel = st.radio("Selecciona el tipo de ejercicio:", ["Teoría y Conceptos", "Laboratorio de Cálculos"], horizontal=True)
        
        if mod_sel == "Teoría y Conceptos":
            if st.button("Generar Pregunta Teórica") or st.session_state.ejercicio_teoria is None:
                st.session_state.ejercicio_teoria = generar_teoria()
            ej = st.session_state.ejercicio_teoria
        else:
            if st.button("Generar Ejercicio de Cálculo") or st.session_state.ejercicio_practico is None:
                st.session_state.ejercicio_practico = generar_practico()
            ej = st.session_state.ejercicio_practico
            
        st.info(ej["p"])
        resp = st.text_input("Tu respuesta:", key=f"ans_{mod_sel}").strip().lower()
        
        if st.button("Validar Respuesta"):
            if resp == ej["c"]:
                st.success("¡Excelente! Respuesta correcta.")
                calif = 10.0
            else:
                st.error("Incorrecto.")
                st.warning(ej["r"])
                calif = 0.0
            
            log = {"Nombre": nombre_raw, "Nivel": nivel, "Calificación": calif, "Intentos": len(hist)+1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            guardar_datos(st.session_state.db)

    # --- TAB ROLEPLAY CON RETROALIMENTACIÓN ---
    with tabs[1]:
        st.subheader("🎙️ Análisis de Speech (Método B)")
        speech = st.text_area("Pega tu speech de venta aquí:", height=150)
        if st.button("Evaluar Estructura"):
            texto = speech.lower()
            retro = []
            score = 0
            if any(x in texto for x in ["hola", "buen día", "buenos días"]): score += 3
            else: retro.append("- 🚩 Falta saludo inicial y presentación.")
            
            if any(x in texto for x in ["monto", "plazo", "pago", "descuento"]): score += 4
            else: retro.append("- 🚩 No mencionaste las condiciones del crédito (monto/pago).")
            
            if any(x in texto for x in ["consubanco", "beneficio", "seguro"]): score += 3
            else: retro.append("- 🚩 Falta resaltar el respaldo de Consubanco.")
            
            st.metric("Calidad de Llamada", f"{score}/10")
            for r in retro: st.info(r)
            if score == 10: st.success("¡Excelente dominio del Método B!")

    # --- TAB GLOSARIO COMPLETO ---
    with tabs[2]:
        if is_admin:
            components.iframe("https://www.canva.com/design/DAHA28GoS8E/4gQn7nxFU_eDZx6KMy5ylQ/view?embed", height=500)
            st.markdown("---")
        st.subheader("📚 Glosario y Tips Financieros")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital"):
                st.write("Monto neto recibido por el cliente.")
                st.info("💡 Tip: El abono a capital reduce la deuda real cada mes.")
            with st.expander("📌 CAT"):
                st.write("Costo Anual Total. Incluye tasa, seguros y comisiones.")
            with st.expander("📌 Tasa Fija"):
                st.success("✅ Garantía: El pago del cliente no subirá jamás.")
        with c2:
            with st.expander("📋 Requisitos"):
                st.write("- INE Vigente, Correo con SIPRE y WhatsApp.")
            with st.expander("📌 Saldos Insolutos"):
                st.write("Cálculo de interés sobre lo que se debe actualmente.")
            with st.expander("📌 SIPRE"):
                st.write("Portal para validar capacidad de pago del pensionado.")

    # --- TAB JUEGOS ---
    with tabs[3]:
        st.subheader("🕹️ Centro de Juegos")
        op = st.radio("Selecciona:", ["Sopa de Letras", "Ahorcado"], horizontal=True)
        if op == "Sopa de Letras":
            st.write("Busca: CAPITAL | CAT | SIPRE | TASA | INSOLUTOS")
            # (Aquí iría la lógica de generación de la sopa ya definida previamente)
            st.info("Función de sopa de letras lista para entrenamiento.")

    # --- TAB EVOLUCIÓN ---
    with tabs[4]:
        st.subheader("📊 Historial Personal")
        st.dataframe(hist[["Fecha", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.write("---")
            st.write("### 🛠️ Administración de Datos")
            st.dataframe(st.session_state.db)
            st.download_button("📥 Descargar Reporte CSV", st.session_state.db.to_csv(index=False), "Reporte_Academia.csv")