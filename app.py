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

# --- FUNCIONES DE BASE DE DATOS ---
def cargar_datos():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])
    return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'db' not in st.session_state:
    st.session_state.db = cargar_datos()

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# --- FUNCIONES DE JUEGOS ---
def generar_sopa_letras(palabras, tamaño=15):
    grid = [[random.choice(string.ascii_uppercase) for _ in range(tamaño)] for _ in range(tamaño)]
    for palabra in palabras:
        palabra = palabra.upper().replace(" ", "")
        colocada = False
        intentos = 0
        while not colocada and intentos < 100:
            direccion = random.choice([(0,1), (1,0)])
            fila = random.randint(0, tamaño - 1 if direccion == (0,1) else tamaño - len(palabra))
            col = random.randint(0, tamaño - len(palabra) if direccion == (0,1) else tamaño - 1)
            puedo = True
            for i in range(len(palabra)):
                if grid[fila + i*direccion[0]][col + i*direccion[1]] not in (string.ascii_uppercase + palabra[i]):
                    puedo = False
            if puedo:
                for i in range(len(palabra)):
                    grid[fila + i*direccion[0]][col + i*direccion[1]] = palabra[i]
                colocada = True
            intentos += 1
    return grid

def generar_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(10, 30) * 100
        plazo = random.choice([12, 18, 24, 36, 48, 60])
        return {"p": f"PAGO TOTAL: El descuento mensual es de ${pago:,.0f} a un plazo de {plazo} meses. ¿Cuál es el Monto Total?", "c": str(pago * plazo)}
    elif nivel == "Avanzado":
        opcion = random.choice(["cat", "insolutos"])
        if opcion == "cat": return {"p": "¿Qué siglas definen el costo anual total del crédito incluyendo todos los costos?", "c": "cat"}
        else: return {"p": "¿Cómo se llama el esquema donde el interés disminuye conforme se paga a capital?", "c": "saldos insolutos"}
    else:
        return {"p": "¿Por qué en Consubanco el cliente NUNCA genera interés compuesto?", "c": "tasa fija"}

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **MODO DE INGRESO:**")
    st.write("1. APELLIDOS\n2. NOMBRE(S)")
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    
    with st.expander("🔐 Acceso Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Ingresa tu nombre (APELLIDOS PRIMERO) para comenzar.")
else:
    # Lógica Instructor (Homologada)
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    if es_instructor and 'limpieza_hecha' not in st.session_state:
        st.session_state.db = st.session_state.db[st.session_state.db["Nombre"] != MI_NOMBRE_CONTROL]
        guardar_datos(st.session_state.db)
        st.session_state.limpieza_hecha = True

    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    num_intentos = len(hist)
    
    if es_instructor: nivel, rango = "Experto", "Diamante (Admin)"
    elif num_intentos > 0 and hist.iloc[-1]["Calificación"] >= 10:
        ultimo_nv = hist.iloc[-1]["Nivel"]
        nivel = "Avanzado" if ultimo_nv == "Básico" else "Experto"
        rango = "Plata" if ultimo_nv == "Básico" else "Oro"
    else: nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_raw}</h2><p><b>Rango Actual:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    with tabs[0]:
        st.subheader("Módulo de Evaluación")
        if st.button("Nueva Pregunta") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        st.info(st.session_state.ejercicio_actual["p"])
        resp = st.text_input("Tu respuesta:", key="eval_ans").strip().lower()
        if st.button("Validar Respuesta"):
            calif = 10.0 if resp == st.session_state.ejercicio_actual["c"] else 0.0
            log = {"Nombre": nombre_raw, "Nivel": nivel, "Calificación": calif, "Intentos": num_intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            guardar_datos(st.session_state.db)
            st.session_state.ejercicio_actual = None
            st.rerun()

    with tabs[1]:
        st.subheader("🎙️ Entrenamiento Modelo B")
        guion = st.text_area("Escribe tu speech o llamada completa aquí:", height=250)
        if st.button("Calificar Estructura"):
            texto = guion.lower()
            pilares = {"Presentación": ["hola", "buen", "día", "habla", "consubanco"], "Monto y Plazo": ["$", "monto", "crédito", "meses"], "Forma de Pago": ["fijo", "nómina", "pensión"]}
            encontrados = sum(1 for p, k in pilares.items() if any(word in texto for word in k))
            st.write(f"### Desempeño: {(encontrados/3)*10}/10")

    with tabs[2]:
        if is_admin:
            st.subheader("📖 Material de Apoyo (Modo Administrador)")
            components.iframe("https://www.canva.com/design/DAHA28GoS8E/4gQn7nxFU_eDZx6KMy5ylQ/view?embed", height=500)
            st.markdown("---")
        
        st.subheader("📚 Glosario y Tips Financieros")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 CAT (Costo Anual Total)"):
                st.write("**Definición:** Indicador que integra tasa, comisiones y seguros.")
                st.info("💡 **Tip:** Úsalo para demostrar transparencia absoluta.")
            with st.expander("📌 Tasa de Interés"):
                st.write("**Definición:** Porcentaje cobrado por el capital.")
                st.success("✅ **Ventaja:** Al ser fija, el cliente tiene certidumbre total.")
            with st.expander("📋 Requisitos"):
                st.markdown("- **INE Vigente**\n- **Correo con acceso a SIPRE**\n- **WhatsApp activo**")
                st.info("💡 **Tip:** Valida estos puntos antes de iniciar el proceso.")
        with c2:
            with st.expander("📌 Saldos Insolutos"):
                st.write("Interés sobre el saldo pendiente. Beneficia la liquidación anticipada.")
            with st.expander("⚠️ Interés Compuesto"):
                st.error("🔒 En Consubanco el cliente NO paga intereses sobre intereses.")
            with st.expander("📌 SIPRE"):
                st.write("Sistema para verificar capacidad de pago del pensionado IMSS.")

    with tabs[3]:
        st.subheader("🕹️ Centro de Juegos")
        op_juego = st.radio("Selecciona una actividad:", ["Sopa de Letras", "Ahorcado", "Orden del Proceso"])
        
        if op_juego == "Sopa de Letras":
            palabras = ["CAT", "SIPRE", "NOMINA", "INSOLUTOS", "TASA"]
            if st.button("Generar Nueva Sopa") or 'sopa_grid' not in st.session_state:
                st.session_state.sopa_grid = generar_sopa_letras(palabras)
            st.table(pd.DataFrame(st.session_state.sopa_grid))

        elif op_juego == "Ahorcado":
            pool = {"SIPRE": "Sistema de consulta IMSS", "CAT": "Costo total del crédito", "TASA FIJA": "Interés que no cambia"}
            if st.button("Cambiar Palabra") or 'ah_pal' not in st.session_state:
                p, pis = random.choice(list(pool.items()))
                st.session_state.ah_pal, st.session_state.ah_pis = p, pis
            st.info(f"Pista: {st.session_state.ah_pis}")
            resp_ah = st.text_input("Palabra completa:", key="ah_input").upper().strip()
            if st.button("Verificar Ahorcado") and resp_ah == st.session_state.ah_pal: st.balloons()

        elif op_juego == "Orden del Proceso":
            orden = st.multiselect("Pasos Modelo B:", ["Monto", "Presentación", "Cierre", "Requisitos"])
            if st.button("Validar Orden") and orden == ["Presentación", "Monto", "Requisitos", "Cierre"]: st.success("¡Orden Correcto!")

    with tabs[4]:
        st.subheader("📊 Historial de Aprendizaje")
        st.dataframe(hist[["Fecha", "Nivel", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.markdown("---")
            st.write("Panel Admin: Reporte Global")
            st.dataframe(st.session_state.db)
            # BOTÓN DE EXPORTAR FIJADO
            st.download_button(
                label="📥 Exportar CSV",
                data=st.session_state.db.to_csv(index=False).encode('utf-8'),
                file_name=f"Reporte_Academia_{datetime.date.today()}.csv",
                mime='text/csv'
            )