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
        return {"p": f"Pago mensual de ${pago:,.0f} a un plazo de {plazo} meses. ¿Monto Total?", "c": str(pago * plazo)}
    elif nivel == "Avanzado":
        cap = random.randint(20, 50) * 1000
        interes = random.randint(10, 25) * 1000
        return {"p": f"Capital de ${cap:,.0f} + Interés de ${interes:,.0f}. ¿Monto Total?", "c": str(cap + interes)}
    else:
        tasa_a = random.choice([36, 48, 60, 72])
        return {"p": f"Tasa Anual del {tasa_a}%. ¿Tasa Mensual?", "c": str(tasa_a // 12)}

st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    nombre_user = st.text_input("NOMBRE DEL ASESOR:").strip().upper()

if not nombre_user:
    st.warning("⬅️ Ingresa tu nombre en el panel lateral.")
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

    st.markdown(f"""<div class='rango-box'>
        <h2>{nombre_user}</h2>
        <p><b>Rango Actual:</b> {rango} | <b>Nivel:</b> {nivel}</p>
    </div>""", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Examen", "🎙️ Roleplay Modelo B", "📊 Evolución"])

    with tabs[0]:
        if st.button("Nuevo Ejercicio") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        st.info(st.session_state.ejercicio_actual["p"])
        resp_input = st.text_input("Resultado:")
        if st.button("Validar"):
            if resp_input == st.session_state.ejercicio_actual["c"]:
                st.success("¡Correcto!")
                calif = 10.0
            else:
                st.error(f"Incorrecto. Era {st.session_state.ejercicio_actual['c']}")
                calif = 0.0
            log = {"Nombre": nombre_user, "Nivel": nivel, "Calificación": calif, "Intentos": num_intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            st.session_state.ejercicio_actual = None

    with tabs[1]:
        st.subheader("🎙️ Entrenamiento de Guion: Modelo B")
        guion = st.text_area("Escribe tu llamada completa aquí:", height=300)
        
        if st.button("Calificar Modelo B"):
            texto = guion.lower()
            # DICCIONARIO MEJORADO Y FLEXIBLE
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
            
            st.write("### Resultados del Análisis")
            c1, c2 = st.columns(2)
            for i, res in enumerate(analisis):
                if i < 4: c1.write(res)
                else: c2.write(res)
            
            calif_rp = (puntos / 8) * 10
            if calif_rp == 10:
                st.balloons()
                st.success(f"Calificación: {calif_rp}/10 - ¡Perfecto!")
            else:
                st.warning(f"Calificación: {calif_rp}/10 - Revisa los puntos faltantes.")

    with tabs[2]:
        st.dataframe(hist[["Fecha", "Nivel", "Calificación"]])