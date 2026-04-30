import streamlit as st
import pandas as pd
import random
import datetime
import string
import streamlit.components.v1 as components

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

# --- INICIALIZACIÓN DE ESTADOS ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# --- FUNCIONES TÉCNICAS Y DE GENERACIÓN ---
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

# --- INTERFAZ DE USUARIO ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.error("⚠️ **IMPORTANTE:**")
    st.write("Escribe tu nombre empezando por **APELLIDOS**.")
    nombre_user = st.text_input("NOMBRE DEL ASESOR:").strip().upper()
    
    with st.expander("🔐 Acceso Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026") # Clave única de administración

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
    else: nivel, rango = "Básico", "Bronce"

    st.markdown(f"<div class='rango-box'><h2>{nombre_user}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay Modelo B", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    with tabs[0]:
        if st.button("Nueva Pregunta") or st.session_state.ejercicio_actual is None:
            st.session_state.ejercicio_actual = generar_ejercicio(nivel)
        st.info(st.session_state.ejercicio_actual["p"])
        resp_input = st.text_input("Tu respuesta:", key="ans_eval").strip().lower()
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
                "2. Monto": ["$", "monto", "cantidad", "crédito", "pesos"],
                "3. Plazo": ["meses", "plazo", "tiempo"],
                "4. Descuento": ["nómina", "descuento", "pensión", "directo", "automático"],
                "5. Requisitos": ["ine", "vigente", "correo", "sipre", "whatsapp"],
                "6. Forma de Pago": ["fijo", "descuento", "insolutos", "capital", "mensual", "ordinario"],
                "7. Tiempo Depósito": ["depósito", "horas", "hrs", "24", "72"],
                "8. Cierre de Venta": ["iniciar", "proceso", "procedemos", "autoriza", "trámite", "disfrute"]
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
        # --- MATERIAL DE APOYO DINÁMICO ---
        if is_admin:
            st.subheader("📖 Material de Apoyo Interactivo (Modo Admin)")
            canva_url = "https://www.canva.com/design/DAHA28GoS8E/4gQn7nxFU_eDZx6KMy5ylQ/view?embed"
            components.iframe(canva_url, height=500, scrolling=True)
            st.markdown("---")
        
        st.subheader("📚 Conceptos Clave y Ventajas Consubanco")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Interés Ordinario"):
                st.write("**Definición:** Es el costo pactado por el uso del dinero prestado.")
                st.info("💡 **Tip:** En CSB, este interés es transparente y se calcula desde el inicio.")
            with st.expander("📌 Tabla de Amortización"):
                st.write("**Definición:** Documento que desglosa capital, intereses y seguros.")
                st.success("✅ **Ventaja CSB:** El cliente conoce exactamente su saldo final desde el día 1.")
            with st.expander("📌 Saldos Insolutos"):
                st.write("**Definición:** Interés cobrado sobre el saldo pendiente actual.")
                st.info("💡 **Tip:** Esto permite liquidaciones anticipadas con ahorro real.")
        with c2:
            with st.expander("⚠️ Interés Compuesto"):
                st.error("🔒 **Seguridad CSB:** Cero riesgo de interés compuesto por Tasa Fija.")
            with st.expander("📊 CAT"):
                st.write("**Definición:** Costo total anual (tasa + seguros + comisiones).")
            with st.expander("📋 Requisitos"):
                st.markdown("- **INE Vigente**\n- **Correo con acceso a SIPRE**\n- **WhatsApp activo**")

    with tabs[3]:
        st.subheader("🕹️ Centro de Juegos")
        juego = st.radio("Selecciona una actividad:", ["Sopa de Letras", "Ahorcado", "Orden del Proceso"])
        
        if juego == "Sopa de Letras":
            palabras_s = ["CAT", "SIPRE", "INSOLUTOS", "NOMINA", "PENSIONADO", "AMORTIZACION"]
            st.write(f"🔍 **Encuentra:** {', '.join(palabras_s)}")
            if st.button("Generar Nueva Sopa") or 'sopa_grid' not in st.session_state:
                st.session_state.sopa_grid = generar_sopa_letras(palabras_s, 15)
            st.table(pd.DataFrame(st.session_state.sopa_grid))

        elif juego == "Ahorcado":
            pool = {
                "SALDOS INSOLUTOS": "Esquema donde el interés disminuye conforme se paga a capital.",
                "SIPRE": "Sistema para consultar capacidad de descuento del pensionado.",
                "CAT": "Costo Anual Total que incluye todos los costos del crédito.",
                "NOMINA": "Tipo de descuento que se aplica directo al sueldo.",
                "VIGENTE": "Estado obligatorio de la identificación oficial para el trámite."
            }
            if st.button("Nueva Palabra") or 'ahorcado_pal' not in st.session_state:
                p, pista = random.choice(list(pool.items()))
                st.session_state.ahorcado_pal = p
                st.session_state.ahorcado_pis = pista
            
            st.info(f"Pista: {st.session_state.ahorcado_pis}")
            display = "".join(["_ " if c != " " else "  " for c in st.session_state.ahorcado_pal])
            st.write(f"### {display}")
            
            ans = st.text_input("Tu respuesta:", key="ans_ahorcado").upper().strip()
            if st.button("Comprobar Ahorcado"):
                if ans.replace(" ", "") == st.session_state.ahorcado_pal.replace(" ", ""):
                    st.balloons(); st.success(f"¡Correcto! Es {st.session_state.ahorcado_pal}")
                else:
                    st.error("Sigue intentando, revisa bien los espacios y plurales.")

        elif juego == "Orden del Proceso":
            st.write("🔢 **Ordena los pasos del Modelo B:**")
            pasos = ["Cierre de Venta", "Presentación", "Monto y Plazo", "Requisitos"]
            orden = st.multiselect("Selecciona en orden:", pasos)
            if st.button("Validar Orden"):
                if orden == ["Presentación", "Monto y Plazo", "Requisitos", "Cierre de Venta"]:
                    st.success("¡Perfecto! Tienes el flujo dominado.")
                else: st.warning("El orden correcto es: Presentación -> Monto -> Requisitos -> Cierre.")

    with tabs[4]:
        st.subheader("📊 Tu Evolución")
        if not hist.empty:
            st.dataframe(hist[["Fecha", "Nivel", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.markdown("---")
            st.subheader("🔓 Admin Panel")
            if not st.session_state.db.empty:
                csv = st.session_state.db.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Descargar Base de Datos", data=csv, file_name="Data_Academia.csv")