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

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

def generar_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(10, 30) * 100
        plazo = random.choice([12, 18, 24, 36])
        return {"p": f"PAGO TOTAL: El descuento mensual es de ${pago:,.0f} a un plazo de {plazo} meses. ¿Cuál es el Monto Total a pagar?", "c": str(pago * plazo)}
    elif nivel == "Avanzado":
        opcion = random.choice(["interes", "cat", "insolutos", "tasa"])
        if opcion == "interes":
            cap = random.randint(30, 60) * 1000
            total = cap * 1.5
            return {"p": f"INTERÉS REAL: Un cliente recibe ${cap:,.0f} y al final paga ${total:,.0f}. ¿Cuánto pagó de PURO INTERÉS?", "c": str(int(total - cap))}
        elif opcion == "cat":
            return {"p": "¿Qué significan las siglas CAT en nuestros contratos?", "c": "costo anual total"}
        elif opcion == "insolutos":
            return {"p": "¿Cómo se llama el esquema donde el interés se calcula sobre el saldo pendiente y no sobre el monto inicial?", "c": "saldos insolutos"}
        else:
            tasa_a = random.choice([48, 60, 72])
            return {"p": f"TASA MENSUAL: Si la Tasa Anual es del {tasa_a}%. ¿Cuál es la tasa mensual?", "c": str(tasa_a // 12)}
    else:
        return {"p": "¿Cuál es el principal beneficio de liquidar antes bajo el esquema de Consubanco?", "c": "ahorra intereses"}

st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **IMPORTANTE:**")
    st.write("Escribe tu nombre empezando por **APELLIDOS**.")
    st.caption("Ejemplo: PEREZ GARCIA JUAN")
    nombre_user = st.text_input("NOMBRE DEL ASESOR:").strip().upper()

if not nombre_user:
    st.warning("⬅️ Ingresa tu nombre en el panel lateral para comenzar.")
else:
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_user]
    num_intentos = len(hist)
    
    if num_intentos > 0 and hist.iloc[-1]["Calificación"] >= 10:
        ultimo_nv = hist.iloc[-1]["Nivel"]
        if ultimo_nv == "Básico": nivel, rango = "Avanzado", "Plata"
        elif ultimo_nv == "Avanzado": nivel, rango = "Experto", "Oro"
        else: nivel, rango = "Experto", "Diamante"
    else:
        nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_user}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay Modelo B", "📚 Infografías", "📊 Evolución"])

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
                "2. Monto": ["$", "monto", "cantidad", "crédito", "70000", "70,000"],
                "3. Plazo": ["meses", "plazo", "60", "sesenta"],
                "4. Descuento": ["nómina", "descuento", "pensión", "directo", "automático"],
                "5. Requisitos": ["ine", "vigente", "correo", "sipre", "acceso", "whatsapp", "teléfono", "celular"],
                "6. Forma de Pago": ["fijo", "descuento", "insolutos", "capital", "mensual"],
                "7. Tiempo Depósito": ["depósito", "horas", "hrs", "24", "72", "cuenta"],
                "8. Cierre de Venta": ["iniciar", "proceso", "procedemos", "autoriza", "le parece bien", "disfrute", "trámite"]
            }
            puntos = 0
            analisis = []
            for pilar, keys in pilares.items():
                if any(k in texto for k in keys): analisis.append(f"✅ {pilar}"); puntos += 1
                else: analisis.append(f"❌ {pilar}")
            st.write("### Análisis de Estructura")
            c1, c2 = st.columns(2)
            for i, res in enumerate(analisis):
                if i < 4: c1.write(res)
                else: c2.write(res)
            calif_rp = (puntos / 8) * 10
            if calif_rp == 10: st.balloons(); st.success(f"Calificación: {calif_rp}/10")
            else: st.warning(f"Calificación: {calif_rp}/10")

    with tabs[2]:
        st.subheader("📚 Infografías de Apoyo")
        c_i1, c_i2 = st.columns(2)
        with c_i1:
            with st.expander("✅ Requisitos de Contratación"):
                st.markdown("""
                Para iniciar el trámite solo necesitamos:
                1. **INE Vigente.**
                2. **Correo Electrónico** (con acceso a SIPRE).
                3. **Teléfono** (con WhatsApp activo).
                """)
                st.info("💡 Tip: Verifica que el asesor tenga su contraseña de SIPRE a la mano.")
            with st.expander("📊 El CAT"):
                st.write("Engloba todos los costos. Es nuestra tasa real anual.")
        with c_i2:
            with st.expander("📉 Saldos Insolutos"):
                st.write("El interés baja cada mes porque se calcula sobre lo que se debe.")
            with st.expander("📅 Pago Fijo"):
                st.write("La mensualidad nunca cambia, dando seguridad al pensionado.")

    with tabs[3]:
        st.dataframe(hist[["Fecha", "Nivel", "Calificación"]])