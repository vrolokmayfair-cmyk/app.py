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

    item = random.
