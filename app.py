# --- TAB 2: ROLEPLAY MODELO B (ACTUALIZADO) ---
    with tabs[1]:
        st.subheader("🎙️ Entrenamiento de Guion: Modelo B")
        st.markdown("""
        **Instrucciones:** Redacta la llamada completa. El sistema detectará automáticamente los 8 pilares.
        """)
        
        respuesta_rp = st.text_area("Escribe tu modelo de llamada aquí:", height=300, 
                                   placeholder="Ej: Buen día, le habla [Nombre] de Consubanco...")
        
        if st.button("Calificar Modelo B"):
            # DICCIONARIO OPTIMIZADO PARA DETECTAR VARIACIONES NATURALES
            puntos_clave = {
                "1. Presentación": ["hola", "buen", "día", "tarde", "noche", "nombre es", "habla", "consubanco", "servidor"],
                "2. Monto": ["$", "monto", "cantidad", "crédito de", "suma de", "70000", "70,000", "setenta mil"],
                "3. Plazo": ["meses", "plazo", "pagar en", "periodo", "60", "sesenta"],
                "4. Descuento": ["nómina", "descuento", "pensión", "directo", "automático", "retención"],
                "5. Requisitos": ["ine", "identificación", "talón", "comprobante", "correo", "documentos", "fotos", "whatsapp"],
                "6. Forma de Pago": ["saldos insolutos", "interés", "capital", "fijo", "disminuye", "pago mensual"],
                "7. Tiempo Depósito": ["depósito", "transferencia", "horas", "hrs", "días", "hábil", "disponible", "24", "48", "72"],
                "8. Cierre de Venta": ["trámite", "iniciar", "comenzamos", "procedemos", "autoriza", "cerramos", "le parece bien", "acuerdo", "firma", "inmediato"]
            }
            
            validos = 0
            resumen = []
            texto_usuario = respuesta_rp.lower()
            
            for punto, keywords in puntos_clave.items():
                # Verificamos si alguna palabra clave existe en el texto
                encontrado = any(k in texto_usuario for k in keywords)
                
                if encontrado:
                    resumen.append(f"✅ **{punto}**")
                    validos += 1
                else:
                    resumen.append(f"❌ **{punto}**")
            
            st.write("### Validación de Estructura Modelo B")
            c1, c2 = st.columns(2)
            for i, item in enumerate(resumen):
                if i < 4: c1.write(item)
                else: c2.write(item)
            
            calif_rp = (validos / 8) * 10
            
            if calif_rp == 10:
                st.balloons()
                st.success(f"Calificación: {calif_rp}/10 - ¡Excelente! Estructura Completa.")
            elif calif_rp >= 8:
                st.warning(f"Calificación: {calif_rp}/10 - Muy bien, pero faltan detalles mínimos.")
            else:
                st.error(f"Calificación: {calif_rp}/10 - Es necesario incluir más elementos de la estructura oficial.")

            # Guardar resultado del Roleplay en la DB
            nuevo_log_rp = {
                "Nombre": nombre_usuario, "Nivel": "Roleplay", "Calificación": calif_rp,
                "Intentos": intentos + 1, "Rango": rango, "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo_log_rp])], ignore_index=True)