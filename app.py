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
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: white; border-radius: 5px 5px 0 0; padding: 10px 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# --- LÓGICA FINANCIERA ---
def generar_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(10, 30) * 100
        plazo = random.choice([12, 18, 24, 36])
        return {"p": f"CÁLCULO BÁSICO: Pago mensual de ${pago:,.0f} a un plazo de {plazo} meses. ¿Cuál es el MONTO TOTAL A PAGAR?", "c": str(pago * plazo)}
    elif nivel == "Avanzado":
        cap = random.randint(20, 50) * 1000
        interes = random.randint(10, 25) * 1000
        return {"p": f"ANÁLISIS AVANZADO: Capital de ${cap:,.0f} + Intereses de ${interes:,.0f}. ¿Cuál es el MONTO TOTAL final?", "c": str(cap + interes)}
    else:
        tasa_a = random.choice([36, 48, 60, 72])
        return {"p": f"NIVEL EXPERTO: Si la Tasa Anual es del {tasa_a}%, ¿cuál es la TASA MENSUAL que el cliente paga?", "c": str(tasa_a // 12)}

# --- INTERFAZ PRINCIPAL ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    nombre_user = st.text_input("NOMBRE DEL ASESOR:").strip().upper()

if not nombre_user:
    st.warning("⬅️ Ingresa tu nombre en el panel lateral para comenzar la sesión.")
else:
    # Lógica de Progresión
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
        <p style='color: {COLOR_NARANJA}; margin: 0; font-size: 0.9em; font-weight: bold;'>SESIÓN ACTIVA</p>
        <h2 style='margin: 0;'>{nombre_user}</h2>
        <p style='margin: 0;'><b>Rango Actual:</b> {rango} | <b>Módulo de Evaluación:</b> {nivel}</p>
    </div>""", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Examen Financiero", "🎙️ Roleplay Modelo B", "📊 Mi Evolución"])

    # --- TAB 1: EXAMEN ---
    with tabs[0]:
        st.subheader("Simulador de Cálculos")
        if st.button("Generar Nuevo Desafío") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        
        st.info(st.session_state.ejercicio_actual["p"])
        resp_input = st.text_input("Ingresa solo el número:", key="input_mate")
        
        if st.button("Validar Resultado"):
            if resp_input == st.session_state.ejercicio_actual["c"]:
                st.success("✅ ¡Correcto! Tu precisión es excelente.")
                calif = 10.0
            else:
                st.error(f"❌ Error. El resultado correcto era {st.session_state.ejercicio_actual['c']}")
                calif = 0.0
            
            # Registrar
            log = {"Nombre": nombre_user, "Nivel": nivel, "Calificación": calif, 
                   "Intentos": num_intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            st.session_state.ejercicio_actual = None

    # --- TAB 2: ROLEPLAY (DICCIONARIO FLEXIBLE) ---
    with tabs[1]:
        st.subheader("🎙️ Entrenamiento de Guion: Modelo B")
        st.write("Instrucciones: Redacta la llamada completa desde el saludo hasta el cierre. El sistema evaluará los 8 pilares obligatorios.")
        
        guion = st.text_area("Escribe tu modelo de llamada aquí:", height=300, 
                            placeholder="Ej: Buen día, mi nombre es...")
        
        if st.button("Calificar Modelo B"):
            texto = guion.lower()
            pilares = {
                "1. Presentación": ["hola", "buen", "día", "tarde", "noche", "nombre", "habla", "consubanco", "servidor"],
                "2. Monto": ["$", "monto", "cantidad", "crédito", "suma", "70000", "70,000", "setenta"],
                "3. Plazo": ["meses", "plazo", "pagar en", "periodo", "60", "sesenta"],
                "4. Descuento": ["nómina", "descuento", "pensión", "directo", "automático", "retención"],
                "5. Requisitos": ["ine", "identificación", "talón", "comprobante", "correo", "documentos", "fotos", "whatsapp"],
                "6. Forma de Pago": ["saldos insolutos", "interés", "capital", "fijo", "disminuye", "pago mensual"],
                "7. Tiempo Depósito": ["depósito", "transferencia", "horas", "hrs", "días", "hábil", "disponible", "24", "48", "72"],
                "8. Cierre de Venta": ["trámite", "iniciar", "comenzamos", "procedemos", "autoriza", "cerramos", "le parece bien", "acuerdo", "firma", "inmediato"]
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
                st.success("¡10/10! Dominas la estructura del Modelo B.")
            else:
                st.warning(f"Calificación: {calif_rp}/10. Asegúrate de incluir los puntos marcados con ❌.")

    # --- TAB 3: PROGRESO ---
    with tabs[2]:
        st.subheader("Historial de Avance")
        if not hist.empty:
            st.dataframe(hist[["Fecha", "Nivel", "Rango", "Calificación"]], use_container_width=True)
            csv = hist.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Reporte Personal", csv, f"Reporte_{nombre_user}.csv", "text/csv")
        else:
            st.info("No hay evaluaciones registradas para este nombre.")