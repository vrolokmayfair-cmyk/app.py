import pandas as pd

def cargar_base_tipificaciones(filepath='Copia de Tipificaciones V6 (1).xlsx'):
    """
    Carga las hojas existentes del libro de Excel original.
    """
    xls = pd.ExcelFile(filepath)
    hojas = {}
    for sheet_name in xls.sheet_names:
        hojas[sheet_name] = pd.read_excel(filepath, sheet_name=sheet_name)
    return hojas


# ==========================================
# MÓDULO 1: SCRIPTS Y ROLEPLAY (INTEGRADO)
# ==========================================
SCRIPTS_ROLEPLAY = {
    "Script_A_Apertura_y_Objeciones": {
        "ejecutivo_inicio": (
            "Hola, muy buenas tardes, ¿hablo con el Titular [Nombre del Cliente]? "
            "Le llamo de la financiera respecto a su crédito autorizado con descuento por nómina/pensión."
        ),
        "cliente_objecion": "Ahorita no me interesa / No tengo tiempo / Ya tengo muchos préstamos.",
        "ejecutivo_respuesta": (
            "Comprendo perfectamente su tiempo, [Nombre del Cliente]. Precisamente por eso le llamo, "
            "porque su crédito ya cuenta con una tasa preferencial congelada del 31.89% y sin cargo de apertura ($0.00). "
            "No venimos a quitarle tiempo, sino a ofrecerle una liquidez inmediata o consolidación de deudas a su medida. "
            "¿Le parecería si en 2 minutos revisamos el monto quincenal que le correspondería sin compromiso?"
        ),
        "cliente_aceptacion": "¿Cuánto me podrían prestar y de a cómo me saldría la quincena?"
    },
    "Script_B_Cierre_y_Transferencia": {
        "ejecutivo_propuesta": (
            "Perfecto, [Nombre del Cliente], para el monto de $[Monto a financiar] a un plazo de [Plazo] meses, "
            "su pago quincenal queda exactamente en $[Pago quincenal] con un CAT del 37.0%. "
            "¿Le acomoda este descuento quincenal en su pensión/nómina?"
        ),
        "cliente_confirmacion": "Sí, me parece bien esa cantidad.",
        "ejecutivo_cierre": (
            "Excelente. Para formalizar y proceder con la liberación de su efectivo, voy a realizar la transferencia "
            "de su llamada con nuestro Ejecutivo de Validación en una conferencia tripartita. Por favor manténgase en la "
            "línea un momento mientras valido sus documentos en sistema. ¿Tiene a la mano su identificación y comprobante?"
        )
    }
}


# ==========================================
# MÓDULO 2: COTIZADOR 4918 IMSS PENSIONADOS
# ==========================================
PARAMETROS_COTIZADOR_4918 = {
    "Convenio": "OPC IMSS PENSIONADOS",
    "Cotizador": "OPC_IMSSPENS_EFEC_EPAG_MN_V006",
    "Material": 4918,
    "Codigo": "SIDN",
    "Cargo_Apertura_Fijo": 0.00,
    "Cargo_Apertura_Porcentaje": 0.00,
    "Tasa_Interes_Anual": 31.89,
    "CAT_Promedio": 37.0,
    "Frecuencia_Pago": "Quincenal",
    "Plazos_Meses": [60, 54, 48, 36, 24, 12]
}

# Tabla de Muestra Representativa del Material 4918
TABLA_COTIZACION_4918_DF = pd.DataFrame([
    {"Monto": 5000.00,   "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 183.89,   "54_Meses": 191.27,   "48_Meses": 200.93,   "36_Meses": 231.87,   "24_Meses": 297.88,   "12_Meses": 504.80},
    {"Monto": 10000.00,  "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 367.78,   "54_Meses": 382.53,   "48_Meses": 401.87,   "36_Meses": 463.73,   "24_Meses": 595.77,   "12_Meses": 1009.61},
    {"Monto": 20000.00,  "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 735.57,   "54_Meses": 765.06,   "48_Meses": 803.73,   "36_Meses": 927.46,   "24_Meses": 1191.54,  "12_Meses": 2019.22},
    {"Monto": 50000.00,  "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 1838.91,  "54_Meses": 1912.65,  "48_Meses": 2009.33,  "36_Meses": 2318.66,  "24_Meses": 2978.85,  "12_Meses": 5048.04},
    {"Monto": 100000.00, "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 3677.83,  "54_Meses": 3825.31,  "48_Meses": 4018.65,  "36_Meses": 4637.31,  "24_Meses": 5957.69,  "12_Meses": 10096.08},
    {"Monto": 150000.00, "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 5516.74,  "54_Meses": 5737.96,  "48_Meses": 6027.98,  "36_Meses": 6955.97,  "24_Meses": 8936.54,  "12_Meses": 15144.12},
    {"Monto": 200000.00, "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 7355.66,  "54_Meses": 7650.61,  "48_Meses": 8037.31,  "36_Meses": 9274.63,  "24_Meses": 11915.38, "12_Meses": 20192.15},
    {"Monto": 250000.00, "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 9194.57,  "54_Meses": 9563.26,  "48_Meses": 10046.63, "36_Meses": 11593.29, "24_Meses": 14894.23, "12_Meses": 25240.19},
    {"Monto": 300000.00, "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 11033.48, "54_Meses": 11475.92, "48_Meses": 12055.96, "36_Meses": 13911.94, "24_Meses": 17873.07, "12_Meses": 30288.23},
    {"Monto": 365000.00, "Tasa_%": 31.89, "CAT_%": 37.0, "60_Meses": 13424.07, "54_Meses": 13962.36, "48_Meses": 14668.08, "36_Meses": 16903.01, "24_Meses": 21715.78, "12_Meses": 36800.20}
])


# ==========================================
# EXPORTACIÓN E INTEGRACIÓN A EXCEL COMPLETO
# ==========================================
def guardar_sistema_actualizado(filepath_original='Copia de Tipificaciones V6 (1).xlsx',
                                filepath_salida='Tipificaciones_Con_Cotizador_y_Roleplay.xlsx'):
    """
    Consolida las hojas originales y añade las nuevas pestañas de Cotizador y Roleplay.
    """
    hojas_existentes = cargar_base_tipificaciones(filepath_original)

    with pd.ExcelWriter(filepath_salida, engine='openpyxl') as writer:
        # 1. Copiar hojas originales exactamente como están
        for nombre_hoja, df_hoja in hojas_existentes.items():
            df_hoja.to_excel(writer, sheet_name=nombre_hoja, index=False)
        
        # 2. Agregar nueva pestaña de Cotizador (Material 4918)
        TABLA_COTIZACION_4918_DF.to_excel(writer, sheet_name='Cotizador 4918 IMSS', index=False)

        # 3. Agregar nueva pestaña de Roleplay & Scripts
        scripts_rows = []
        for script_name, dialogo in SCRIPTS_ROLEPLAY.items():
            for rol, texto in dialogo.items():
                scripts_rows.append({"Módulo": script_name, "Rol/Paso": rol, "Diálogo": texto})
        
        pd.DataFrame(scripts_rows).to_excel(writer, sheet_name='Roleplay & Scripts', index=False)

    print(f"Archivo generado exitosamente en: {filepath_salida}")

if __name__ == '__main__':
    # Ejemplo de ejecución para generar el archivo Excel integrado
    guardar_sistema_actualizado()
