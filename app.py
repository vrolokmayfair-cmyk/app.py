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
    .instrucciones-box {{
        background-color: #E8F0FE; padding: 15px; border-radius: 10px;
        border: 1px solid {COLOR_AZUL}; margin-bottom: 20px;
    }}
    h1, h2, h3 {{ color: {COLOR_AZUL}; font-family: 'Arial'; }}
    .cvb-header {{
        padding: 10px; color: white; font-weight: bold; text-align: center; border-radius: 5px; margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE AUXILIARES Y DATOS ---
def limpiar_cifra_numerica(texto: str) -> str:
    """Limpia la entrada del usuario eliminando comas, puntos, signos $ y espacios."""
    if not texto:
        return ""
    return texto.replace(",", "").replace(".", "").replace("$", "").replace(" ", "").strip()

def cargar_datos():
    if os.path.exists(DB_FILE):
        try: return pd.read_csv(DB_FILE)
        except: return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])
    return pd.DataFrame(columns=["Nombre", "Nivel", "Calificación", "Intentos", "Rango", "Fecha"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'db' not in st.session_state:
    st.session_state.db = cargar_datos()

if 'ejercicio_teoria' not in st.session_state:
    st.session_state.ejercicio_teoria = None

if 'ejercicio_practico' not in st.session_state:
    st.session_state.ejercicio_practico = None

# --- BANCO TEÓRICO EXPANDIDO (+100 VARIACIONES AL AZAR) ---
def generar_teoria():
    conceptos = [
        {
            "t": "Saldos Insolutos",
            "preguntas": [
                "¿Cómo se llama el esquema donde el interés se calcula únicamente sobre el capital pendiente?",
                "¿Qué nombre recibe el sistema de cobro donde tu deuda real disminuye conforme realizas abonos?",
                "¿Bajo qué esquema de cobro de intereses se beneficia directamente al cliente que realiza pagos anticipados?"
            ],
            "c": ["insoluto", "saldos insolutos", "saldo insoluto"],
            "r": "Retroalimentación: Los saldos insolutos calculan el interés solo sobre lo que resta por pagar, premiando la liquidación anticipada."
        },
        {
            "t": "CAT",
            "preguntas": [
                "¿Qué siglas definen el Costo Anual Total que agrupa tasa, comisiones y seguros?",
                "¿Cuál es el indicador oficial de transparencia financiera que permite comparar créditos?",
                "¿Qué métrica obligatoria incluye todos los costos reales de un financiamiento?"
            ],
            "c": ["cat"],
            "r": "Retroalimentación: El CAT integra de forma transparente todos los costos asociados al crédito en un solo porcentaje anual."
        },
        {
            "t": "SIPRE",
            "preguntas": [
                "¿Cómo se llama el portal oficial para validar la capacidad de descuento de un pensionado IMSS?",
                "¿Qué sistema utilizamos para consultar la disponibilidad exacta de descuento de un cliente IMSS?",
                "¿Cuál es la herramienta digital indispensable para validar la capacidad de pago institucional?"
            ],
            "c": ["sipre"],
            "r": "Retroalimentación: El SIPRE es el portal institucional oficial para validar y asegurar la capacidad de descuento del pensionado."
        },
        {
            "t": "Tasa Fija",
            "preguntas": [
                "¿Cómo se le llama al tipo de interés que protege al cliente asegurando que su pago no subirá jamás?",
                "¿Qué característica de nuestra tasa garantiza estabilidad económica ante la inflación?",
                "¿Qué clase de tasa ofrece total certidumbre al presupuesto mensual del pensionado?"
            ],
            "c": ["tasa fija", "fija"],
            "r": "Retroalimentación: La tasa fija blinda al cliente frente a la inflación, garantizando que su descuento permanezca intacto."
        },
        {
            "t": "INE",
            "preguntas": [
                "¿Qué documento oficial de identificación con fotografía es obligatorio y requisito #1?",
                "¿Sin qué credencial oficial vigente no podemos iniciar ningún trámite de crédito?",
                "¿Cuál es el documento de identidad principal que debemos solicitar desde el primer contacto?"
            ],
            "c": ["ine", "identificacion", "credencial"],
            "r": "Retroalimentación: El INE vigente es el documento básico e indispensable para validar la identidad y dar inicio al proceso."
        },
        {
            "t": "Capital",
            "preguntas": [
                "¿Cómo se le denomina al monto neto o dinero real que se le entrega al cliente?",
                "¿Qué término define el recurso financiero base que el cliente recibe en su cuenta?",
                "¿Cómo se le llama a la suma directa prestada antes de aplicar accesorios o plazos?"
            ],
            "c": ["capital"],
            "r": "Retroalimentación: El capital representa el monto neto del préstamo que el cliente recibe directamente para su disposición."
        },
        {
            "t": "Interés Compuesto",
            "preguntas": [
                "Por política de Consubanco, ¿cobramos intereses sobre intereses? (Sí/No)",
                "¿Aplicamos el esquema de anatocismo o interés compuesto en nuestros créditos de nómina? (Sí/No)",
                "¿Está permitido cobrar cargos financieros sobre intereses atrasados en Consubanco? (Sí/No)"
            ],
            "c": ["no", "falso"],
            "r": "Retroalimentación: Correcto. En Consubanco protegemos el patrimonio del cliente prohibiendo el anatocismo o interés compuesto."
        },
        {
            "t": "Tabla de Amortización",
            "preguntas": [
                "¿Cómo se llama el documento detallado que muestra el calendario y desglose de cada pago?",
                "¿Qué formato desglosa periodo a periodo el capital, intereses y seguros de un crédito?",
                "¿Qué tabla descriptiva le otorga total transparencia al cliente sobre su plan de pagos?"
            ],
            "c": ["tabla de amortización", "tabla de amortizacion", "tabla"],
            "r": "Retroalimentación: La tabla de amortización detalla de forma transparente la evolución de cada mensualidad y el saldo remanente."
        },
        {
            "t": "WhatsApp",
            "preguntas": [
                "¿Qué medio de comunicación digital utilizamos de forma principal para agilizar el envío de documentos?",
                "¿A través de qué canal oficial de mensajería instantánea recibimos los expedientes de forma segura?",
                "¿Qué vía digital resulta clave para mantener un seguimiento ágil y constante con el cliente?"
            ],
            "c": ["whatsapp"],
            "r": "Retroalimentación: El WhatsApp es el canal oficial ágil y seguro para la recepción de expedientes y la comunicación directa."
        }
    ]
    
    item = random.choice(conceptos)
    pregunta_texto = random.choice(item["preguntas"])
    return {
        "p": pregunta_texto,
        "c": item["c"],
        "r": item["r"]
    }

# --- LABORATORIO DE CÁLCULOS Y OBJECIONES EXPANDIDO (+100 VARIACIONES AL AZAR) ---
def generar_practico():
    nombres_clientes = ["Martínez", "Rodríguez", "Hernández", "García", "López", "González", "Pérez", "Ramírez", "Flores", "Sánchez"]
    apodo = random.choice(nombres_clientes)
    
    monto_base = random.randint(10, 80) * 1000
    plazo = random.choice([12, 24, 36, 48, 60, 72, 84])
    pago_cotizado = round((monto_base * random.uniform(1.25, 1.45)) / plazo, -1)
    monto_total = int(pago_cotizado * plazo)
    
    banco_practicos = [
        {
            "tipo": "input",
            "p": f"🧮 CÁLCULO DE MONTO TOTAL: Tras realizar la cotización en el sistema, le informas al Señor/Señora {apodo} que su descuento mensual autorizado es de ${pago_cotizado:,.0f} a un plazo de {plazo} meses. El cliente te pregunta directamente: '¿Cuánto voy a pagar en total al finalizar el crédito?'. Realiza la operación matemática correspondiente:",
            "c": str(monto_total),
            "r": f"Retroalimentación: El cálculo correcto se obtiene multiplicando el pago mensual (${pago_cotizado:,.0f}) por el número de meses del plazo ({plazo}), arrojando un Monto Total de ${monto_total:,.0f}."
        },
        {
            "tipo": "radio",
            "p": f"📈 MANEJO DE TASAS: Al ofrecerle una opción de crédito al Señor/Señora {apodo}, este te comenta que otra institución le ofrece una tasa supuestamente más baja pero de tipo 'Variable'. ¿Cuál es el argumento comercial técnico ideal para defender la Tasa Fija de Consubanco?",
            "options": [
                "Mencionar que las tasas variables son ilegales en créditos de nómina y que nosotros somos los únicos regulados.",
                "Explicar el blindaje financiero: 'Comprendo su punto, Señor/Señora {apodo}. Sin embargo, una tasa variable significa que sus descuentos mensuales podrían dispararse si las condiciones macroeconómicas cambian. Con la Tasa Fija de Consubanco usted tiene la absoluta certeza de que su pago no subirá ni un solo peso, protegiendo su economía familiar hasta el último día.'",
                "Decirle que nuestra tasa fija es más alta al principio pero que con los abonos voluntarios se compensa sola."
            ],
            "c": f"Explicar el blindaje financiero: 'Comprendo su punto, Señor/Señora {apodo}. Sin embargo, una tasa variable significa que sus descuentos mensuales podrían dispararse si las condiciones macroeconómicas cambian. Con la Tasa Fija de Consubanco usted tiene la absoluta certeza de que su pago no subirá ni un solo peso, protegiendo su economía familiar hasta el último día.'",
            "r": "Retroalimentación: ¡Excelente! La tasa fija se posiciona con éxito como un escudo protector frente a la inestabilidad de las tasas variables."
        },
        {
            "tipo": "radio",
            "p": f"🛡️ MANEJO DE OBJECIONES (CAT): Estás dialogando con el Señor/Señora {apodo} y este te interrumpe manifestando desconfianza: 'No me interesa, las financieras siempre esconden comisiones, seguros obligatorios y cobros ocultos'. ¿Cómo respondes aplicando normatividad y términos financieros?",
            "options": [
                "Asegurarle que si encuentra algo oculto puede cancelar sin costo en los primeros cinco días.",
                "Aplicar empatía y transparencia con el CAT: 'Comprendo perfectamente su preocupación, Señor/Señora {apodo}. Precisamente por seguridad, en Consubanco somos una institución regulada y le garantizamos transparencia absoluta a través de nuestro CAT (Costo Anual Total); este indicador legal ya integra la tasa, comisiones y seguros desde el primer momento, garantizándole cero sorpresas.'",
                "Decirle que ignore los seguros ya que esos son trámites internos que no afectan su dinero en efectivo."
            ],
            "c": f"Aplicar empatía y transparencia con el CAT: 'Comprendo perfectamente su preocupación, Señor/Señora {apodo}. Precisamente por seguridad, en Consubanco somos una institución regulada y le garantizamos transparencia absoluta a través de nuestro CAT (Costo Anual Total); este indicador legal ya integra la tasa, comisiones y seguros desde el primer momento, garantizándole cero sorpresas.'",
            "r": "Retroalimentación: ¡Correcto! Utilizar el CAT como herramienta de transparencia desarma por completo la objeción de cargos ocultos."
        },
        {
            "tipo": "radio",
            "p": f"🛡️ MANEJO DE OBJECIONES (INTERÉS COMPUESTO): El Señor/Señora {apodo} te expresa un temor muy común: 'He sabido de casos donde la gente se atrasa y les aplican intereses sobre intereses, volviendo la deuda impagable'. ¿Cómo neutralizas esta objeción?",
            "options": [
                "Garantizar la política estricta de no anatocismo: 'Entiendo su inquietud, Señor/Señora {apodo}. En Consubanco su patrimonio está totalmente protegido: por norma y contrato institucional NO aplicamos interés compuesto ni anatocismo. Sus intereses ordinarios jamás generarán cargos adicionales sobre intereses moratorios.'",
                "Explicarle que como el descuento es directo vía nómina es imposible que se atrase y sufra ese problema.",
                "Comentarle que si liquida antes de tiempo todos esos intereses compuestos se eliminan automáticamente."
            ],
            "c": f"Garantizar la política estricta de no anatocismo: 'Entiendo su inquietud, Señor/Señora {apodo}. En Consubanco su patrimonio está totalmente protegido: por norma y contrato institucional NO aplicamos interés compuesto ni anatocismo. Sus intereses ordinarios jamás generarán cargos adicionales sobre intereses moratorios.'",
            "r": "Retroalimentación: ¡Excelente respuesta! Aclarar de forma tajante la ausencia de interés compuesto transmite absoluta seguridad y confianza."
        },
        {
            "tipo": "radio",
            "p": f"🛡️ MANEJO DE OBJECIONES (LIQUIDACIÓN ANTICIPADA): Durante la llamada, el Señor/Señora {apodo} te dice: 'Me agrada el efectivo, pero me aterra amarrarme a un plazo de {plazo} meses por si tengo liquidez y quiero liquidar antes'. ¿Qué esquema técnico le explicas para tranquilizarlo?",
            "options": [
                "Explicar las bondades de los Saldos Insolutos: 'Es una excelente postura, Señor/Señora {apodo}. Con nosotros tiene total libertad de realizar abonos voluntarios o liquidar el crédito de manera anticipada sin penalización alguna. Al operar bajo el esquema de saldos insolutos, los intereses se calculan exclusivamente sobre el capital que aún debe, logrando un ahorro masivo si decide terminar antes.'",
                "Mencionar que el plazo es un requisito obligatorio del banco pero que puede pedir una prórroga de pagos cada año.",
                "Decirle que no se preocupe por el plazo largo ya que los intereses ya vienen calculados en una sola exhibición."
            ],
            "c": f"Explicar las bondades de los Saldos Insolutos: 'Es una excelente postura, Señor/Señora {apodo}. Con nosotros tiene total libertad de realizar abonos voluntarios o liquidar el crédito de manera anticipada sin penalización alguna. Al operar bajo el esquema de saldos insolutos, los intereses se calculan exclusivamente sobre el capital que aún debe, logrando un ahorro masivo si decide terminar antes.'",
            "r": "Retroalimentación: ¡Perfecto! Dominar los Saldos Insolutos y asociarlos a la liquidación sin penalización es la clave maestra para cerrar clientes precavidos."
        }
    ]
    
    return random.choice(banco_practicos)

# --- INTERFAZ ---
st.title("🏦 Academia de Ventas Consubanco")

with st.sidebar:
    st.image("https://www.consubanco.com/assets/images/logo.svg", width=180)
    st.markdown("---")
    st.markdown("""
    <div class='instrucciones-box'>
    <b>📋 INSTRUCCIONES DE ACCESO:</b><br><br>
    1. <b>Registro:</b> Ingresa nombre por APELLIDOS.<br>
    2. <b>Navegación:</b> Usa las pestañas superiores.<br>
    3. <b>Evaluación:</b> Elige módulo y valida respuesta.
    </div>
    """, unsafe_allow_html=True)
    nombre_raw = st.text_input("NOMBRE COMPLETO:").strip().upper()
    with st.expander("🔐 Administrador"):
        admin_pass = st.text_input("Contraseña:", type="password")
        is_admin = (admin_pass == "CSB2026")

if not nombre_raw:
    st.warning("⬅️ Ingresa tu nombre para comenzar.")
else:
    es_instructor = (nombre_raw == MI_NOMBRE_CONTROL)
    hist = st.session_state.db[st.session_state.db["Nombre"] == nombre_raw]
    nivel = "Experto" if es_instructor else "Básico"
    rango = "Diamante" if es_instructor else "Bronce"

    st.markdown(f"<div class='rango-box'><h2>Bienvenido, {nombre_raw}</h2><p><b>Rango:</b> {rango} | <b>Módulo:</b> {nivel}</p></div>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Evaluación", "🎙️ Roleplay", "📚 Glosario e Infografías", "🕹️ Centro de Juegos", "📊 Evolución"])

    with tabs[0]:
        st.subheader("Evaluación Dinámica de Conocimientos")
        mod_sel = st.radio("Módulo de aprendizaje:", ["Teoría y Conceptos", "Laboratorio de Cálculos"], horizontal=True)
        
        if mod_sel == "Teoría y Conceptos":
            if st.button("Generar Nueva Pregunta Teórica") or st.session_state.ejercicio_teoria is None:
                st.session_state.ejercicio_teoria = generar_teoria()
            ej = st.session_state.ejercicio_teoria
            
            st.info(ej["p"])
            resp_raw = st.text_input("Escribe tu respuesta aquí:", key="ans_teoria").strip().lower()
            resp = resp_raw
            
        else:
            if st.button("Generar Nuevo Caso Práctico (Cálculo / Objeción)") or st.session_state.ejercicio_practico is None:
                st.session_state.ejercicio_practico = generar_practico()
            ej = st.session_state.ejercicio_practico
            
            st.info(ej["p"])
            if ej["tipo"] == "input":
                resp_raw = st.text_input("Escribe tu respuesta numérica aquí (puedes usar comas como 92,400 o escribirlo directo 92400):", key="ans_practico_in")
                # Limpiamos comas, puntos o signos para permitir cualquier formato numérico
                resp = limpiar_cifra_numerica(resp_raw)
            else:
                resp = st.radio("Selecciona la mejor opción de Speech Profesional para el manejo de la llamada:", ej["options"], key="ans_practico_rad")
        
        if st.button("Validar Respuesta"):
            correctas = ej["c"]
            es_valida = resp in correctas if isinstance(correctas, list) else resp == correctas
            
            if es_valida:
                st.success("¡Excelente! Respuesta correcta.")
                calif = 10.0
            else:
                st.error("Respuesta incorrecta.")
                st.warning(ej["r"])
                calif = 0.0
            
            log = {"Nombre": nombre_raw, "Nivel": nivel, "Calificación": calif, "Intentos": len(hist)+1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([log])], ignore_index=True)
            guardar_datos(st.session_state.db)

    with tabs[1]:
        st.subheader("🎙️ Análisis Método B (Speech)")
        speech = st.text_area("Pega tu speech de venta aquí:", height=150)
        if st.button("Analizar Speech"):
            t = speech.lower()
            errs = []
            if not any(x in t for x in ["hola", "buen", "presento"]): errs.append("- Falta saludo o presentación inicial.")
            if not any(x in t for x in ["monto", "pago", "pesos", "$", "000"]): errs.append("- Falta la oferta económica clara.")
            if "consubanco" not in t: errs.append("- Olvidaste mencionar el respaldo de Consubanco.")
            
            if not errs: st.success("¡Speech Profesional! Cumple con los pilares del Método B.")
            else: 
                st.error("Puntos a mejorar en tu speech:")
                for e in errs: st.write(e)

    with tabs[2]:
        st.subheader("📊 Matriz de Producto Consubanco")
        
        col_c, col_v, col_b = st.columns(3)
        with col_c:
            st.markdown("<div class='cvb-header' style='background-color:#002D72;'>01. Características</div>", unsafe_allow_html=True)
            st.markdown("""
            *   **Crédito personal**
            *   **No es adelanto** de dinero
            *   **Dinero en efectivo** disponible
            *   **Contrato personalizado** a la medida del cliente
            """, unsafe_allow_html=True)
            
        with col_v:
            st.markdown("<div class='cvb-header' style='background-color:#FF6600;'>02. Ventajas</div>", unsafe_allow_html=True)
            st.markdown("""
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
            """, unsafe_allow_html=True)
            
        with col_b:
            st.markdown("<div class='cvb-header' style='background-color:#8A95A5;'>03. Beneficios</div>", unsafe_allow_html=True)
            st.markdown("""
            *   **Comodidad:** Sin tener que ir al banco a realizar filas para pagar.
            *   **Tranquilidad:** Descuentos programados directos sin presiones de cobranza.
            *   **Seguridad:** Respaldo institucional que protege las finanzas.
            *   **Trámite digital:** Proceso cómodo, seguro y sin salir de casa.
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("🛡️ Guía para el Manejo de Objeciones")
        
        o1, o2 = st.columns(2)
        with o1:
            with st.expander("🗣️ Objeción: 'No me interesa, gracias'"):
                st.write("**Estrategia:** Rompe el hielo validando su postura y reenfocando el beneficio.")
                st.info("💡 **Speech Sugerido:** *'Lo entiendo perfectamente, Señor/Señora [Apellido]. Precisamente le llamo porque no busco venderle un servicio tradicional, sino informarle de un beneficio exclusivo en efectivo que ya tiene autorizado por ser pensionado, sin consultar buró ni pedir aval.'*")
            with st.expander("🗣️ Objeción: '¿Me van a revisar Buró de Crédito?'"):
                st.write("**Estrategia:** Convierte el miedo en una ventaja absoluta de Consubanco.")
                st.success("✅ **Speech Sugerido:** *'Despreocúpese por completo, Señor/Señora. Una de nuestras mayores ventajas competitivas es que NO tomamos en cuenta el historial del Buró para otorgarle su dinero en efectivo.'*")
        with o2:
            with st.expander("🗣️ Objeción: 'Tengo desconfianza de los trámites digitales'"):
                st.write("**Estrategia:** Apóyate en el respaldo institucional y la comodidad del proceso.")
                st.info("💡 **Speech Sugerido:** *'Comprendo su cuidado, Señor/Señora, y hace muy bien. Consubanco es una institución bancaria totalmente regulada. El trámite digital está diseñado para su comodidad, protegiendo sus datos personales mediante WhatsApp oficial y directo, evitándole dar vueltas o hacer filas innecesarias.'*")
            with st.expander("🗣️ Objeción: '¿Y si quiero pagar antes de tiempo?'"):
                st.write("**Estrategia:** Destaca los saldos insolutos y la flexibilidad del contrato.")
                st.info("💡 **Speech Sugerido:** *'Eso es lo mejor de nuestro esquema, Señor/Señora. Usted cuenta con el beneficio de liquidación anticipada y abonos voluntarios sin penalización. Al manejarse bajo saldos insolutos, el interés solo se cobra sobre el dinero pendiente, lo que le permite ahorrar muchísimo si decide pagar antes.'*")

        st.markdown("---")
        st.subheader("📚 Glosario y Conceptos Técnicos")
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("📌 Capital (El dinero real)"):
                st.write("**Definición:** El monto neto que se entrega al cliente.")
                st.info("💡 **Tip de Venta:** Recuérdale al cliente que sus abonos bajan esta deuda base directamente.")
            with st.expander("📌 CAT (Costo Anual Total)"):
                st.write("**Definición:** Indicador que suma tasa, seguros y comisiones.")
                st.info("💡 **Tip de Venta:** Úsalo para demostrar que no hay cobros ocultos; todo está en el CAT.")
            with st.expander("📌 Tasa Fija"):
                st.write("**Definición:** Interés que permanece igual toda la vida del crédito.")
                st.success("✅ **Tip de Venta:** Ideal para tiempos de inflación: 'Su pago no subirá pase lo que pase'.")
        with c2:
            with st.expander("📌 Saldos Insolutos"):
                st.write("**Definición:** Interés calculado sobre el remanente de la deuda.")
                st.info("💡 **Tip de Venta:** El mejor gancho para quien quiere liquidar antes y ahorrar intereses.")
            with st.expander("📌 SIPRE (Validación IMSS)"):
                st.write("**Definición:** Sistema de validación de capacidad para pensionados.")
                st.info("💡 **Tip de Venta:** 'Validamos en minutos para que se vaya con la seguridad de su aprobación'.")
            with st.expander("📋 Requisitos Indispensables"):
                st.write("- INE Vigente (Frente y Vuelta)\n- Acceso a SIPRE (Pensionados)\n- WhatsApp para agilidad")

    with tabs[4]:
        st.subheader("📊 Historial de Aprendizaje")
        st.dataframe(hist[["Fecha", "Calificación", "Rango"]], use_container_width=True)
        if is_admin:
            st.write("---")
            st.write("### Panel de Control (Admin)")
            st.dataframe(st.session_state.db)
            st.download_button("📥 Exportar Reporte Global (CSV)", st.session_state.db.to_csv(index=False), "Reporte_Academia.csv")
