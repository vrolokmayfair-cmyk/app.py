import streamlit as st
import pandas as pd
import random
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Academia Consubanco", layout="wide", page_icon="🏦")

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

# Inicializar base de datos en la sesión
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

def generar_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(10, 30) * 100
        plazo = random.choice([12, 18, 24, 36, 48, 60])
        return {"p": f"PAGO TOTAL: El descuento mensual es de ${pago:,.0f} a un plazo de {plazo} meses. ¿Cuál es el Monto Total a pagar?", "c": str(pago * plazo)}
    elif nivel == "Avanzado":
        opcion = random.choice(["interes", "cat", "insolutos", "amortizacion"])
        if opcion == "interes":
            cap = random.randint(30, 60) * 1000
            total = cap * 1.6
            return {"p": f"INTERÉS ORDINARIO: Un cliente recibe ${cap:,.0f} y paga un total de ${total:,.0f}. ¿A cuánto asciende el interés ordinario total?", "c": str(int(total - cap))}
        elif opcion == "cat":
            return {"p": "¿Qué siglas definen el costo total del crédito incluyendo seguros y comisiones?", "c": "cat"}
        elif opcion == "insolutos":
            return {"p": "¿Cómo se llama el esquema donde el interés disminuye conforme se paga a capital?", "c": "saldos insolutos"}
        else:
            return {"p": "¿Cómo se llama el documento que desglosa pago a pago el capital, interés y saldo pendiente?", "c": "tabla de amortizacion"}
    else:
        return {"p": "¿Por qué en Consubanco el cliente NUNCA genera interés compuesto?", "c": "tasa fija y descuento via pension"}

st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **IMPORTANTE:**")
    st.write("Escribe tu nombre empezando por **APELLIDOS**.")
    st.caption("Ejemplo: SUMANO GARCIA JUAN CARLOS")
    nombre_user = st.text_input("NOMBRE DEL ASESOR:").strip().upper()
    
    st.markdown("---")
    # --- PANEL DE ADMINISTRADOR ---
    with st.expander("🔐 Acceso Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_user:
    st.warning("⬅️ Ingresa tu nombre en el panel lateral para comenzar.")
else:
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_user]
    num_intentos = len(hist)
    
    # Lógica de niveles y rangos
    if num_intentos > 0 and hist.iloc[-1]["Calificación"] >= 10:
        ultimo_nv = hist.iloc[-1]["Nivel"]
        if ultimo_nv == "Básico": nivel, rango = "Avanzado", "Plata"
        elif ultimo_nv == "Avanzado": nivel, rango = "Experto", "Oro"
        else: nivel, rango = "Experto", "Diamante"
    else:
        nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_user}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay Modelo B", "📚 Glosario e Infografías", "📊 Evolución"])

    with tabs[0]:
        if st.button("Nueva Pregunta") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        st.info(st.session_state.ejercicio_actual["p"])
        resp_input = st.text_input("Tu respuesta:").strip().lower()
        if st.button("Validar"):
            if resp_input == st.session_state.ejercicio_actual["c"]:
                st.success("¡Excelente!"); calif = 10.0
            else:
                st.error(f"La respuesta era: {st.session_state.ejercicio_actual['c']}"); calif = 0.0
            
            log = {"Nombre": nombre_user, "Nivel": nivel, "Calificación": calif, "Intentos": num_intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            st.session_state.ejercicio_actual = None

    with tabs[1]:
        st.subheader("🎙️ Entrenamiento Modelo B")
        guion = st.text_area("Escribe tu llamada completa aquí:", height=300)
        if st.button("Calificar"):
            texto = guion.lower()
            pilares = {
                "1. Presentación": ["hola", "buen", "día", "tarde", "noche", "nombre", "habla", "consubanco"],
                "2. Monto": ["$", "monto", "cantidad", "crédito", "pesos"],
                "3. Plazo": ["meses", "plazo", "tiempo"],
                "4. Descuento": ["nómina", "descuento", "pensión", "directo", "automático"],
                "5. Requisitos": ["ine", "vigente", "correo", "sipre", "whatsapp"],
                "6. Forma de Pago": ["fijo", "descuento", "insolutos", "capital", "mensual", "ordinario"],
                "7. Tiempo Depósito": ["depósito", "horas", "hrs", "24", "72"],
                "8. Cierre de Venta": ["iniciar", "proceso", "procedemos", "autoriza", "trámite", "disfrute"]
            }
            puntos = 0
            analisis = []
            for pilar, keys in pilares.items():
                if any(k in texto for k in keys): analisis.append(f"