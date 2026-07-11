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

# --- FUNCIONES DE DATOS ---
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

# --- LÓGICA DE EJERCICIOS TEÓRICOS ---
def generar_teoria():
    banco = [
        {"p": "¿Cómo se llama el cobro de interés sobre el capital pendiente?", "c": ["insoluto", "saldos insolutos", "saldo insoluto"], "r": "Retroalimentación: El interés sobre saldos insolutos premia al cliente que paga a tiempo reduciendo su deuda real."},
        {"p": "¿Qué siglas definen el Costo Anual Total (incluye tasa, seguros y comisiones)?", "c": ["cat"], "r": "Retroalimentación: El CAT es la herramienta de transparencia para comparar créditos."},
        {"p": "¿Portal oficial para validar capacidad de descuento del pensionado IMSS?", "c": ["sipre"], "r": "Retroalimentación: El SIPRE es indispensable para evitar rechazos por falta de capacidad."},
        {"p": "¿Cómo se llama la tasa que garantiza estabilidad y no sube con la inflación?", "c": ["tasa fija", "fija"], "r": "Retroalimentación: La tasa fija es seguridad para el bolsillo del cliente."},
        {"p": "¿Qué documento oficial vigente es el requisito #1 para el trámite?", "c": ["ine", "identificacion"], "r": "Retroalimentación: Sin INE vigente no hay proceso; valídalo desde el saludo."},
        {"p": "¿Cómo se le llama al monto neto que efectivamente recibe el cliente?", "c": ["capital"], "r": "Retroalimentación: El capital es el dinero 'líquido' que el cliente usará."},
        {"p": "¿En Consubanco aplicamos interés compuesto (interés sobre interés)? (Sí/No)", "c": ["no", "falso"], "r": "Retroalimentación: No aplicamos anatocismo, lo cual protege el patrimonio del cliente."},
        {"p": "¿Documento que detalla el calendario de pagos, seguros y abonos?", "c": ["tabla de amortización", "tabla de amortizacion", "tabla"], "r": "Retroalimentación: La tabla de amortización da certeza sobre la duración del crédito."},
        {"p": "¿Cómo se llama la capacidad de descuento máxima permitida por ley?", "c": ["capacidad de pago", "capacidad", "descuento maximo"], "r": "Retroalimentación: Cuidar la capacidad de pago asegura la salud financiera del pensionado."},
        {"p": "¿Qué medio de contacto es vital para el envío de documentos y seguimientos?", "c": ["whatsapp"], "r": "Retroalimentación: El WhatsApp es nuestra herramienta principal y más ágil para el envío seguro de expedientes."}
    ]
    return random.choice(banco)

# --- LABORATORIO DE CÁLCULOS, TASAS Y OBJECIONES REFORMULADO ---
def generar_practico():
    monto_base = random.randint(15, 70) * 1000
    plazo = random.choice([24, 36, 48, 60, 72, 84])
    # Pago mensual ficticio proveniente del cotizador simulado para el ejercicio de monto total
    pago_cotizador = round((monto_base * 1.38) / plazo, 0)
    monto_total = pago_cotizador * plazo
    
    opciones_calc = [
        {
            "tipo": "input",
            "p": f"🧮 CALCULO DE MONTO TOTAL: Tu cotizador arroja que un cliente califica para recibir su capital en efectivo con un descuento mensual exacto de ${pago_cotizador:,.0f} a un plazo fijo de {plazo} meses. ¿Cuál es el Monto Total exacto que debes registrar como valor final que pagará el cliente?",
            "c": str(int(monto_total)),
            "r": f"Retroalimentación: El Monto Total que pagará el cliente a lo largo de la vida del crédito se calcula multiplicando el descuento mensual arrojado por tu cotizador (${pago_cotizador:,.0f}) por el número de meses pactados ({plazo}), lo que equivale a ${monto_total:,.0f}."
        },
        {
            "tipo": "radio",
            "p": f"🛡️ MANEJO DE OBJECIONES: Al presentarle una propuesta de crédito de nómina, el Señor López te comenta preocupado: 'Sé que los intereses en México están subiendo mucho por las noticias, no quiero que mi descuento mensual empiece a cambiar de precio el próximo año'. ¿Cómo manejas esta situación utilizando las condiciones de nuestra tasa de interés?",
            "options": [
                "Decirle que no se preocupe, que si la tasa llega a subir nosotros le avisamos por WhatsApp antes de aplicar el descuento.",
                "Darle certeza con la Tasa Fija: 'Lo entiendo y es una excelente preocupación, Señor López. Con Consubanco tiene tranquilidad total, ya que operamos con una Tasa Fija. Esto significa que su descuento mensual de hoy será exactamente el mismo hasta el último mes de su crédito, sin importar la inflación o los cambios en la economía.'",
                "Explicarle que el descuento se calcula de acuerdo al portal SIPRE y que por ley la tasa no se puede modificar una vez cargado el trámite."
            ],
            "c": "Darle certeza con la Tasa Fija: 'Lo entiendo y es una excelente preocupación, Señor López. Con Consubanco tiene tranquilidad total, ya que operamos con una Tasa Fija. Esto significa que su descuento mensual de hoy será exactamente el mismo hasta el último mes de su crédito, sin importar la inflación o los cambios en la economía.'",
            "r": "Retroalimentación: ¡Excelente! La Tasa Fija es el mejor escudo comercial contra el miedo a la inflación, otorgando seguridad financiera total al Señor López desde el primer momento."
        },
        {
            "tipo": "radio",
            "p": f"🛡️ MANEJO DE OBJECIONES: Una clienta, la Señora Gómez, te dice: 'Me interesa el dinero en efectivo pero otra institución me ofrece una tasa mensual más baja en su publicidad'. Sabiendo que el costo real implica seguros y comisiones integradas, ¿cómo defiendes tu venta utilizando los términos financieros correctos?",
            "options": [
                "Mencionar que las otras financieras mienten en sus tasas y que la de nosotros es mejor porque se descuenta directo por nómina.",
                "Reenfocar la venta hacia el CAT: 'Comprendo, Señora Gómez. Muchas instituciones muestran tasas de interés bajas que no reflejan el costo real porque no incluyen comisiones ni seguros obligatorios. En Consubanco somos transparentes: le pedimos comparar el CAT (Costo Anual Total), que incluye absolutamente todo, garantizándole que con nosotros no tendrá sorpresas ni cobros ocultos.'",
                "Pedirle que le mande una captura de la tabla de amortización de la competencia por WhatsApp para ver si se la podemos igualar."
            ],
            "c": "Reenfocar la venta hacia el CAT: 'Comprendo, Señora Gómez. Muchas instituciones muestran tasas de interés bajas que no reflejan el costo real porque no incluyen comisiones ni seguros obligatorios. En Consubanco somos transparentes: le pedimos comparar el CAT (Costo Anual Total), que incluye absolutamente todo, garantizándole que con nosotros no tendrá sorpresas ni cobros ocultos.'",
            "r": "Retroalimentación: ¡Es correcto! El CAT es la herramienta legal y técnica idónea para neutralizar argumentos de tasas nominales engañosas de la competencia, demostrando la honestidad de Consubanco."
        },
        {
            "tipo": "radio",
            "p": f"🛡️ MANEJO DE OBJECIONES: El Señor Sánchez objeta la cotización diciendo: 'El dinero me sirve, pero considero que terminaré pagando una cantidad muy alta sumando todos los meses'. ¿Qué argumento financiero del glosario utilizas para rescatar el cierre?",
            "options": [
                "Explicar el beneficio de los Saldos Insolutos: 'Entiendo su punto, Señor Sánchez. Sin embargo, recuerde que nuestro esquema opera bajo Saldos Insolutos. Esto significa que usted tiene el derecho por contrato de realizar abonos voluntarios directos a capital o liquidar el total anticipadamente sin penalización. Al hacerlo, el interés se recalcula solo sobre lo que reste, lo que reduce drásticamente el monto total que pagará.'",
                "Mencionar que al ser un crédito personalizado el interés compuesto se congela para que no aumente su deuda.",
                "Decirle que al dividir el monto total entre todo el plazo se dará cuenta de que es una inversión sumamente cómoda y digital."
            ],
            "c": "Explicar el beneficio de los Saldos Insolutos: 'Entiendo su punto, Señor Sánchez. Sin embargo, recuerde que nuestro esquema opera bajo Saldos Insolutos. Esto significa que usted tiene el derecho por contrato de realizar abonos voluntarios directos a capital o liquidar el total anticipadamente sin penalización. Al hacerlo, el interés se recalcula solo sobre lo que reste, lo que reduce drásticamente el monto total que pagará.'",
            "r": "Retroalimentación: ¡Gran cierre! Destacar los Saldos Insolutos le devuelve el control financiero al Señor Sánchez, quitando la percepción de un crédito 'eterno' o impagable."
        }
    ]
    return random.choice(opciones_calc)

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
            resp = st.text_input("Escribe tu respuesta aquí:", key="ans_teoria").strip().lower()
            
        else:
            if st.button("Generar Nuevo Ejercicio Práctico (Cálculo / Objeción)") or st.session_state.ejercicio_practico is None:
                st.session_state.ejercicio_practico = generar_practico()
            ej = st.session_state.ejercicio_practico
            
            st.info(ej["p"])
            if ej["tipo"] == "input":
                resp = st.text_input("Escribe tu respuesta numérica aquí (sin comas ni signos):", key="ans_practico_in").strip().lower()
            else:
                resp = st.radio("Selecciona la mejor opción de Speech Profesional:", ej["options"], key="ans_practico_rad")
        
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
