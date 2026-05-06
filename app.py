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

# --- LÓGICA DE EJERCICIOS CON FLEXIBILIDAD DE LENGUAJE ---
def generar_teoria():
    opciones = [
        {
            "p": "¿Cómo se llama el cobro sobre el capital pendiente?", 
            "c": ["insoluto", "saldos insolutos", "saldo insoluto"], 
            "r": "Retroalimentación: Los saldos insolutos permiten ahorrar intereses al liquidar antes ya que el interés se calcula sobre lo que se debe."
        },
        {"p": "¿Qué siglas definen el costo anual total?", "c": ["cat"], "r": "Retroalimentación: El CAT incluye tasa, comisiones y seguros en un solo indicador para comparar créditos."},
        {"p": "¿Qué portal valida la capacidad del pensionado IMSS?", "c": ["sipre"], "r": "Retroalimentación: El SIPRE es la herramienta oficial de validación de descuentos para el sector IMSS."}
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
    st.markdown("""
    <div class='instrucciones-box'>
    <b>📋 INSTRUCCIONES DE ACCESO:</b><br><br>
    1. <b>Registro:</b> Ingresa tu nombre empezando por APELLIDOS.<br>
    2. <b>Navegación:</b> Usa las pestañas superiores para cambiar de módulo.<br>
    3. <b>Evaluación:</b> Responde y valida. Si fallas, revisa la retroalimentación.<br>
    </div>
    """, unsafe_allow_html=True)

    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    with st.expander("🔐 Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Ingresa tu nombre en el panel lateral para comenzar.")
else:
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    nivel = "Experto" if es_instructor else "Básico"
    rango = "Diamante" if es_instructor else "Bronce"

    st.markdown(f"<div class='rango-box'><h2>Bienvenido, {nombre_raw}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    # --- TAB EVALUACIÓN ---
    with tabs[0]:
        st.subheader("Evaluación Dinámica")
        mod_sel = st.radio("Tipo de ejercicio:", ["Teoría y Conceptos", "Laboratorio de Cálculos"], horizontal=True)
        
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
            # Validación flexible
            resp_correcta = ej["c"]
            es_valida = resp in resp_correcta if isinstance(resp_correcta, list) else resp == resp_correcta
            
            if es_valida:
                st.success("¡Correcto!")
                calif = 10.0
            else:
                st.error("Incorrecto.")
                st.warning(ej["r"])
                calif = 0.0
            
            log = {"Nombre": nombre_raw, "Nivel": nivel, "Calificación": calif, "Intentos": len(hist)+1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            guardar_datos(st.session_state.db)

    # --- TAB GLOSARIO CON TIPS COMPLETOS ---
    with tabs[2]:
        if is_admin:
            components.iframe("https://www.canva.com/design/DAHA28GoS8E/4gQn7nxFU_eDZx6KMy5ylQ/view?embed", height=500)
            st.markdown("---")
        
        st.subheader("📚 Glosario y Tips de Venta")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital"):
                st.write("**Definición:** El monto real que se presta al cliente.")
                st.info("💡 **Tip:** Explica que cada pago reduce el capital, lo que disminuye el interés total a largo plazo.")
            with st.expander("📌 CAT"):
                st.write("**Definición:** Costo Anual Total (tasa + comisiones + seguros).")
                st.info("💡 **Tip:** Úsalo para demostrar que no tenemos letras chiquitas comparado con la competencia.")
            with st.expander("📌 Tasa Fija"):
                st.write("**Definición:** Interés que no cambia durante el crédito.")
                st.success("✅ **Tip:** Véndelo como seguridad: 'Su descuento será el mismo hoy y en 5 años'.")
        with c2:
            with st.expander("📌 Saldos Insolutos"):
                st.write("**Definición:** Interés cobrado solo sobre lo que falta pagar.")
                st.info("💡 **Tip:** Es el mejor argumento para clientes que quieren liquidar antes de tiempo.")
            with st.expander("📌 SIPRE"):
                st.write("**Definición:** Portal de validación para pensionados IMSS.")
                st.info("💡 **Tip:** Valida rápido para no generar falsas expectativas al cliente.")
            with st.expander("📋 Requisitos"):
                st.write("- INE Vigente\n- Correo con acceso a SIPRE\n- WhatsApp activo")