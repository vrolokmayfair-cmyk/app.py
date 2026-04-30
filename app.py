import streamlit as st
import pandas as pd
import random
import datetime
import string

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Academia Consubanco", layout="wide", page_icon="🏦")

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
    h1, h2, h3 {{ color: {COLOR_AZUL}; font-family: 'Arial'; }}
    .game-card {{
        background-color: white; padding: 20px; border-radius: 10px;
        border: 1px solid #ddd; margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADOS ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# --- FUNCIONES DE APOYO ---
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
        elif opcion == "cat": return {"p": "¿Qué siglas definen el costo total del crédito incluyendo seguros y comisiones?", "c": "cat"}
        elif opcion == "insolutos": return {"p": "¿Cómo se llama el esquema donde el interés disminuye conforme se paga a capital?", "c": "saldos insolutos"}
        else: return {"p": "¿Cómo se llama el documento que desglosa pago a pago el capital, interés y saldo pendiente?", "c": "tabla de amortizacion"}
    else:
        return {"p": "¿Por qué en Consubanco el cliente NUNCA genera interés compuesto?", "c": "tasa fija y descuento via pension"}

def generar_sopa_letras(palabras, tamaño=15):
    grid = [[random.choice(string.ascii_uppercase) for _ in range(tamaño)] for _ in range(tamaño)]
    for palabra in palabras:
        palabra = palabra.upper()
        colocada = False
        while not colocada:
            direccion = random.choice([(0,1), (1,0)]) # Horizontal o Vertical
            fila = random.randint(0, tamaño - 1 if direccion == (0,1) else tamaño - len(palabra))
            col = random.randint(0, tamaño - len(palabra) if direccion == (0,1) else tamaño - 1)
            
            puedo = True
            for i in range(len(palabra)):
                if grid[fila + i*direccion[0]][col + i*direccion[1]] not in (string.ascii_uppercase + palabra[i]):
                    if grid[fila + i*direccion[0]][col + i*direccion[1]] != palabra[i]:
                        puedo = True # Simplificado para demo
            
            if puedo:
                for i in range(len(palabra)):
                    grid[fila + i*direccion[0]][col + i*direccion[1]] = palabra[i]
                colocada = True
    return grid

# --- INTERFAZ PRINCIPAL ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **IMPORTANTE:**")
    st.write("Escribe tu nombre empezando por **APELLIDOS**.")
    nombre_user = st.text_input("NOMBRE DEL ASESOR:").strip().upper()
    
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
    else: nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_user}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario", "🕹️ Centro de Juegos", "📊 Evolución"])

    # TABS 0, 1 y 2 se mantienen igual al código base anterior...
    # (Evaluación, Roleplay y Glosario con Tips incluidos)
    
    with tabs[0]:
        if st.button("Nueva Pregunta") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        st.info(st.session_state.ejercicio_actual["p"])
        resp_input = st.text_input("Tu respuesta:").strip().lower()
        if st.button("Validar"):
            if resp_input == st.session_state.ejercicio_actual["c"]: st.success("¡Excelente!"); calif = 10.0
            else: st.error(f"La respuesta era: {st.session_state.ejercicio_actual['c']}"); calif = 0.0
            log = {"Nombre": nombre_user, "Nivel": nivel, "Calificación": calif, "Intentos": num_intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            st.session_state.ejercicio_actual = None

    with tabs[1]:
        st.subheader("🎙️ Entrenamiento Modelo B")
        guion = st.text_area("Escribe tu llamada aquí:", height=200)
        if st.button("Calificar Roleplay"):
            # Lógica de pilares (Presentación, Monto, etc.)
            st.success("Análisis completado (Simulado para esta versión)")

    with tabs[2]:
        st.subheader("📚 Conceptos y Tips")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Interés Ordinario"):
                st.write("Costo por el uso del dinero.")
                st.info("💡 Tip: En CSB es transparente desde el inicio.")
        with c2:
            with st.expander("⚠️ Interés Compuesto"):
                st.error("🔒 Seguridad CSB: Cero riesgo por Tasa Fija.")

    # --- NUEVA PESTAÑA: CENTRO DE JUEGOS ---
    with tabs[3]:
        st.subheader("🕹️ Zona de Gamificación para Formación")
        
        juego = st.radio("Selecciona una actividad:", ["Sopa de Letras (15x15)", "Ahorcado Técnico", "Orden del Proceso"])
        
        if juego == "Sopa de Letras (15x15)":
            st.write("🔍 **Encuentra las palabras:** CAT, SIPRE, INSOLUTOS, NOMINA, PENSIONADO")
            if st.button("Generar Nueva Sopa"):
                st.session_state.sopa = generar_sopa_letras(["CAT", "SIPRE", "INSOLUTOS", "NOMINA", "PENSIONADO"])
            
            if 'sopa' in st.session_state:
                # Mostrar sopa en formato tabla
                df_sopa = pd.DataFrame(st.session_state.sopa)
                st.table(df_sopa)
                st.caption("Tip: Las palabras pueden estar horizontales o verticales.")

        elif juego == "Ahorcado Técnico":
            palabra_reto = "AMORTIZACION"
            st.write("🧩 **Adivina la palabra:**")
            st.write("_ " * len(palabra_reto))
            st.info("Pista: Documento que desglosa pago a pago el capital e interés.")
            intento = st.text_input("Escribe una letra o la palabra completa:").upper()
            if st.button("Adivinar"):
                if intento == palabra_reto: st.balloons(); st.success("¡Correcto!")
                else: st.error("Sigue intentando...")

        elif juego == "Orden del Proceso":
            st.write("🔢 **Ordena los pasos del Modelo B de Venta:**")
            pasos = ["Cierre de Venta", "Presentación", "Monto y Plazo", "Requisitos"]
            orden = st.multiselect("Selecciona en el orden correcto:", pasos)
            if st.button("Verificar Orden"):
                if orden == ["Presentación", "Monto y Plazo", "Requisitos", "Cierre de Venta"]:
                    st.success("¡Orden Perfecto! Estás listo para piso de ventas.")
                else:
                    st.warning("Revisa el manual, el orden es vital para la confianza del cliente.")

    with tabs[4]:
        st.subheader("📊 Historial y Control")
        if not hist.empty: st.dataframe(hist[["Fecha", "Nivel", "Calificación"]], use_container_width=True)
        if is_admin:
            st.markdown("---")
            if not st.session_state.db.empty:
                csv = st.session_state.db.to_csv(index=False).encode('utf-8')
                st.download_button("📥 REPORTE ADMIN", data=csv, file_name="Reporte_Academia.csv", key="dl_admin")