import streamlit as st
import pandas as pd
import random
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Capacitación Consubanco", layout="wide")

# --- COLORES CONSUBANCO ---
COLOR_PRIMARIO = "#002D72" # Azul Consubanco
COLOR_SECUNDARIO = "#FF6600" # Naranja Consubanco

st.markdown(f"""
    <style>
    .main {{ background-color: #f0f2f6; }}
    .stButton>button {{ 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: {COLOR_PRIMARIO}; color: white; font-weight: bold;
    }}
    .stButton>button:hover {{ border: 2px solid {COLOR_SECUNDARIO}; color: {COLOR_SECUNDARIO}; }}
    .rango-box {{ 
        padding: 25px; border-radius: 15px; 
        border-left: 10px solid {COLOR_SECUNDARIO}; 
        background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    h1, h2, h3 {{ color: {COLOR_PRIMARIO}; }}
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# --- FUNCIONES DE LÓGICA ---
def generar_nuevo_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(10, 30) * 100
        plazo = random.choice([12, 18, 24, 36])
        st.session_state.ejercicio_actual = {
            "p": f"Un pensionado solicita un crédito con un pago mensual de ${pago:,.0f} a un plazo de {plazo} meses. ¿Cuál es el MONTO TOTAL A PAGAR?",
            "c": str(pago * plazo)
        }
    elif nivel == "Avanzado":
        cap = random.randint(20, 50) * 1000
        interes = random.randint(10, 25) * 1000
        st.session_state.ejercicio_actual = {
            "p": f"Si el Capital entregado es de ${cap:,.0f} y el Puro Interés generado es de ${interes:,.0f}, ¿Cuál es el MONTO TOTAL que el cliente pagará?",
            "c": str(cap + interes)
        }
    else:
        tasa_a = random.choice([36, 48, 60, 72])
        st.session_state.ejercicio_actual = {
            "p": f"Para un crédito con Tasa Anual del {tasa_a}%, ¿Cuál es la TASA MENSUAL que debemos informar al cliente?",
            "c": str(tasa_a // 12)
        }

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=200) # Logo genérico o link a logo real
    nombre_usuario = st.text_input("NOMBRE DEL ASESOR:").strip().upper()

if not nombre_usuario:
    st.warning("⚠️ Ingresa tu nombre en el panel lateral para activar la plataforma.")
else:
    # Determinación de Nivel y Rango
    historial = st.session_state.db[st.session_state.db["Nombre"] == nombre_usuario]
    intentos = len(historial)
    
    if intentos > 0 and historial.iloc[-1]["Calificación"] >= 10:
        if historial.iloc[-1]["Nivel"] == "Básico": nivel, rango = "Avanzado", "Plata"
        elif historial.iloc[-1]["Nivel"] == "Avanzado": nivel, rango = "Experto", "Oro"
        else: nivel, rango = "Experto", "Diamante"
    else:
        nivel, rango = "Básico", "Bronce"

    st.markdown(f"""<div class='rango-box'>
        <span style='color: {COLOR_SECUNDARIO}; font-weight: bold;'>PERFIL DE ASESOR</span>
        <h2>{nombre_usuario}</h2>
        <p><b>Rango:</b> {rango} | <b>Nivel de Evaluación:</b> {nivel}</p>
    </div>""", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación Financiera", "🎙️ Simulador de Roleplay", "📈 Mi Progreso"])

    # --- TAB 1: EXAMEN ---
    with tabs[0]:
        st.subheader("Cálculos Financieros Rápidos")
        
        if st.button("Generar Ejercicio Nuevo") or st.session_state.ejercicio_actual is None:
            generar_nuevo_ejercicio(nivel)
        
        st.info(st.session_state.ejercicio_actual["p"])
        
        resp_user = st.text_input("Escribe el resultado (solo números):", key="resp_ej")
        
        if st.button("Validar Respuesta"):
            if resp_user == st.session_state.ejercicio_actual["c"]:
                st.success("✅ ¡Correcto! Has demostrado precisión en el cálculo.")
                calif = 10.0
            else:
                st.error(f"❌ Incorrecto. El resultado correcto era: {st.session_state.ejercicio_actual['c']}")
                calif = 0.0
            
            # Guardar en Historial
            nuevo_log = {
                "Nombre": nombre_usuario, "Nivel": nivel, "Calificación": calif,
                "Intentos": intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo_log])], ignore_index=True)
            st.session_state.ejercicio_actual = None # Reset para el siguiente

    # --- TAB 2: ROLEPLAY ---
    with tabs[1]:
        st.subheader("Módulo de Cierre de Venta")
        st.write("Simulación: El cliente acepta las condiciones, procede a realizar el cierre siguiendo la estructura oficial.")
        
        respuesta_rp = st.text_area("Ingresa tu respuesta de venta:", height=250, placeholder="Ej: Hola, soy Juan de Consubanco...")
        
        if st.button("Evaluar Mi Venta"):
            # Diccionario robusto de validación
            puntos_clave = {
                "Presentación": ["hola", "buen", "tarde", "noche", "nombre", "consubanco"],
                "Monto": ["monto", "cantidad", "pesos", "$"],
                "Plazo": ["meses", "plazo", "tiempo", "periodo"],
                "Descuento": ["nómina", "descuento", "automático", "pago"],
                "Requisitos": ["ine", "identificación", "talón", "comprobante", "documentos"],
                "Forma de Pago": ["saldos insolutos", "interés", "capital", "fijo"],
                "Tiempo Depósito": ["depósito", "horas", "días", "transferencia", "disponible"],
                "Cierre de Venta": ["parece bien", "comenzamos", "procedemos", "autoriza", "firme", "trámite", "cerramos", "beneficiario"]
            }
            
            validos = 0
            resumen = []
            for punto, keywords in puntos_clave.items():
                if any(k in respuesta_rp.lower() for k in keywords):
                    resumen.append(f"✅ **{punto}**: Detectado")
                    validos += 1
                else:
                    resumen.append(f"❌ **{punto}**: No detectado")
            
            st.write("### Resultados del Análisis")
            c1, c2 = st.columns(2)
            for i, item in enumerate(resumen):
                if i < 4: c1.write(item)
                else: c2.write(item)
            
            calif_rp = (validos / 8) * 10
            if calif_rp >= 8.5:
                st.balloons()
                st.success(f"Puntaje de Roleplay: {calif_rp}/10 - ¡Excelente manejo de guion!")
            else:
                st.warning(f"Puntaje: {calif_rp}/10 - Te faltaron puntos clave. Revisa los elementos marcados con ❌.")

    # --- TAB 3: PROGRESO ---
    with tabs[2]:
        st.subheader("Tu Evolución en Consubanco")
        if not historial.empty:
            st.table(historial[["Fecha", "Nivel", "Rango", "Calificación"]])
            csv = historial.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar mi Reporte Académico", csv, f"Reporte_{nombre_usuario}.csv", "text/csv")
        else:
            st.info("Realiza tu primera evaluación para ver estadísticas.")