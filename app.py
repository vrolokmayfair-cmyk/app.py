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

# --- INICIALIZACIÓN DE VARIABLES ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

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
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=200)
    nombre_usuario = st.text_input("NOMBRE DEL ASESOR:").strip().upper()

if not nombre_usuario:
    st.warning("⚠️ Ingresa tu nombre en el panel lateral para activar la plataforma.")
else:
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
        <p><b>Rango:</b> {rango} | <b>Nivel:</b> {nivel}</p>
    </div>""", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación Financiera", "🎙️ Simulador Roleplay (Modelo B)", "📈 Mi Progreso"])

    # --- TAB 1: EXAMEN ---
    with tabs[0]:
        st.subheader("Cálculos Financieros")
        if st.button("Generar Ejercicio Nuevo") or st.session_state.ejercicio_actual is None:
            generar_nuevo_ejercicio(nivel)
        
        st.info(st.session_state.ejercicio_actual["p"])
        resp_user = st.text_input("Escribe el resultado (solo números):")
        
        if st.button("Validar Respuesta"):
            if resp_user == st.session_state.ejercicio_actual["c"]:
                st.success("✅ ¡Correcto!")
                calif = 10.0
            else:
                st.error(f"❌ Incorrecto. Era: {st.session_state.ejercicio_actual['c']}")
                calif = 0.0
            
            nuevo_log = {
                "Nombre": nombre_usuario, "Nivel": nivel, "Calificación": calif,
                "Intentos": intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo_log])], ignore_index=True)
            st.session_state.ejercicio_actual = None

    # --- TAB 2: ROLEPLAY MODELO B ---
    with tabs[1]:
        st.subheader("🎙️ Entrenamiento de Guion: Modelo B")
        st.markdown("""
        **Instrucciones:** Redacta la llamada completa siguiendo la estructura de **Modelo B**. 
        Tu guion debe incluir obligatoriamente los 8 pilares de la venta para ser aprobado.
        """)
        
        respuesta_rp = st.text_area("Escribe tu modelo de llamada aquí:", height=300, 
                                   placeholder="Ej: Buen día, le habla [Nombre] de Consubanco. El motivo de mi llamada es...")
        
        if st.button("Calificar Modelo B"):
            puntos_clave = {
                "1. Presentación": ["hola", "buen", "día", "tarde", "noche", "nombre", "consubanco", "habla"],
                "2. Monto": ["monto", "cantidad", "pesos", "$", "ofrecer", "línea"],
                "3. Plazo": ["meses", "plazo", "tiempo", "periodo", "mensualidades"],
                "4. Descuento": ["nómina", "descuento", "automático", "pago", "directo"],
                "5. Requisitos": ["ine", "identificación", "talón", "comprobante", "documentos", "requisitos"],
                "6. Forma de Pago": ["saldos insolutos", "interés", "capital", "fijo", "disminuye"],
                "7. Tiempo Depósito": ["depósito", "horas", "días", "transferencia", "disponible", "rápido"],
                "8. Cierre de Venta": ["parece bien", "comenzamos", "procedemos", "autoriza", "firme", "trámite", "cerramos", "beneficiario", "acuerdo"]
            }
            
            validos = 0
            resumen = []
            for punto, keywords in puntos_clave.items():
                if any(k in respuesta_rp.lower() for k in keywords):
                    resumen.append(f"✅ **{punto}**")
                    validos += 1
                else:
                    resumen.append(f"❌ **{punto}**")
            
            st.write("### Validación de Estructura Modelo B")
            c1, c2 = st.columns(2)
            for i, item in enumerate(resumen):
                if i < 4: c1.write(item)
                else: c2.write(item)
            
            calif_rp = (validos / 8) * 10
            if calif_rp == 10:
                st.balloons()
                st.success("¡Felicidades! Has cumplido con el Modelo B a la perfección.")
            elif calif_rp >= 7:
                st.warning(f"Calificación: {calif_rp}/10. Revisa los puntos faltantes para alcanzar la excelencia.")
            else:
                st.error(f"Calificación: {calif_rp}/10. Es necesario incluir todos los elementos de la estructura.")

    # --- TAB 3: PROGRESO ---
    with tabs[2]:
        st.subheader("Tu Evolución")
        if not historial.empty:
            st.table(historial[["Fecha", "Nivel", "Rango", "Calificación"]])
        else:
            st.info("Aún no hay datos. Realiza tu primera evaluación.")