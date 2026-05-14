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

# --- LÓGICA DE EJERCICIOS EXPANDIDA (EVITA REPETICIONES) ---
def generar_teoria():
    banco = [
        {"p": "¿Cómo se llama el cobro de interés sobre el capital pendiente?", "c": ["insoluto", "saldos insolutos", "saldo insoluto"], "r": "Retroalimentación: El interés sobre saldos insolutos premia al cliente que paga a tiempo reduciendo su deuda real."},
        {"p": "¿Qué siglas definen el Costo Anual Total (incluye tasa, seguros y comisiones)?", "c": ["cat"], "r": "Retroalimentación: El CAT es la herramienta de transparencia para comparar créditos."},
        {"p": "¿Portal oficial para validar capacidad de descuento del pensionado IMSS?", "c": ["sipre"], "r": "Retroalimentación: El SIPRE es indispensable para evitar rechazos por falta de capacidad."},
        {"p": "¿Cómo se llama la tasa que garantiza estabilidad y no sube con la inflación?", "c": ["tasa fija", "fija"], "r": "Retroalimentación: La tasa fija es seguridad para el bolsillo del cliente."},
        {"p": "¿Qué documento oficial vigente es el requisito #1 para el trámite?", "c": ["ine", "identificacion"], "r": "Retroalimentación: Sin INE vigente no hay proceso; valídalo desde el saludo."},
        {"p": "¿Cómo se le llama al monto neto que efectivamente recibe el cliente?", "c": ["capital"], "r": "Retroalimentación: El capital es el dinero 'líquido' que el cliente usará."},
        {"p": "¿En Consubanco aplicamos interés compuesto (interés sobre interés)? (Sí/No)", "c": ["no", "falso"], "r": "Retroalimentación: No aplicamos anatocismo, lo cual protege el patrimonio del cliente."},
        {"p": "¿Documento que detalla el calendario de pagos, seguros y abonos?", "c": ["tabla de amortización", "tabla de amortizacion", "tabla"], "r": "Retroalimentación: La tabla de amortización da certeza sobre la duración del crédito."},
        {"p": "¿Cómo se llama la capacidad de descuento máxima permitida por ley?", "c": ["capacidad de pago", "capacidad", "descuento maximo"], "r": "Retroalimentación: Cuidar la capacidad de pago asegura la salud financiera del pensionado."},
        {"p": "¿Qué medio de contacto es vital para el envío de documentos y seguimiento?", "c": ["whatsapp", "celular", "correo"], "r": "Retroalimentación: La agilidad en la comunicación cierra ventas."}
    ]
    return random.choice(banco)

def generar_practico():
    # Generación dinámica de valores para evitar repeticiones
    monto_base = random.randint(5, 50) * 1000
    plazo = random.choice([12, 24, 36, 48, 60, 72, 84, 96])
    # Cálculo simulado de pago mensual simple para el ejercicio
    pago_sugerido = round((monto_base * 1.4) / plazo, 0)
    monto_total = pago_sugerido * plazo
    
    opciones_calc = [
        {
            "p": f"CÁLCULO: Si un cliente tiene un descuento mensual de ${pago_sugerido:,.0f} a un plazo de {plazo} meses. ¿Cuál es el Monto Total a pagar?",
            "c": str(int(monto_total)),
            "r": f"Retroalimentación: Multiplica Pago (${pago_sugerido:,.0f}) x Plazo ({plazo}) = ${monto_total:,.0f}."
        },
        {
            "p": f"PRÁCTICA: Un crédito de ${monto_total:,.0f} totales se pagará en {plazo} meses. ¿De cuánto es el descuento mensual?",
            "c": str(int(pago_sugerido)),
            "r": f"Retroalimentación: Divide Total (${monto_total:,.0f}) / Plazo ({plazo}) = ${pago_sugerido:,.0f}."
        }
    ]
    return random.choice(opciones_calc)

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
        st.subheader("Evaluación Dinámica de Conocimientos")
        mod_sel = st.radio("Módulo de aprendizaje:", ["Teoría y Conceptos", "Laboratorio de Cálculos"], horizontal=True)
        
        if mod_sel == "Teoría y Conceptos":
            if st.button("Generar Nueva Pregunta Teórica") or st.session_state.ejercicio_teoria is None:
                st.session_state.ejercicio_teoria = generar_teoria()
            ej = st.session_state.ejercicio_teoria
        else:
            if st.button("Generar Nuevo Ejercicio de Cálculo") or st.session_state.ejercicio_practico is None:
                st.session_state.ejercicio_practico = generar_practico()
            ej = st.session_state.ejercicio_practico
        
        st.info(ej["p"])
        resp = st.text_input("Escribe tu respuesta aquí:", key=f"ans_{mod_sel}").strip().lower()
        
        if st.button("Validar Respuesta"):
            correctas = ej["c"]
            # Soporte para validación flexible de texto o números
            es_valida = resp in correctas if isinstance(correctas, list) else resp == correctas
            
            if es_valida:
                st.success("¡Excelente! Respuesta correcta.")
                calif = 10.0
            else:
                st.error("Respuesta incorrecta.")
                st.warning(ej["r"])
                calif = 0.0
            
            log = {"Nombre": nombre_raw, "Nivel": nivel, "Calificación": calif, "Intentos": len(hist)+1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            guardar_datos(st.session_state.db)

    with tabs[1]:
        st.subheader("🎙️ Análisis Método B (Speech)")
        speech = st.text_area("Pega tu speech de venta aquí:", height=150)
        if st.button("Analizar Speech"):
            t = speech.lower()
            errs = []
            if not any(x in t for x in ["hola", "buen", "presento"]): errs.append("- Falta saludo o presentación inicial.")
            if not any(x in t for x in ["monto", "pago", "pesos", "$", "000"]): errs.append("- Falta la oferta económica clara.")
            if "consubanco" not in t: errs.append("- Olvidaste mencionar el respaldo de Consubanco.")
            
            if not errs: st.success("¡Speech Profesional! Cumple con los pilares del Método B.")
            else: 
                st.error("Puntos a mejorar en tu speech:")
                for e in errs: st.write(e)

    with tabs[2]:
        st.subheader("📚 Glosario Completo y Tips de Venta")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital (El dinero real)"):
                st.write("**Definición:** El monto neto que se entrega al cliente.")
                st.info("💡 **Tip de Venta:** Recuérdale al cliente que sus abonos bajan esta deuda base directamente.")
            with st.expander("📌 CAT (Costo Anual Total)"):
                st.write("**Definición:** Indicador que suma tasa, seguros y comisiones.")
                st.info("💡 **Tip de Venta:** Úsalo para demostrar que no hay cobros ocultos; todo está en el CAT.")
            with st.expander("📌 Tasa Fija"):
                st.write("**Definición:** Interés que permanece igual toda la vida del crédito.")
                st.success("✅ **Tip de Venta:** Ideal para tiempos de inflación: 'Su pago no subirá pase lo que pase'.")
        with c2:
            with st.expander("📌 Saldos Insolutos"):
                st.write("**Definición:** Interés calculado sobre el remanente de la deuda.")
                st.info("💡 **Tip de Venta:** El mejor gancho para quien quiere liquidar antes y ahorrar intereses.")
            with st.expander("📌 SIPRE (Validación IMSS)"):
                st.write("**Definición:** Sistema de validación de capacidad para pensionados.")
                st.info("💡 **Tip de Venta:** 'Validamos en minutos para que se vaya con la seguridad de su aprobación'.")
            with st.expander("📋 Requisitos Indispensables"):
                st.write("- INE Vigente (Frente y Vuelta)\n- Acceso a SIPRE (Pensionados)\n- WhatsApp para agilidad")

    with tabs[4]:
        st.subheader("📊 Historial de Aprendizaje")
        st.dataframe(hist[["Fecha", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.write("---")
            st.write("### Panel de Control (Admin)")
            st.dataframe(st.session_state.db)
            st.download_button("📥 Exportar Reporte Global (CSV)", st.session_state.db.to_csv(index=False), "Reporte_Academia.csv")
            st.dataframe(st.session_state.db)
            st.download_button("📥 Exportar CSV", st.session_state.db.to_csv(index=False), "Reporte_Academia.csv")
