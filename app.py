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
    banco = [
        {"p": "¿Cómo se llama el cobro de interés sobre el capital pendiente?", "c": ["insoluto", "saldos insolutos", "saldo insoluto"], "r": "Retroalimentación: Los saldos insolutos permiten ahorrar intereses al liquidar antes."},
        {"p": "¿Qué siglas definen el costo anual total?", "c": ["cat"], "r": "Retroalimentación: El CAT suma tasa, seguros y comisiones."},
        {"p": "¿Portal para validar capacidad del pensionado IMSS?", "c": ["sipre"], "r": "Retroalimentación: El SIPRE es vital para conocer la capacidad de descuento real."},
        {"p": "¿Cómo se llama la tasa que no cambia nunca?", "c": ["tasa fija", "fija"], "r": "Retroalimentación: La tasa fija da seguridad al cliente ante la inflación."},
        {"p": "¿Qué documento oficial vigente es indispensable?", "c": ["ine"], "r": "Retroalimentación: El INE vigente es el requisito número uno."},
        {"p": "¿Cómo se le llama al dinero neto que recibe el cliente?", "c": ["capital"], "r": "Retroalimentación: El capital es el monto base del préstamo."},
        {"p": "¿En Consubanco cobramos intereses sobre intereses? (Si/No)", "c": ["no", "falso"], "r": "Retroalimentación: No aplicamos interés compuesto para proteger al cliente."}
    ]
    return random.choice(banco)

def generar_practico():
    pago = random.randint(10, 40) * 100
    plazo = random.choice([12, 24, 36, 48, 60, 72, 84, 96])
    total = pago * plazo
    return {
        "p": f"Un cliente tiene un descuento de ${pago:,.0f} a un plazo de {plazo} meses. ¿Cuál es el Monto Total que pagará?",
        "c": str(total),
        "r": f"Retroalimentación: Multiplica ${pago:,.0f} x {plazo} meses = ${total:,.0f}."
    }

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.markdown("""
    <div class='instrucciones-box'>
    <b>📋 INSTRUCCIONES DE ACCESO:</b><br><br>
    1. <b>Registro:</b> Ingresa nombre por APELLIDOS.<br>
    2. <b>Navegación:</b> Usa las pestañas superiores.<br>
    3. <b>Evaluación:</b> Elige módulo y valida respuesta.
    </div>
    """, unsafe_allow_html=True)
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

    st.markdown(f"<div class='rango-box'><h2>Bienvenido, {nombre_raw}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    with tabs[0]:
        st.subheader("Evaluación Dinámica")
        mod_sel = st.radio("Módulo:", ["Teoría y Conceptos", "Laboratorio de Cálculos"], horizontal=True)
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
        if st.button("Validar"):
            correctas = ej["c"]
            es_valida = resp in correctas if isinstance(correctas, list) else resp == correctas
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

    # --- CORRECCIÓN EN EL ANÁLISIS MÉTODO B ---
    with tabs[1]:
        st.subheader("🎙️ Análisis Método B")
        speech = st.text_area("Pega tu speech aquí:", height=150)
        if st.button("Analizar Speech"):
            t = speech.lower()
            errs = []
            
            # Validación de Saludo
            if not any(x in t for x in ["hola", "buen", "buenos días", "buenas tardes"]): 
                errs.append("- 🚩 Falta un saludo profesional inicial.")
            
            # Validación de Oferta Económica (MEJORADA)
            # Ahora busca palabras clave O símbolos de dinero/números de miles
            tiene_oferta = any(x in t for x in ["monto", "pago", "descuento", "$", "pesos", "000"])
            if not tiene_oferta: 
                errs.append("- 🚩 Falta mencionar la oferta económica o condiciones del crédito.")
            
            # Validación de Marca
            if "consubanco" not in t: 
                errs.append("- 🚩 Es vital mencionar el respaldo de Consubanco.")
            
            if not errs: 
                st.success("¡Excelente! Tu speech cumple con los pilares del Método B.")
            else: 
                st.error("Retroalimentación de Speech:")
                for e in errs: st.write(e)

    with tabs[2]:
        st.subheader("📚 Glosario con Tips de Venta")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital"):
                st.write("Monto neto prestado.")
                st.info("💡 Tip: Explicar que el pago a capital reduce el interés futuro.")
            with st.expander("📌 CAT"):
                st.write("Costo Anual Total.")
                st.info("💡 Tip: Transparencia total vs competencia.")
        with c2:
            with st.expander("📌 Saldos Insolutos"):
                st.write("Interés sobre el saldo pendiente.")
                st.info("💡 Tip: Ideal para clientes que quieren liquidar antes.")
            with st.expander("📌 Tasa Fija"):
                st.success("✅ Tip: El descuento no sube nunca.")

    with tabs[4]:
        st.subheader("📊 Historial")
        st.dataframe(hist[["Fecha", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.write("### Panel Administrador")
            st.dataframe(st.session_state.db)
            st.download_button("📥 Exportar CSV", st.session_state.db.to_csv(index=False), "Reporte_Academia.csv")