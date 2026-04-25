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

# --- LÓGICA DE EJERCICIOS VARIADOS ---
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
            
    else: # Experto
        return {"p": "ESCENARIO: ¿Cuál es el principal beneficio de nuestro esquema de pagos para un cliente que quiere liquidar antes de tiempo?", "c": "ahorra intereses"}

st.title("🏦 Academia de Ventas Consubanco")

# --- BARRA LATERAL CON INSTRUCCIÓN CRÍTICA ---
with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **IMPORTANTE:**")
    st.write("Escribe tu nombre empezando por **APELLIDOS**.")
    st.caption("Ejemplo: PEREZ GARCIA JUAN")
    nombre_user = st.text_input("NOMBRE DEL ASESOR:").strip().upper()

if not nombre_user:
    st.warning("⬅️ Por favor, ingresa tu nombre (Apellido Paterno Apellido Materno Nombres) en el panel lateral para comenzar.")
else:
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_user]
    num_intentos = len(hist)
    
    # Lógica de niveles
    if num_intentos > 0 and hist.iloc[-1]["Calificación"] >= 10:
        ultimo_nv = hist.iloc[-1]["Nivel"]
        if ultimo_nv == "Básico": nivel, rango = "Avanzado", "Plata"
        elif ultimo_nv == "Avanzado": nivel, rango = "Experto", "Oro"
        else: nivel, rango = "Experto", "Diamante"
    else:
        nivel, rango = "Básico", "Bronce"

    st.markdown(f"""<div class='rango-box'>
        <h2>{nombre_user}</h2>
        <p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p>
    </div>""", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación Mixta", "🎙️ Roleplay Modelo B", "📊 Evolución"])

    with tabs[0]:
        st.subheader(f"Desafío Nivel {nivel}")
        if st.button("Generar Nueva Pregunta") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        
        st.info(st.session_state.ejercicio_actual["p"])
        resp_input = st.text_input("Tu respuesta:").strip().lower()
        
        if st.button("Validar"):
            if resp_input == st.session_state.ejercicio_actual["c"]:
                st.success("¡Excelente! Respuesta correcta.")
                calif = 10.0
            else:
                st.error(f"Incorrecto. La respuesta era: {st.session_state.ejercicio_actual['c']}")
                calif = 0.0
            
            log = {"Nombre": nombre_user, "Nivel": nivel, "Calificación": calif, "Intentos": num_intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            st.session_state.ejercicio_actual = None

    with tabs[1]:
        st.subheader("🎙️ Entrenamiento de Guion: Modelo B")
        guion = st.text_area("Escribe tu llamada completa aquí:", height=300)
        if st.button("Calificar Modelo B"):
            texto = guion.lower()
            pilares = {
                "1. Presentación": ["hola", "buen", "día", "tarde", "noche", "nombre", "habla", "consubanco", "servidor"],
                "2. Monto": ["$", "monto", "cantidad", "crédito", "70000", "70,000", "suma"],
                "3. Plazo": ["meses", "plazo", "60", "sesenta", "pagar en"],
                "4. Descuento": ["nómina", "descuento", "pensión", "directo", "automático", "retención"],
                "5. Requisitos": ["ine", "identificación", "talón", "comprobante", "correo", "documentos", "whatsapp", "comparta"],
                "6. Forma de Pago": ["saldos insolutos", "interés", "capital", "fijo", "descuento", "pago mensual", "cuenta", "disminuye"],
                "7. Tiempo Depósito": ["depósito", "transferencia", "horas", "hrs", "días", "hábil", "disponible", "24", "72", "cuenta"],
                "8. Cierre de Venta": ["trámite", "iniciar", "iniciemos", "comenzamos", "procedemos", "autoriza", "cerramos", "le parece bien", "disfrute", "proceso", "firma"]
            }
            puntos = 0
            analisis = []
            for pilar, keys in pilares.items():
                if any(k in texto for k in keys):
                    analisis.append(f"✅ {pilar}")
                    puntos += 1
                else:
                    analisis.append(f"❌ {pilar}")
            st.write("### Resultados")
            c1, c2 = st.columns(2)
            for i, res in enumerate(analisis):
                if i < 4: c1.write(res)
                else: c2.write(res)
            calif_rp = (puntos / 8) * 10
            if calif_rp == 10:
                st.balloons(); st.success(f"Calificación: {calif_rp}/10")
            else:
                st.warning(f"Calificación: {calif_rp}/10")

    with tabs[2]:
        st.dataframe(hist[["Fecha", "Nivel", "Calificación"]])