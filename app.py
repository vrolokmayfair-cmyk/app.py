import datetime
import io
import os
import random
import pandas as pd
import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Academia Consubanco", layout="wide", page_icon="🏦"
)

# --- VARIABLES DE CONTROL Y PERSISTENCIA ---
DB_FILE = "database_asesores.csv"
MI_NOMBRE_CONTROL = "SUMANO GARCIA JUAN CARLOS"

# --- COLORES INSTITUCIONALES ---
COLOR_AZUL = "#002D72"
COLOR_NARANJA = "#FF6600"
COLOR_FONDO = "#F4F7F9"

st.markdown(
    f"""
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
    .instrucciones-box {{
        background-color: #E8F0FE; padding: 15px; border-radius: 10px;
        border: 1px solid {COLOR_AZUL}; margin-bottom: 20px;
    }}
    h1, h2, h3 {{ color: {COLOR_AZUL}; font-family: 'Arial'; }}
    .cvb-header {{
        padding: 10px; color: white; font-weight: bold; text-align: center; border-radius: 5px; margin-bottom: 10px;
    }}
    .script-box {{
        background-color: #FFFFFF; padding: 15px; border-radius: 10px;
        border-left: 5px solid {COLOR_AZUL}; margin-bottom: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# --- FUNCIONES AUXILIARES Y DATOS ---
def limpiar_cifra_numerica(texto: str) -> str:
    """Limpia la entrada del usuario eliminando comas, puntos, signos $ y espacios."""
    if not texto:
        return ""
    return (
        texto.replace(",", "")
        .replace(".", "")
        .replace("$", "")
        .replace(" ", "")
        .strip()
    )


def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except Exception:
            return pd.DataFrame(
                columns=[
                    "Nombre",
                    "Nivel",
                    "Calificación",
                    "Intentos",
                    "Rango",
                    "Fecha",
                ]
            )
    return pd.DataFrame(
        columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"]
    )


def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)


if "db" not in st.session_state:
    st.session_state.db = cargar_datos()

if "ejercicio_teoria" not in st.session_state:
    st.session_state.ejercicio_teoria = None

if "ejercicio_practico" not in st.session_state:
    st.session_state.ejercicio_practico = None


# --- BANCO TEÓRICO EXPANDIDO ---
def generar_teoria():
    conceptos = [
        {
            "t": "Saldos Insolutos",
            "preguntas": [
                "¿Cómo se llama el esquema donde el interés se calcula únicamente sobre el capital pendiente?",
                "¿Qué nombre recibe el sistema de cobro donde tu deuda real disminuye conforme realizas abonos?",
                "¿Bajo qué esquema de cobro de intereses se beneficia directamente al cliente que realiza pagos anticipados?",
            ],
            "c": ["insoluto", "saldos insolutos", "saldo insoluto"],
            "r": "Retroalimentación: Los saldos insolutos calculan el interés solo sobre lo que resta por pagar, premiando la liquidación anticipada.",
        },
        {
            "t": "CAT",
            "preguntas": [
                "¿Qué siglas definen el Costo Anual Total que agrupa tasa, comisiones y seguros?",
                "¿Cuál es el indicador oficial de transparencia financiera que permite comparar créditos?",
                "¿Qué métrica obligatoria incluye todos los costos reales de un financiamiento?",
            ],
            "c": ["cat"],
            "r": "Retroalimentación: El CAT integra de forma transparente todos los costos asociados al crédito en un solo porcentaje anual.",
        },
        {
            "t": "SIPRE",
            "preguntas": [
                "¿Cómo se llama el portal oficial para validar la capacidad de descuento de un pensionado IMSS?",
                "¿Qué sistema utilizamos para consultar la disponibilidad exacta de descuento de un cliente IMSS?",
                "¿Cuál es la herramienta digital indispensable para validar la capacidad de pago institucional?",
            ],
            "c": ["sipre"],
            "r": "Retroalimentación: El SIPRE es el portal institucional oficial para validar y asegurar la capacidad de descuento del pensionado.",
        },
        {
            "t": "Tasa Fija",
            "preguntas": [
                "¿Cómo se le llama al tipo de interés que protege al cliente asegurando que su pago no subirá jamás?",
                "¿Qué característica de nuestra tasa garantiza estabilidad económica ante la inflación?",
                "¿Qué clase de tasa ofrece total certidumbre al presupuesto mensual del pensionado?",
            ],
            "c": ["tasa fija", "fija"],
            "r": "Retroalimentación: La tasa fija blinda al cliente frente a la inflación, garantizando que su descuento permanezca intacto.",
        },
        {
            "t": "INE",
            "preguntas": [
                "¿Qué documento oficial de identificación con fotografía es obligatorio y requisito #1?",
                "¿Sin qué credencial oficial vigente no podemos iniciar ningún trámite de crédito?",
                "¿Cuál es el documento de identidad principal que debemos solicitar desde el primer contacto?",
            ],
            "c": ["ine", "identificacion", "credencial"],
            "r": "Retroalimentación: El INE vigente es el documento básico e indispensable para validar la identidad y dar inicio al proceso.",
        },
        {
            "t": "Capital",
            "preguntas": [
                "¿Cómo se le denomina al monto neto o dinero real que se le entrega al cliente?",
                "¿Qué término define el recurso financiero base que el cliente recibe en su cuenta?",
                "¿Cómo se le llama a la suma directa prestada antes de aplicar accesorios o plazos?",
            ],
            "c": ["capital"],
            "r": "Retroalimentación: El capital representa el monto neto del préstamo que el cliente recibe directamente para su disposición.",
        },
        {
            "t": "Interés Compuesto",
            "preguntas": [
                "Por política de Consubanco, ¿cobramos intereses sobre intereses? (Sí/No)",
                "¿Aplicamos el esquema de anatocismo o interés compuesto en nuestros créditos de nómina? (Sí/No)",
                "¿Está permitido cobrar cargos financieros sobre intereses atrasados en Consubanco? (Sí/No)",
            ],
            "c": ["no", "falso"],
            "r": "Retroalimentación: Correcto. En Consubanco protegemos el patrimonio del cliente prohibiendo el anatocismo o interés compuesto.",
        },
        {
            "t": "Tabla de Amortización",
            "preguntas": [
                "¿Cómo se llama el documento detallado que muestra el calendario y desglose de cada pago?",
                "¿Qué formato desglosa periodo a periodo el capital, intereses y seguros de un crédito?",
                "¿Qué tabla descriptiva le otorga total transparencia al cliente sobre su plan de pagos?",
            ],
            "c": ["tabla de amortización", "tabla de amortizacion", "tabla"],
            "r": "Retroalimentación: La tabla de amortización detalla de forma transparente la evolución de cada mensualidad y el saldo remanente.",
        },
        {
            "t": "WhatsApp",
            "preguntas": [
                "¿Qué medio de comunicación digital utilizamos de forma principal para agilizar el envío de documentos?",
                "¿A través de qué canal oficial de mensajería instantánea recibimos los expedientes de forma segura?",
                "¿Qué vía digital resulta clave para mantener un seguimiento ágil y constante con el cliente?",
            ],
            "c": ["whatsapp"],
            "r": "Retroalimentación: El WhatsApp es el canal oficial ágil y seguro para la recepción de expedientes y la comunicación directa.",
        },
    ]

    item = random.choice(conceptos)
    pregunta_texto = random.choice(item["preguntas"])
    return {"p": pregunta_texto, "c": item["c"], "r": item["r"]}


# --- LABORATORIO DE CÁLCULOS Y OBJECIONES ---
def generar_practico():
    nombres_clientes = [
        "Martínez", "Rodríguez", "Hernández", "García", "López",
        "González", "Pérez", "Ramírez", "Flores", "Sánchez"
    ]
    apodo = random.choice(nombres_clientes)

    monto_base = random.randint(10, 80) * 1000
    plazo = random.choice([12, 24, 36, 48, 60, 72, 84])
    pago_cotizado = round((monto_base * random.uniform(1.25, 1.45)) / plazo, -1)
    monto_total = int(pago_cotizado * plazo)

    banco_practicos = [
        {
            "tipo": "input",
            "p": (
                f"🧮 CÁLCULO DE MONTO TOTAL: Tras realizar la cotización en el sistema, le informas al Señor/Señora {apodo} "
                f"que su descuento mensual autorizado es de ${pago_cotizado:,.0f} a un plazo de {plazo} meses. "
                "El cliente te pregunta directamente: '¿Cuánto voy a pagar en total al finalizar el crédito?'. "
                "Realiza la operación matemática correspondiente:"
            ),
            "c": str(monto_total),
            "r": (
                f"Retroalimentación: El cálculo correcto se obtiene multiplicando el pago mensual (${pago_cotizado:,.0f}) "
                f"por el número de meses del plazo ({plazo}), arrojando un Monto Total de ${monto_total:,.0f}."
            ),
        },
        {
            "tipo": "radio",
            "p": (
                f"📈 MANEJO DE TASAS: Al ofrecerle una opción de crédito al Señor/Señora {apodo}, este te comenta que otra institución "
                "le ofrece una tasa supuestamente más baja pero de tipo 'Variable'. ¿Cuál es el argumento comercial técnico ideal "
                "para defender la Tasa Fija de Consubanco?"
            ),
            "options": [
                "Mencionar que las tasas variables son ilegales en créditos de nómina y que nosotros somos los únicos regulados.",
                (
                    f"Explicar el blindaje financiero: 'Comprendo su punto, Señor/Señora {apodo}. Sin embargo, una tasa variable "
                    "significa que sus descuentos mensuales podrían dispararse si las condiciones macroeconómicas cambian. "
                    "Con la Tasa Fija de Consubanco usted tiene la absoluta certeza de que su pago no subirá ni un solo peso, "
                    "protegiendo su economía familiar hasta el último día.'"
                ),
                "Decirle que nuestra tasa fija es más alta al principio pero que con los abonos voluntarios se compensa sola.",
            ],
            "c": (
                f"Explicar el blindaje financiero: 'Comprendo su punto, Señor/Señora {apodo}. Sin embargo, una tasa variable "
                "significa que sus descuentos mensuales podrían dispararse si las condiciones macroeconómicas cambian. "
                "Con la Tasa Fija de Consubanco usted tiene la absoluta certeza de que su pago no subirá ni un solo peso, "
                "protegiendo su economía familiar hasta el último día.'"
            ),
            "r": "Retroalimentación: ¡Excelente! La tasa fija se posiciona con éxito como un escudo protector frente a la inestabilidad de las tasas variables.",
        },
        {
            "tipo": "radio",
            "p": (
                f"🛡️ MANEJO DE OBJECIONES (CAT): Estás dialogando con el Señor/Señora {apodo} y este te interrumpe manifestando "
                "desconfianza: 'No me interesa, las financieras siempre esconden comisiones, seguros obligatorios y cobros ocultos'. "
                "¿Cómo respondes aplicando normatividad y términos financieros?"
            ),
            "options": [
                "Asegurarle que si encuentra algo oculto puede cancelar sin costo en los primeros cinco días.",
                (
                    f"Aplicar empatía y transparencia con el CAT: 'Comprendo perfectamente su preocupación, Señor/Señora {apodo}. "
                    "Precisamente por seguridad, en Consubanco somos una institución regulada y le garantizamos transparencia absoluta "
                    "a través de nuestro CAT (Costo Anual Total); este indicador legal ya integra la tasa, comisiones y seguros "
                    "desde el primer momento, garantizándole cero sorpresas.'"
                ),
                "Decirle que ignore los seguros ya que esos son trámites internos que no afectan su dinero en efectivo.",
            ],
            "c": (
                f"Aplicar empatía y transparencia con el CAT: 'Comprendo perfectamente su preocupación, Señor/Señora {apodo}. "
                "Precisamente por seguridad, en Consubanco somos una institución regulada y le garantizamos transparencia absoluta "
                "a través de nuestro CAT (Costo Anual Total); este indicador legal ya integra la tasa, comisiones y seguros "
                "desde el primer momento, garantizándole cero sorpresas.'"
            ),
            "r": "Retroalimentación: ¡Correcto! Utilizar el CAT como herramienta de transparencia desarma por completo la objeción de cargos ocultos.",
        },
        {
            "tipo": "radio",
            "p": (
                f"🛡️ MANEJO DE OBJECIONES (INTERÉS COMPUESTO): El Señor/Señora {apodo} te expresa un temor muy común: "
                "'He sabido de casos donde la gente se atrasa y les aplican intereses sobre intereses, volviendo la deuda impagable'. "
                "¿Cómo neutralizas esta objeción?"
            ),
            "options": [
                (
                    f"Garantizar la política estricta de no anatocismo: 'Entiendo su inquietud, Señor/Señora {apodo}. "
                    "En Consubanco su patrimonio está totalmente protegido: por norma y contrato institucional NO aplicamos "
                    "interés compuesto ni anatocismo. Sus intereses ordinarios jamás generarán cargos adicionales sobre intereses moratorios.'"
                ),
                "Explicarle que como el descuento es directo vía nómina es imposible que se atrase y sufra ese problema.",
                "Comentarle que si liquida antes de tiempo todos esos intereses compuestos se eliminan automáticamente.",
            ],
            "c": (
                f"Garantizar la política estricta de no anatocismo: 'Entiendo su inquietud, Señor/Señora {apodo}. "
                "En Consubanco su patrimonio está totalmente protegido: por norma y contrato institucional NO aplicamos "
                "interés compuesto ni anatocismo. Sus intereses ordinarios jamás generarán cargos adicionales sobre intereses moratorios.'"
            ),
            "r": "Retroalimentación: ¡Excelente respuesta! Aclarar de forma tajante la ausencia de interés compuesto transmite absoluta seguridad y confianza.",
        },
        {
            "tipo": "radio",
            "p": (
                f"🛡️ MANEJO DE OBJECIONES (LIQUIDACIÓN ANTICIPADA): Durante la llamada, el Señor/Señora {apodo} te dice: "
                f"'Me agrada el efectivo, pero me aterra amarrarme a un plazo de {plazo} meses por si tengo liquidez y quiero liquidar antes'. "
                "¿Qué esquema técnico le explicas para tranquilizarlo?"
            ),
            "options": [
                (
                    f"Explicar las bondades de los Saldos Insolutos: 'Es una excelente postura, Señor/Señora {apodo}. "
                    "Con nosotros tiene total libertad de realizar abonos voluntarios o liquidar el crédito de manera anticipada "
                    "sin penalización alguna. Al operar bajo el esquema de saldos insolutos, los intereses se calculan exclusivamente "
                    "sobre el capital que aún debe, logrando un ahorro masivo si decide terminar antes.'"
                ),
                "Mencionar que el plazo es un requisito obligatorio del banco pero que puede pedir una prórroga de pagos cada año.",
                "Decirle que no se preocupe por el plazo largo ya que los intereses ya vienen calculados en una sola exhibición.",
            ],
            "c": (
                f"Explicar las bondades de los Saldos Insolutos: 'Es una excelente postura, Señor/Señora {apodo}. "
                "Con nosotros tiene total libertad de realizar abonos voluntarios o liquidar el crédito de manera anticipada "
                "sin penalización alguna. Al operar bajo el esquema de saldos insolutos, los intereses se calculan exclusivamente "
                "sobre el capital que aún debe, logrando un ahorro masivo si decide terminar antes.'"
            ),
            "r": "Retroalimentación: ¡Perfecto! Dominar los Saldos Insolutos y asociarlos a la liquidación sin penalización es la clave maestra para cerrar clientes precavidos.",
        },
    ]

    return random.choice(banco_practicos)


# --- INTERFAZ STREAMLIT ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.markdown(
        """
    <div class='instrucciones-box'>
    <b>📋 INSTRUCCIONES DE ACCESO:</b><br><br>
    1. <b>Registro:</b> Ingresa nombre por APELLIDOS.<br>
    2. <b>Navegación:</b> Usa las pestañas superiores.<br>
    3. <b>Evaluación:</b> Elige módulo y valida respuesta.
    </div>
    """,
        unsafe_allow_html=True,
    )
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    with st.expander("🔐 Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = admin_pass == "CSB2026"

if not nombre_raw:
    st.warning("⬅️ Ingresa tu nombre para comenzar.")
else:
    es_instructor = nombre_raw == MI_NOMBRE_CONTROL
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    nivel = "Experto" if es_instructor else "Básico"
    rango = "Diamante" if es_instructor else "Bronce"

    st.markdown(
        f"<div class='rango-box'><h2>Bienvenido, {nombre_raw}</h2><p><b>Rango:</b>"
        f" {rango} | <b>Módulo:</b> {nivel}</p></div>",
        unsafe_allow_html=True,
    )

    tabs = st.tabs([
        "📝 Evaluación",
        "🧮 Cotizador y Calculadora IMSS",
        "🗣️ Scripts de Roleplay",
        "📚 Glosario e Infografías",
        "📊 Evolución",
    ])

    with tabs[0]:
        st.subheader("Evaluación Dinámica de Conocimientos")
        mod_sel = st.radio(
            "Módulo de aprendizaje:",
            ["Teoría y Conceptos", "Laboratorio de Cálculos"],
            horizontal=True,
        )

        if mod_sel == "Teoría y Conceptos":
            if (
                st.button("Generar Nueva Pregunta Teórica")
                or st.session_state.ejercicio_teoria is None
            ):
                st.session_state.ejercicio_teoria = generar_teoria()
            ej = st.session_state.ejercicio_teoria

            st.info(ej["p"])
            resp_raw = (
                st.text_input("Escribe tu respuesta aquí:", key="ans_teoria")
                .strip()
                .lower()
            )
            resp = resp_raw

        else:
            if (
                st.button("Generar Nuevo Caso Práctico (Cálculo / Objeción)")
                or st.session_state.ejercicio_practico is None
            ):
                st.session_state.ejercicio_practico = generar_practico()
            ej = st.session_state.ejercicio_practico

            st.info(ej["p"])
            if ej["tipo"] == "input":
                resp_raw = st.text_input(
                    "Escribe tu respuesta numérica aquí (puedes usar comas como 92,400"
                    " o escribirlo directo 92400):",
                    key="ans_practico_in",
                )
                resp = limpiar_cifra_numerica(resp_raw)
            else:
                resp = st.radio(
                    "Selecciona la mejor opción de Speech Profesional para el manejo de"
                    " la llamada:",
                    ej["options"],
                    key="ans_practico_rad",
                )

        if st.button("Validar Respuesta"):
            correctas = ej["c"]
            es_valida = (
                resp in correctas if isinstance(correctas, list) else resp == correctas
            )

            if es_valida:
                st.success("¡Excelente! Respuesta correcta.")
                calif = 10.0
            else:
                st.error("Respuesta incorrecta.")
                st.warning(ej["r"])
                calif = 0.0

            log = {
                "Nombre": nombre_raw,
                "Nivel": nivel,
                "Calificación": calif,
                "Intentos": len(hist) + 1,
                "Rango": rango,
                "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
            st.session_state.db = pd.concat(
                [st.session_state.db, pd.DataFrame([log])], ignore_index=True
            )
            guardar_datos(st.session_state.db)

    # --- TAB 1: COTIZADOR Y CALCULADORA IMSS (CON VALORES DIRECTOS DEL ARCHIVO) ---
    with tabs[1]:
        st.subheader("🧮 Cotizador Interactivo de Crédito - OPC IMSS Pensionados (Material 4918)")
        
        c_param1, c_param2, c_param3 = st.columns(3)
        with c_param1:
            st.info("**Convenio:** OPC IMSS PENSIONADOS\n\n**Código Material:** 4918 / SIDN")
        with c_param2:
            st.info("**Tasa Nominal Anual:** 31.89%\n\n**CAT Promedio:** 37.0% (sin IVA)")
        with c_param3:
            st.info("**Cargo Apertura:** $0.00 (0.00%)\n\n**Frecuencia de Pago:** Mensual")

        st.markdown("---")
        st.markdown("### Simulador Dinámico de Pagos Mensuales")
        
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            monto_solicitado = st.number_input(
                "Monto a Financiar ($ MXN):",
                min_value=5000,
                max_value=367000,
                value=5000,
                step=500
            )
        with col_input2:
            plazo_meses = st.selectbox(
                "Plazo en Meses:",
                [12, 24, 36, 48, 54, 60],
                index=5
            )

        # Factores exactos por cada $1,000 financiado extraídos directamente del PDF 4918
        factores_directos = {
            60: 36.778,   # $183.89 para $5,000
            54: 38.254,   # $191.27 para $5,000
            48: 40.186,   # $200.93 para $5,000
            36: 46.374,   # $231.87 para $5,000
            24: 59.576,   # $297.88 para $5,000
            12: 100.960   # $504.80 para $5,000
        }
        
        pago_mensual_est = (monto_solicitado / 1000.0) * factores_directos[plazo_meses]
        monto_total_estimado = pago_mensual_est * plazo_meses

        r1, r2, r3 = st.columns(3)
        r1.metric("Pago Mensual Estimado", f"${pago_mensual_est:,.2f}")
        r2.metric("Total de Pagos Mensuales", f"{plazo_meses} Meses")
        r3.metric("Monto Total al Finalizar", f"${monto_total_estimado:,.2f}")

        st.markdown("---")
        st.markdown("### Matriz Representativa de Cotización (Material 4918)")
        
        # Tabla con los montos exactos provenientes del archivo PDF 4918
        tabla_cotizacion = pd.DataFrame([
            {"Monto Financiar": "$5,000.00",   "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$183.89",   "54 Meses": "$191.27",   "48 Meses": "$200.93",   "36 Meses": "$231.87",   "24 Meses": "$297.88",   "12 Meses": "$504.80"},
            {"Monto Financiar": "$10,000.00",  "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$367.78",   "54 Meses": "$382.53",   "48 Meses": "$401.87",   "36 Meses": "$463.73",   "24 Meses": "$595.77",   "12 Meses": "$1,009.61"},
            {"Monto Financiar": "$20,000.00",  "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$735.57",   "54 Meses": "$765.06",   "48 Meses": "$803.73",   "36 Meses": "$927.46",   "24 Meses": "$1,191.54",  "12 Meses": "$2,019.22"},
            {"Monto Financiar": "$50,000.00",  "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$1,838.91",  "54 Meses": "$1,912.65",  "48 Meses": "$2,009.33",  "36 Meses": "$2,318.66",  "24 Meses": "$2,978.85",  "12 Meses": "$5,048.04"},
            {"Monto Financiar": "$100,000.00", "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$3,677.83",  "54 Meses": "$3,825.31",  "48 Meses": "$4,018.65",  "36 Meses": "$4,637.31",  "24 Meses": "$5,957.69",  "12 Meses": "$10,096.08"},
            {"Monto Financiar": "$150,000.00", "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$5,516.74",  "54 Meses": "$5,737.96",  "48 Meses": "$6,027.98",  "36 Meses": "$6,955.97",  "24 Meses": "$8,936.54",  "12 Meses": "$15,144.12"},
            {"Monto Financiar": "$200,000.00", "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$7,355.66",  "54 Meses": "$7,650.61",  "48 Meses": "$8,037.31",  "36 Meses": "$9,274.63",  "24 Meses": "$11,915.38", "12 Meses": "$20,192.15"},
            {"Monto Financiar": "$250,000.00", "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$9,194.57",  "54 Meses": "$9,563.26",  "48 Meses": "$10,046.63", "36 Meses": "$11,593.29", "24 Meses": "$14,894.23", "12 Meses": "$25,240.19"},
            {"Monto Financiar": "$300,000.00", "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$11,033.48", "54 Meses": "$11,475.92", "48 Meses": "$12,055.96", "36 Meses": "$13,911.94", "24 Meses": "$17,873.07", "12 Meses": "$30,288.23"},
            {"Monto Financiar": "$365,000.00", "Tasa %": "31.89%", "CAT %": "37.0%", "60 Meses": "$13,424.07", "54 Meses": "$13,962.36", "48 Meses": "$14,668.08", "36 Meses": "$16,903.01", "24 Meses": "$21,715.78", "12 Meses": "$36,800.20"}
        ])
        st.dataframe(tabla_cotizacion, use_container_width=True)

    # --- TAB 2: SCRIPTS DE ROLEPLAY (ADAPTADOS A MESES CON CIFRAS EXACTAS DEL ARCHIVO) ---
    with tabs[2]:
        st.subheader("🗣️ Guiño y Scripts Oficiales de Roleplay para Ejecutivos")
        
        st.markdown("### 📞 Script A: Apertura y Manejo Efectivo de Objeciones")
        st.markdown(
            """
            <div class='script-box'>
            <b>🎧 EJECUTIVO:</b> "Hola, muy buenas tardes, ¿hablo con el Titular [Nombre del Cliente]? Le llamo de la financiera respecto a su crédito autorizado con descuento por nómina/pensión."<br><br>
            <b>👤 CLIENTE:</b> "Ahorita no me interesa / No tengo tiempo / Ya tengo muchos préstamos."<br><br>
            <b>🎧 EJECUTIVO:</b> "Comprendo perfectamente su tiempo, [Nombre del Cliente]. Precisamente por eso le llamo, porque su crédito ya cuenta con una tasa preferencial congelada del <b>31.89%</b> y sin cargo de apertura ($0.00). No venimos a quitarle tiempo, sino a ofrecerle una liquidez inmediata o consolidación de deudas a su medida. ¿Le parecería si en 2 minutos revisamos el monto mensual que le correspondería sin compromiso?"<br><br>
            <b>👤 CLIENTE:</b> "Bueno, ¿cuánto me podrían prestar y de a cómo me saldría la mensualidad?"
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 📞 Script B: Cierre, Conferencia Tripartita y Transferencia")
        st.markdown(
            """
            <div class='script-box'>
            <b>🎧 EJECUTIVO:</b> "Perfecto, [Nombre del Cliente], para el monto de <b>$[Monto a financiar]</b> a un plazo de <b>[Plazo] meses</b>, su pago mensual queda exactamente en <b>$[Pago mensual]</b> con un CAT del <b>37.0%</b>. ¿Le acomoda este descuento mensual en su pensión/nómina?"<br><br>
            <b>👤 CLIENTE:</b> "Sí, me parece bien esa cantidad."<br><br>
            <b>🎧 EJECUTIVO:</b> "Excelente. Para formalizar y proceder con la liberación de su efectivo, voy a realizar la transferencia de su llamada con nuestro Ejecutivo de Validación en una conferencia tripartita. Por favor manténgase en la línea un momento mientras valido sus documentos en sistema. ¿Tiene a la mano su identificación y comprobante?"
            </div>
            """,
            unsafe_allow_html=True
        )

    with tabs[3]:
        st.subheader("📊 Matriz de Producto Consubanco")

        col_c, col_v, col_b = st.columns(3)
        with col_c:
            st.markdown(
                "<div class='cvb-header' style='background-color:#002D72;'>01."
                " Características</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                *   **Crédito personal**
                *   **No es adelanto** de dinero
                *   **Dinero en efectivo** disponible
                *   **Contrato personalizado** a la medida del cliente
                """,
                unsafe_allow_html=True,
            )

        with col_v:
            st.markdown(
                "<div class='cvb-header' style='background-color:#FF6600;'>02."
                " Ventajas</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                *   **No se revisa buró** de crédito
                *   **Sin aval** o garantías prendarias
                *   **Documentación sencilla** e inmediata
                *   **Tasa fija** durante todo el plazo
                *   **Descuento vía nómina** automatizado
                *   **Autorización ágil** en un periodo de **24 a 72 hrs**
                *   Con opción a un **segundo crédito**
                *   Con opción a un **refinanciamiento** efectivo
                *   **No es hereditario** (cuenta con seguro)
                *   Permite **liquidación anticipada**
                *   Permite **abonar voluntariamente** a capital
                """,
                unsafe_allow_html=True,
            )

        with col_b:
            st.markdown(
                "<div class='cvb-header' style='background-color:#8A95A5;'>03."
                " Beneficios</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                *   **Comodidad:** Sin tener que ir al banco a realizar filas para pagar.
                *   **Tranquilidad:** Descuentos programados directos sin presiones de cobranza.
                *   **Seguridad:** Respaldo institucional que protege las finanzas.
                *   **Trámite digital:** Proceso cómodo, seguro y sin salir de casa.
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.subheader("🛡️ Guía para el Manejo de Objeciones Generales")

        o1, o2 = st.columns(2)
        with o1:
            with st.expander("🗣️ Objeción: 'No me interesa, gracias'"):
                st.write(
                    "**Estrategia:** Rompe el hielo validando su postura y reenfocando"
                    " el beneficio."
                )
                st.info(
                    "💡 **Speech Sugerido:** *'Lo entiendo perfectamente, Señor/Señora"
                    " [Apellido]. Precisamente le llamo porque no busco venderle un"
                    " servicio tradicional, sino informarle de un beneficio exclusivo"
                    " en efectivo que ya tiene autorizado por ser pensionado, sin"
                    " consultar buró ni pedir aval.'*"
                )
            with st.expander("🗣️ Objeción: '¿Me van a revisar Buró de Crédito?'"):
                st.write(
                    "**Estrategia:** Convierte el miedo en una ventaja absoluta de"
                    " Consubanco."
                )
                st.success(
                    "✅ **Speech Sugerido:** *'Despreocúpese por completo,"
                    " Señor/Señora. Una de nuestras mayores ventajas competitivas es"
                    " que NO tomamos en cuenta el historial del Buró para otorgarle su"
                    " dinero en efectivo.'*"
                )
        with o2:
            with st.expander(
                "🗣️ Objeción: 'Tengo desconfianza de los trámites digitales'"
            ):
                st.write(
                    "**Estrategia:** Apóyate en el respaldo institucional y la"
                    " comodidad del proceso."
                )
                st.info(
                    "💡 **Speech Sugerido:** *'Comprendo su cuidado, Señor/Señora, y"
                    " hace muy bien. Consubanco es una institución bancaria totalmente"
                    " regulada. El trámite digital está diseñado para su comodidad,"
                    " protegiendo sus datos personales mediante WhatsApp oficial y"
                    " directo, evitándole dar vueltas o hacer filas innecesarias.'*"
                )
            with st.expander("🗣️ Objeción: '¿Y si quiero pagar antes de tiempo?'"):
                st.write(
                    "**Estrategia:** Destaca los saldos insolutos y la flexibilidad del"
                    " contrato."
                )
                st.info(
                    "💡 **Speech Sugerido:** *'Eso es lo mejor de nuestro esquema,"
                    " Señor/Señora. Usted cuenta con el beneficio de liquidación"
                    " anticipada y abonos voluntarios sin penalización. Al manejarse"
                    " bajo saldos insolutos, el interés solo se cobra sobre el dinero"
                    " pendiente, lo que le permite ahorrar muchísimo si decide pagar"
                    " antes.'*"
                )

        # --- SECCIÓN INTEGRADA: PROGRAMA LAZOS CONSUBANCO 2026 ---
        st.markdown("---")
        st.subheader(
            "🤝 Programa Lazos Consubanco 2026 - Apertura de Cuenta"
        )

        col_lazos1, col_lazos2 = st.columns(2)

        with col_lazos1:
            with st.expander(
                "🏛️ Respaldo Institucional y Soluciones Financieras", expanded=True
            ):
                st.markdown("""
                *   **Experiencia:** Banco regulado y supervisado por la CNBV desde 2012, con más de 25 años de experiencia financiera y presencia nacional.
                *   **Trayectoria:** Más de 1.5 millones de créditos otorgados; #4 en colocación de créditos personales.
                *   **Cuenta de Débito Digital:** Proceso rápido, seguro y 100% digital, sin monto mínimo de apertura ni saldo promedio requerido.
                *   **Inversión en Pagaré:** Tasa y plazo fijo de 1 a 720 días, respaldada por el IPAB hasta por 400,000 UDIs por cliente.
                *   **Pensiona Plus:** Diseñado para mejorar hasta 3 veces más el monto de la pensión en promedio.
                """)

            with st.expander("🎁 Beneficios Exclusivos Lazos para el Cliente"):
                st.markdown("""
                *   **Bono de Bienvenida:** Bono único de bienvenida por $1,000 MXN.
                *   **Reembolso en Retiros:** Hasta $60 MXN de reembolso mensual por retiros en efectivo.
                *   **Bonificación Chedraui:** $50 MXN por cada $500 MXN de compra en tienda y farmacia Chedraui (bonificados en monedero).
                *   **Rendimiento en Saldo a la Vista:** De 3% a 5% de rendimiento por saldo a la vista.
                *   **Inversiones Digitales:** De 9% a 10% de rendimiento en inversiones digitales desde 84 días.
                *   **Descuentos Médicos:** 20% de descuento en Laboratorios Médicos del Chopo.
                *   **Retiros y Servicios:** Más de 84 mil puntos de retiro en el país, además de pago de servicios (Luz, Agua) y descuentos en entretenimiento.
                """)

        with col_lazos2:
            with st.expander(
                "📝 Requisitos y Recomendaciones de Apertura", expanded=True
            ):
                st.markdown("""
                **Requisitos Principales:**
                1. Tener un crédito con Consubanco.
                2. Realizar la apertura de la Cuenta de Débito Digital.
                3. Portabilidad de Nómina / Pensión.

                **Recomendaciones para el Proceso:**
                1. **Uso Exclusivo:** El proceso debe realizarse desde el celular personal del cliente.
                2. **Documentación:** INE vigente. Si no tiene domicilio o no coincide, presentar comprobante (TELMEX o CFE) menor a 3 meses y conocer su RFC con homoclave.
                3. **Captura de Datos:** Capturar los datos exactamente como aparecen en la identificación oficial, sin cambios ni errores.
                4. **Fotos Claras:** Estar en un lugar bien iluminado para la toma de fotografías.
                5. **Activación TDD:** La Tarjeta de Débito se activa desde la aplicación de Consubanco.
                6. **Soporte:** En caso de ayuda, comunicarse con un ejecutivo a Consulínea.
                """)

            with st.expander(
                "🛡️ Manejo de Objeciones Específicas - Programa Lazos"
            ):
                st.markdown("""
                **1. "No conozco el banco"**
                * *Respuesta:* Consubanco es una institución de banca múltiple con más de 20 años de experiencia, consolidada desde 2012. Ofrecemos créditos con descuento vía nómina, Consucuenta Digital, Consubanco App, seguro de vida y asistencias. Puede verificar la trayectoria en `www.consubanco.com`.

                **2. "No tienen sucursales físicas para resolver dudas"**
                * *Respuesta:* Somos un banco digital, lo que nos permite ofrecer mejores beneficios. Gestiones como consultas, transferencias y aclaraciones se realizan de forma cómoda en la Consubanco App. ¡La sucursal está al alcance de sus manos!

                **3. "Se me dificulta ir a un Oxxo y solo retirar parte de mi nómina"**
                * *Respuesta:* Además de Oxxo (con límite de $3,000 MXN por transacción), puede retirar en la red de cajeros VISA y tiendas como Chedraui y Farmacias Guadalajara. También cuenta con transferencias SPEI 24/7 sin costo desde la App.

                **4. "Las tiendas Oxxo no tienen dinero suficiente para montos altos"**
                * *Respuesta:* Para montos de pensión altos, establecimientos como Chedraui, Farmacias Guadalajara y la red de cajeros VISA cuentan con mayor disponibilidad de efectivo. También puede realizar pagos y transferencias directo desde su App.
                """)

        st.markdown("---")
        st.subheader("📚 Glosario y Conceptos Técnicos")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital (El dinero real)"):
                st.write("**Definición:** El monto neto que se entrega al cliente.")
                st.info(
                    "💡 **Tip de Venta:** Recuérdale al cliente que sus abonos bajan esta"
                    " deuda base directamente."
                )
            with st.expander("📌 CAT (Costo Anual Total)"):
                st.write("**Definición:** Indicador que suma tasa, seguros y comisiones.")
                st.info(
                    "💡 **Tip de Venta:** Úsalo para demostrar que no hay cobros"
                    " ocultos; todo está en el CAT."
                )
            with st.expander("📌 Tasa Fija"):
                st.write(
                    "**Definición:** Interés que permanece igual toda la vida del"
                    " crédito."
                )
                st.success(
                    "✅ **Tip de Venta:** Ideal para tiempos de inflación: 'Su pago no"
                    " subirá pase lo que pase'."
                )
        with c2:
            with st.expander("📌 Saldos Insolutos"):
                st.write(
                    "**Definición:** Interés calculado sobre el remanente de la deuda."
                )
                st.info(
                    "💡 **Tip de Venta:** El mejor gancho para quien quiere liquidar"
                    " antes y ahorrar intereses."
                )
            with st.expander("📌 SIPRE (Validación IMSS)"):
                st.write(
                    "**Definición:** Sistema de validación de capacidad para"
                    " pensionados."
                )
                st.info(
                    "💡 **Tip de Venta:** 'Validamos en minutos para que se vaya con la"
                    " seguridad de su aprobación'."
                )
            with st.expander("📋 Requisitos Indispensables"):
                st.write(
                    "- INE Vigente (Frente y Vuelta)\n- Acceso a SIPRE"
                    " (Pensionados)\n- WhatsApp para agilidad"
                )

        # --- SECCIÓN INTEGRADA DE TIPIFICACIONES ---
        st.markdown("---")
        st.subheader("📋 Catálogo Oficial de Tipificaciones V6")

        tip_tab1, tip_tab2, tip_tab3, tip_tab4 = st.tabs([
            "💳 Crédito (Outbound / Inbound)",
            "🤝 Lazos",
            "🛡️ Seguros",
            "🚨 Acciones Especiales / Blacklist",
        ])

        with tip_tab1:
            st.markdown("#### Tipificaciones para Crédito Outbound e Inbound")
            df_credito_outbound = pd.DataFrame([
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "Transferencia",
                    "Descripción": (
                        "La conferencia que se hace con el TMK, CLIENTE Y EJECUTIVO,"
                        " para la validación de información y recepción de"
                        " documentos."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "Se agenda llamada",
                    "Descripción": (
                        "Cuando el cliente sí esté interesado y solicite una llamada"
                        " en un horario o fecha posterior."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "Lo va a pensar",
                    "Descripción": (
                        "Indica que lo va a pensar pero no agenda llamada."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "Se envía información",
                    "Descripción": (
                        "Solicita que le enviemos la información por WhatsApp o"
                        " correo pero no agenda llamada."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "Acepta producto 1 pero no acepta producto 2",
                    "Descripción": "Consuprotección seguro y no asistencia.",
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "Acepta producto 1 y producto 2",
                    "Descripción": "Consuprotección acepta combo.",
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "Acepta producto 2",
                    "Descripción": "Consuprotección asistencia.",
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "Interesado",
                    "Detalle": "No acepta producto 1 pero acepta producto 2",
                    "Descripción": "Consuprotección seguro.",
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No Sujeto a Crédito",
                    "Detalle": "En proceso de Autoservicio",
                    "Descripción": "Ya cuenta con un proceso vigente.",
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No Sujeto a Crédito",
                    "Detalle": "Convenio no gestionable / Sin convenio",
                    "Descripción": "No hay convenio vigente en su dependencia.",
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No Sujeto a Crédito",
                    "Detalle": "Matriz de plazos",
                    "Descripción": (
                        "Cuando exceda la edad o tiempo de antigüedad para realizar"
                        " un CNCA o crédito nuevo en caso de IMSS."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No Sujeto a Crédito",
                    "Detalle": "Sin capacidad de Pago/Nomipay",
                    "Descripción": (
                        "Cuando se valide la capacidad en los portales e indique"
                        " saldo negativo, sin capacidad."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No Sujeto a Crédito",
                    "Detalle": "Políticas generales",
                    "Descripción": (
                        "Cuando no cumpla cualquier política solicitada en GC (edad,"
                        " tipo de plaza, antigüedad, Círculo de Crédito,"
                        " boletinado, ya no labora, etc.)."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": (
                        "Hasta que liquide el actual / Ya tiene muchos créditos"
                    ),
                    "Descripción": (
                        "Cuando indique que quiere terminar con el crédito que tiene"
                        " actualmente."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "Interés muy alto",
                    "Descripción": (
                        "Cuando menciona que la tasa de interés la considera alta."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "No le es suficiente el monto",
                    "Descripción": (
                        "Cuando al cliente no le interesa el monto ya que quiere uno"
                        " más alto."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "No quiere tener deudas",
                    "Descripción": (
                        "Cuando comenta que no le agrada endeudarse o los créditos."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "Poca disposición del cliente",
                    "Descripción": (
                        "Cuando se niegue rotundamente a recibir información."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "Posible demanda",
                    "Descripción": (
                        "Cuando el cliente indica que tiene un proceso de demanda con"
                        " Condusef o el IMSS o amenaza con hacerlo."
                    ),
                },
                {
                    "Tipo de contacto": "Se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "Cliente Molesto",
                    "Descripción": (
                        "Cuando ofenda o utilice un tono de voz alto e indique ya no"
                        " quiere recibir llamadas."
                    ),
                },
                {
                    "Tipo de contacto": "No se identifica al titular",
                    "Estatus": "Contacto con tercero",
                    "Detalle": "Se deja Recado",
                    "Descripción": (
                        "Cuando responda una tercera persona y se deje mensaje."
                    ),
                },
                {
                    "Tipo de contacto": "No se identifica al titular",
                    "Estatus": "Contacto con tercero",
                    "Detalle": "Finado / Sin Beneficiario",
                    "Descripción": (
                        "Cuando un tercero menciona que el cliente ya falleció y"
                        " 'heredó' la pensión."
                    ),
                },
                {
                    "Tipo de contacto": "No se identifica al titular",
                    "Estatus": "Contacto con tercero",
                    "Detalle": "Teléfono equivocado / Reporte de número equivocado",
                    "Descripción": (
                        "Cuando la persona que responde no sea la persona buscada."
                    ),
                },
                {
                    "Tipo de contacto": "No se identifica al titular",
                    "Estatus": "Sin contacto",
                    "Detalle": "Cuelga / Se corta llamada",
                    "Descripción": (
                        "Cuelga o se corta la llamada pero no se confirma que haya"
                        " sido el titular."
                    ),
                },
                {
                    "Tipo de contacto": "No se identifica al titular",
                    "Estatus": "Sin contacto",
                    "Detalle": "Sin Interacción",
                    "Descripción": (
                        "Tono ocupado / Conmutador / Grabadora / Suspendido / Buzón"
                        " de Voz / Número no existe."
                    ),
                },
                {
                    "Tipo de contacto": "No se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "No da información",
                    "Descripción": (
                        "La persona que contesta no da nombre ni muestra interés en"
                        " ninguna propuesta."
                    ),
                },
                {
                    "Tipo de contacto": "No se identifica al titular",
                    "Estatus": "No le interesa",
                    "Detalle": "No es pensionado",
                    "Descripción": "La persona que contesta indica no ser pensionado.",
                },
            ])
            st.dataframe(df_credito_outbound, use_container_width=True)

        with tip_tab2:
            st.markdown("#### Tipificaciones del Programa Lazos")
            df_lazos = pd.DataFrame([
                {
                    "Estatus": "Acepta",
                    "Detalle": "Lazos",
                    "Descripción": "Cliente acepta aperturar cuenta Lazos.",
                },
                {
                    "Estatus": "Acepta",
                    "Detalle": "Agenda llamada",
                    "Descripción": "Solicita llamada posterior para tramitar.",
                },
                {
                    "Estatus": "Acepta",
                    "Detalle": "Se envía información",
                    "Descripción": "Solicita detalles por WhatsApp/correo.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "No quiere cambiar de nómina",
                    "Descripción": "Prefiere conservar su banco actual.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Tiene pagos domiciliados",
                    "Descripción": (
                        "Tiene compromisos de cobro automático en otro banco."
                    ),
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Ya cuenta con portabilidad",
                    "Descripción": "Ya realizó cambio a otra institución.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Posible demanda",
                    "Descripción": "Proceso legal activo contra la institución.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Cliente Molesto",
                    "Descripción": "Inconformidad alta / No desea contacto.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Ninguno de los beneficios le es atractivo",
                    "Descripción": "No muestra interés en la oferta de Lazos.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Otro banco le da mayor rendimiento",
                    "Descripción": "Menciona mejor tasa de rendimiento externa.",
                },
                {
                    "Estatus": "No sujeto a Seguro",
                    "Detalle": "Ya es cliente Lazos",
                    "Descripción": "Cuenta previamente con el producto activo.",
                },
                {
                    "Estatus": "No sujeto a Seguro",
                    "Detalle": "Edad Máxima permitida",
                    "Descripción": (
                        "Excede el límite de edad contractual permitido."
                    ),
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Finado",
                    "Descripción": "Tercero reporta fallecimiento del titular.",
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Se Deja Recado",
                    "Descripción": "Mensaje entregado a familiar/contacto.",
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Teléfono equivocado",
                    "Descripción": "Línea no corresponde al titular.",
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Sin Interacción",
                    "Descripción": "Sin voz humana / Contestadora.",
                },
                {
                    "Estatus": "Sin contacto",
                    "Detalle": "Cuelga / Se corta llamada",
                    "Descripción": "Llamada interrumpida sin confirmar titular.",
                },
            ])
            st.dataframe(df_lazos, use_container_width=True)

        with tip_tab3:
            st.markdown("#### Tipificaciones de Seguros y Asistencias")
            df_seguros = pd.DataFrame([
                {
                    "Estatus": "Acepta",
                    "Detalle": "Seguro",
                    "Descripción": "Aceptación de seguro de vida/protección.",
                },
                {
                    "Estatus": "Acepta",
                    "Detalle": "Asistencia",
                    "Descripción": "Aceptación de plan de asistencias.",
                },
                {
                    "Estatus": "Acepta",
                    "Detalle": "Combo",
                    "Descripción": "Acepta paquete combinado (Seguro + Asistencia).",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Ya cuenta con seguro con Tercero",
                    "Descripción": "Protegido por otra compañía aseguradora.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "No le es suficiente el monto asegurado",
                    "Descripción": "Requiere suma asegurada mayor.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Ya tiene seguro IMSS",
                    "Descripción": "Cubre sus necesidades con la prestación IMSS.",
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Descuentos Altos",
                    "Descripción": (
                        "Considera excesivo el costo de la prima/descuento."
                    ),
                },
                {
                    "Estatus": "No le Interesa",
                    "Detalle": "Cliente Molesto / Cuelga",
                    "Descripción": "Rechazo tajante / Interrupción de llamada.",
                },
                {
                    "Estatus": "No sujeto a Seguro",
                    "Detalle": "Ya cuenta con seguro CSB",
                    "Descripción": "Tiene póliza activa con Consubanco.",
                },
                {
                    "Estatus": "No sujeto a Seguro",
                    "Detalle": "Edad Máxima permitida",
                    "Descripción": "Excede el límite de edad para aseguramiento.",
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Finado",
                    "Descripción": "Titular fallecido.",
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Se Deja Recado",
                    "Descripción": "Recado con familiar.",
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Teléfono equivocado",
                    "Descripción": "Número equivocado.",
                },
                {
                    "Estatus": "Contacto con terceros",
                    "Detalle": "Sin Interacción",
                    "Descripción": "Buzón de voz o falla en comunicación.",
                },
            ])
            st.dataframe(df_seguros, use_container_width=True)

        with tip_tab4:
            st.markdown("#### Protocolos y Acciones Operativas (Blacklist)")
            df_acciones = pd.DataFrame([
                {
                    "Estatus": "No le interesa",
                    "Detalle": "Poca disposición del cliente",
                    "Descripción": (
                        "Cuando se niegue rotundamente a recibir información."
                    ),
                    "Acción CCC": "N/A",
                    "Acción DH": "Ingresar a blacklist temporal CCC - 15 días",
                    "Alcance": "La cuenta de CCC",
                },
                {
                    "Estatus": "No le interesa",
                    "Detalle": "Cliente Molesto",
                    "Descripción": (
                        "Cuando ofenda o utilice un tono de voz alto e indique ya no"
                        " quiere recibir llamadas."
                    ),
                    "Acción CCC": "Black List Campaign",
                    "Acción DH": "Ingresar a blacklist temporal CCC - 30 días",
                    "Alcance": "La cuenta de CCC",
                },
                {
                    "Estatus": "No le interesa",
                    "Detalle": "Posible demanda",
                    "Descripción": (
                        "Cuando el cliente indica que tiene un proceso de demanda con"
                        " Condusef o el IMSS."
                    ),
                    "Acción CCC": "Black List Permanently",
                    "Acción DH": "Se manda a BL por tres meses",
                    "Alcance": "Se envía a DH",
                },
                {
                    "Estatus": "Contacto con tercero",
                    "Detalle": "Finado / Sin Beneficiario",
                    "Descripción": (
                        "Cuando un tercero menciona que el cliente ya falleció."
                    ),
                    "Acción CCC": "N/A",
                    "Acción DH": (
                        "Se manda después de la X tipificación con el mismo detalle"
                    ),
                    "Alcance": "La cuenta de CCC",
                },
                {
                    "Estatus": "Contacto con tercero",
                    "Detalle": "Teléfono equivocado",
                    "Descripción": (
                        "Cuando la persona que responde no sea la persona buscada."
                    ),
                    "Acción CCC": "N/A",
                    "Acción DH": (
                        "Se manda después de la X tipificación con el mismo detalle"
                    ),
                    "Alcance": "La cuenta de CCC",
                },
            ])
            st.dataframe(df_acciones, use_container_width=True)

    with tabs[4]:
        st.subheader("📊 Historial de Aprendizaje")
        st.dataframe(
            hist[["Fecha", "Calificación", "Rango"]], use_container_width=True
        )
        if is_admin:
            st.write("---")
            st.write("### Panel de Control (Admin)")
            st.dataframe(st.session_state.db, use_container_width=True)
            st.download_button(
                "📥 Exportar Reporte Global (CSV)",
                st.session_state.db.to_csv(index=False),
                "Reporte_Academia.csv",
            )
