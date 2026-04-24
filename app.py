import streamlit as st
import pandas as pd
import random
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Capacitación Financiera Pro", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .rango-box { padding: 20px; border-radius: 10px; border: 2px solid #007bff; text-align: center; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE BASE DE DATOS (Simulada para el ejemplo, conectar con st.connection para Sheets) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

# --- FUNCIONES DE GENERACIÓN DE EJERCICIOS ---
def generar_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(10, 30) * 100
        plazo = random.choice([12, 24, 36])
        return {"p": f"Calcula el Monto Total: Pago mensual de ${pago} a un plazo de {plazo} meses.", "c": str(pago * plazo), "t": "num"}
    
    elif nivel == "Avanzado":
        cap = random.randint(20, 50) * 1000
        total = cap * 1.45
        return {"p": f"Si el Capital es ${cap:,.0f} y el Monto Total es ${total:,.0f}, ¿cuánto es el Puro Interés?", "c": str(int(total - cap)), "t": "num"}
    
    else: # Experto
        tasa_a = random.choice([36, 48, 60])
        return {"p": f"Si la tasa anual es del {tasa_a}%, ¿cuál es la tasa mensual exacta?", "c": str(tasa_a // 12), "t": "num"}

# --- INTERFAZ DE USUARIO ---
st.title("🏆 Plataforma de Alto Rendimiento: Créditos Pensionados")

# Registro / Login
with st.sidebar:
    st.header("Acceso Asesor")
    nombre_usuario = st.text_input("Ingresa tu Nombre Completo:").strip().upper()

if not nombre_usuario:
    st.info("Por favor, ingresa tu nombre en la barra lateral para comenzar.")
else:
    # Determinar Rango y Nivel
    historial = st.session_state.db[st.session_state.db["Nombre"] == nombre_usuario]
    intentos = len(historial)
    
    if intentos > 0 and historial.iloc[-1]["Calificación"] == 10:
        if historial.iloc[-1]["Nivel"] == "Básico": nivel = "Avanzado"; rango = "Plata"
        elif historial.iloc[-1]["Nivel"] == "Avanzado": nivel = "Experto"; rango = "Oro"
        else: nivel = "Experto"; rango = "Diamante"
    else:
        nivel = "Básico"; rango = "Bronce"

    st.markdown(f"""<div class='rango-box'><h4>Asesor: {nombre_usuario}</h4><h2>Rango: {rango}</h2><p>Nivel actual: {nivel}</p></div>""", unsafe_allow_html=True)

    tabs = st.tabs(["📊 Mi Evolución", "🧮 Examen Financiero", "🗣️ Simulador Roleplay"])

    # TAB 1: EVOLUCIÓN
    with tabs[0]:
        st.subheader("Historial de Desempeño")
        if intentos > 0:
            st.dataframe(historial)
        else:
            st.write("Aún no tienes registros. ¡Comienza tu primera evaluación!")

    # TAB 2: EXAMEN
    with tabs[1]:
        st.subheader(f"Evaluación Dinámica - Nivel {nivel}")
        ejercicio = generar_ejercicio(nivel)
        st.write(ejercicio["p"])
        resp_user = st.text_input("Tu respuesta:")
        
        if st.button("Enviar Evaluación"):
            if resp_user == ejercicio["c"]:
                calif = 10.0
                st.success("¡Excelente! Cálculo exacto.")
            else:
                calif = 0.0
                st.error(f"Incorrecto. La respuesta era {ejercicio['c']}")
            
            # Guardar resultado
            nuevo_log = {
                "Nombre": nombre_usuario, "Nivel": nivel, "Calificación": calif,
                "Intentos": intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo_log])], ignore_index=True)

    # TAB 3: ROLEPLAY (El corazón de la venta)
    with tabs[2]:
        st.subheader("Simulador de Llamada de Venta")
        st.write("Escenario: Un pensionado te pregunta por qué debería confiar en este crédito.")
        
        st.info("Asegúrate de cubrir los 8 puntos: Presentación, Monto, Plazo, Descuento, Requisitos, Pago, Depósito y Cierre.")
        
        respuesta_rp = st.text_area("Escribe tu guion de respuesta aquí:", height=200)
        
        if st.button("Calificar Roleplay"):
            # Lógica de validación de palabras clave
            puntos_clave = {
                "Presentación": ["hola", "buen día", "nombre es", "asesor"],
                "Monto": ["monto", "cantidad", "$", "pesos"],
                "Plazo": ["meses", "plazo", "tiempo"],
                "Descuento": ["nómina", "descuento", "automático"],
                "Requisitos": ["identificación", "ine", "comprobante", "talón"],
                "Pago": ["saldos insolutos", "interés", "capital"],
                "Depósito": ["depósito", "transferencia", "horas", "días"],
                "Cierre": ["le parece bien", "comenzamos", "procedemos", "firma"]
            }
            
            check_list = []
            for punto, palabras in puntos_clave.items():
                if any(word in respuesta_rp.lower() for word in palabras):
                    check_list.append(f"✅ {punto}")
                else:
                    check_list.append(f"❌ {punto}")
            
            st.write("### Análisis de tu estructura:")
            col1, col2 = st.columns(2)
            for i, check in enumerate(check_list):
                if i < 4: col1.write(check)
                else: col2.write(check)
            
            nota_rp = (len([c for c in check_list if "✅" in c]) / 8) * 10
            st.metric("Calificación Roleplay", f"{nota_rp}/10")
            
            if nota_rp == 10:
                st.balloons()
                st.success("¡Dominas la estructura de venta!")