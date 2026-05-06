# --- LÓGICA DE EJERCICIOS EXPANDIDA (MÁS TEMAS Y PREGUNTAS) ---
def generar_teoria():
    # Banco de preguntas expandido para cubrir todos los temas del glosario
    banco_preguntas = [
        # Tema: Saldos Insolutos
        {
            "p": "¿Cómo se llama el esquema donde el interés se cobra solo sobre el capital pendiente?", 
            "c": ["insoluto", "saldos insolutos", "saldo insoluto"], 
            "r": "Retroalimentación: Los saldos insolutos permiten ahorrar intereses al liquidar antes. ¡Es un gran gancho de venta!"
        },
        # Tema: CAT
        {
            "p": "¿Qué siglas representan el Costo Anual Total que incluye seguros y comisiones?", 
            "c": ["cat"], 
            "r": "Retroalimentación: El CAT es la medida estándar para comparar el costo real entre distintas financieras."
        },
        # Tema: SIPRE
        {
            "p": "¿Cuál es el nombre del portal donde validamos la capacidad de pago de un pensionado IMSS?", 
            "c": ["sipre"], 
            "r": "Retroalimentación: El SIPRE nos dice exactamente cuánto podemos descontar sin afectar al cliente."
        },
        # Tema: Tasa Fija
        {
            "p": "¿Cómo se le llama a la tasa que garantiza que el descuento mensual no subirá nunca?", 
            "c": ["tasa fija", "fija"], 
            "r": "Retroalimentación: La tasa fija brinda seguridad al cliente ante la inflación o crisis económicas."
        },
        # Tema: Capital
        {
            "p": "¿Cómo se le denomina al monto neto o 'dinero real' que el cliente recibe en su cuenta?", 
            "c": ["capital"], 
            "r": "Retroalimentación: Cada abono a capital reduce la deuda base del cliente."
        },
        # Tema: Requisitos
        {
            "p": "¿Qué documento oficial vigente es indispensable para iniciar cualquier trámite?", 
            "c": ["ine", "identificacion", "identificación"], 
            "r": "Retroalimentación: Sin el INE vigente no podemos procesar la solicitud. Valídalo siempre al inicio."
        },
        # Tema: Interés Compuesto (Prevención)
        {
            "p": "En Consubanco, ¿cobramos intereses sobre intereses? (Sí/No)", 
            "c": ["no", "falso"], 
            "r": "Retroalimentación: Correcto. En Consubanco NO aplicamos interés compuesto (anatocismo), protegiendo al cliente."
        },
        # Tema: Tabla de Amortización
        {
            "p": "¿Cómo se llama el documento que muestra el desglose de cada pago mensual del cliente?", 
            "c": ["tabla de amortizacion", "tabla de amortización", "tabla"], 
            "r": "Retroalimentación: La tabla de amortización da transparencia total sobre cuántos pagos faltan y qué incluyen."
        }
    ]
    return random.choice(banco_preguntas)

# --- EL RESTO DE LA LÓGICA DE VALIDACIÓN SE MANTIENE IGUAL ---
# (Asegúrate de que la validación use: 'resp in ej["c"]')