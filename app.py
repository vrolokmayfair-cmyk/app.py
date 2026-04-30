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
    .word-list {{
        background-color: #E8F0FE; padding: 15px; border-radius: 10px;
        border: 1px solid {COLOR_AZUL}; margin-bottom: 15px;
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

# --- LÓGICA DE EVALUACIÓN CON RETROALIMENTACIÓN ---
def generar_ejercicio(nivel):
    if nivel == "Básico":
        pago = random.randint(15, 45) * 100
        plazo = random.choice([12, 24, 36, 48, 60])
        total = pago * plazo
        return {
            "p": f"CÁLCULO RÁPIDO: Si un cliente tiene un descuento mensual de ${pago:,.0f} a un plazo de {plazo} meses, ¿cuál es el Monto Total que pagará al final del crédito?",
            "c": str(total),
            "r": f"Retroalimentación: El Monto Total se obtiene multiplicando el pago mensual (${pago:,.0f}) por el número de meses ({plazo}). El resultado correcto es ${total:,.0f}."
        }
    elif nivel == "Avanzado":
        opciones = [
            {"p": "¿Qué concepto define el costo total del crédito expresado en términos porcentuales anuales?", "c": "cat", "r": "Retroalimentación: El CAT (Costo Anual Total) es el indicador clave que suma tasa, comisiones y seguros para comparar créditos."},
            {"p": "¿Cómo se llama el esquema donde los intereses se calculan sobre lo que el cliente aún debe?", "c": "saldos insolutos", "r": "Retroalimentación: Los Saldos Insolutos permiten que el interés baje conforme el cliente paga capital."},
            {"p": "¿Qué documento es vital entregar para que el cliente vea el desglose de sus pagos?", "c": "tabla de amortización", "r": "Retroalimentación: La Tabla de Amortización es el calendario detallado de pagos, intereses y seguros."}
        ]
        return random.choice(opciones)
    else: # Experto
        opciones = [
            {"p": "¿Por qué la Tasa Fija es un argumento de venta superior ante la inflación?", "c": "seguridad", "r": "Retroalimentación: La Tasa Fija garantiza que el descuento del cliente no subirá aunque la economía sea inestable, dándole seguridad."},
            {"p": "Verdadero o Falso: ¿Consubanco aplica interés compuesto en sus créditos de nómina?", "c": "falso", "r": "Retroalimentación: Es Falso. En Consubanco no hay anatocismo (cobro de intereses sobre intereses)."},
            {"p": "¿Cuál es la herramienta principal para validar la capacidad de descuento de un pensionado IMSS?", "c": "sipre", "r": "Retroalimentación: El SIPRE es el portal oficial para consultar la capacidad de descuento disponible del pensionado."}
        ]
        return random.choice(opciones)

# --- FUNCIONES DE JUEGOS ---
def generar_sopa_letras(palabras, tamaño=12):
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

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **MODO DE INGRESO:**")
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    
    with st.expander("🔐 Acceso Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Ingresa tu nombre (APELLIDOS PRIMERO) para comenzar.")
else:
    # Lógica Instructor
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    if es_instructor and 'limpieza_hecha' not in st.session_state:
        st.session_state.db = st.session_state.db[st.session_state.db["Nombre"] != MI_NOMBRE_CONTROL]
        guardar_datos(st.session_state.db)
        st.session_state.limpieza_hecha = True

    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    num_intentos = len(hist)
    
    if es_instructor: nivel, rango = "Experto", "Diamante (Admin)"
    elif num_intentos > 0 and hist.iloc[-1]["Calificación"] >= 10:
        nivel, rango = "Avanzado", "Plata"
    else: nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_raw}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    # --- TAB EVALUACIÓN CON RETROALIMENTACIÓN ---
    with tabs[0]:
        st.subheader("Módulo de Evaluación Dinámica")
        if st.button("Generar Nueva Pregunta") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        
        st.info(st.session_state.ejercicio_actual["p"])
        resp = st.text_input("Escribe tu respuesta aquí:", key="eval_ans").strip().lower()
        
        if st.button("Validar y Guardar"):
            if resp == st.session_state.ejercicio_actual["c"]:
                st.success("¡Excelente! Respuesta correcta (+10 puntos).")
                calif = 10.0
            else:
                st.error(f"Incorrecto.")
                st.warning(st.session_state.ejercicio_actual["r"]) # Mostrar retroalimentación
                calif = 0.0
            
            log = {
                "Nombre": nombre_raw, "Nivel": nivel, "Calificación": calif, 
                "Intentos": num_intentos + 1, "Rango": rango, 
                "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            guardar_datos(st.session_state.db)
            st.session_state.ejercicio_actual = None 
            st.info("💡 Haz clic en 'Generar Nueva Pregunta' para continuar.")

    # --- TAB ROLEPLAY ---
    with tabs[1]:
        st.subheader("🎙️ Entrenamiento de Speech")
        guion = st.text_area("Pega aquí tu speech de venta:", height=200)
        if st.button("Analizar"):
            texto = guion.lower()
            p = 0
            if "hola" in texto: p += 3
            if any(x in texto for x in ["monto", "pago"]): p += 4
            if "consubanco" in texto: p += 3
            st.metric("Calidad", f"{p}/10")

    # --- TAB GLOSARIO COMPLETO ---
    with tabs[2]:
        if is_admin:
            components.iframe("https://www.canva.com/design/DAHA28GoS8E/4gQn7nxFU_eDZx6KMy5ylQ/view?embed", height=500)
            st.markdown("---")
        
        st.subheader("📚 Glosario Financiero")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital"):
                st.write("**Definición:** Monto neto que el cliente recibe.")
                st.info("💡 Tip: El abono a capital reduce la deuda real mes a mes.")
            with st.expander("📌 CAT"):
                st.write("**Definición:** Costo Anual Total (tasa + seguros + comisiones).")
                st.info("💡 Tip: Ideal para comparar transparencia contra la competencia.")
            with st.expander("📌 Tasa de Interés"):
                st.write("**Definición:** El precio del dinero prestado.")
                st.success("✅ Ventaja: Nuestra tasa es fija, garantizando estabilidad.")
        with c2:
            with st.expander("📋 Requisitos"):
                st.write("- INE Vigente\n- Correo con SIPRE\n- WhatsApp")
            with st.expander("📌 Saldos Insolutos"):
                st.write("Cálculo sobre el remanente. Facilita liquidar antes y ahorrar.")
            with st.expander("⚠️ Interés Compuesto"):
                st.error("🔒 Seguridad: En Consubanco NO cobramos intereses sobre intereses.")
            with st.expander("📌 SIPRE"):
                st.write("Portal para validar la capacidad de pago del pensionado IMSS.")

    # --- TAB JUEGOS ---
    with tabs[3]:
        st.subheader("🕹️ Centro de Entrenamiento")
        op_juego = st.radio("Selecciona actividad:", ["Sopa de Letras", "Ahorcado"])
        
        if op_juego == "Sopa de Letras":
            st.markdown("### 🔍 Busca estas palabras:")
            palabras_sopa = ["CAPITAL", "CAT", "SIPRE", "INSOLUTOS", "TASA"]
            st.markdown(f"<div class='word-list'>{' | '.join(palabras_sopa)}</div>", unsafe_allow_html=True)
            if st.button("Nueva Sopa") or 'sopa_grid' not in st.session_state:
                st.session_state.sopa_grid = generar_sopa_letras(palabras_sopa)
            st.table(pd.DataFrame(st.session_state.sopa_grid))

        elif op_juego == "Ahorcado":
            pool = {"CAPITAL": "Monto neto", "CAT": "Costo total", "SIPRE": "Portal IMSS"}
            if st.button("Nueva Palabra") or 'ah_pal' not in st.session_state:
                p, pis = random.choice(list(pool.items()))
                st.session_state.ah_pal, st.session_state.ah_pis = p, pis
            st.info(f"Pista: {st.session_state.ah_pis}")
            resp_ah = st.text_input("Escribe la palabra:", key="ah_input").upper().strip()
            if st.button("Verificar"):
                if resp_ah == st.session_state.ah_pal: st.balloons()

    # --- TAB EVOLUCIÓN ---
    with tabs[4]:
        st.subheader("📊 Mi Historial")
        st.dataframe(hist[["Fecha", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.markdown("---")
            st.write("### Panel Administrativo")
            st.dataframe(st.session_state.db)
            st.download_button(
                label="📥 Exportar CSV",
                data=st.session_state.db.to_csv(index=False).encode('utf-8'),
                file_name=f"Reporte_General_{datetime.date.today()}.csv",
                mime='text/csv'
            )