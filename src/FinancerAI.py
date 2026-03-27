import streamlit as st
import openai
import pandas as pd
import os
from dotenv import load_dotenv
from io import BytesIO

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="FinancerAI - Asistente de Impuestos",
    layout="wide"
)

st.title("FinancerAI - Asistente de Impuestos")

# Área principal
uploaded_file = st.file_uploader(
    "Sube tu archivo Excel con registros contables", 
    type=["xlsx", "xls"]
)

if uploaded_file:
    st.success("Archivo cargado exitosamente")
    
    try:
        # Leer el archivo Excel
        excel_file = pd.read_excel(uploaded_file)
        
        # Mostrar preview de los datos
        st.subheader("📊 Vista previa de los datos")
        st.dataframe(excel_file, use_container_width=True)
        
        st.markdown("---")
        
        # Mostrar información del archivo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de registros", len(excel_file))
        with col2:
            st.metric("Total de columnas", len(excel_file.columns))
        with col3:
            st.metric("Columnas", ", ".join(excel_file.columns.tolist()))
        
        st.markdown("---")
        
        # Convertir datos a texto para enviar a OpenAI
        excel_text = excel_file.to_string()
        
        # Botón para analizar
        if st.button("Analizar registros contables con IA", use_container_width=True):
            with st.spinner("Analizando registros contables..."):
                try:
                    # Prepare el prompt para OpenAI
                    prompt = f"""Eres un experto contador guatemalteco especializado en impuestos SAT (Superintendencia de Administración Tributaria).

                        Has recibido los siguientes registros contables de una empresa:

                        {excel_text}

                        Por favor, realiza un análisis detallado que incluya:
                        1. Resumen general de ingresos y egresos
                        2. Identificación de transacciones importantes
                        3. Cálculo estimado de impuestos (ISR, IVA) según requisitos SAT Guatemala
                        4. Recomendaciones de cumplimiento fiscal
                        5. Clasificación de gastos deducibles
                        6. Alertas sobre posibles incumplimientos fiscales

                        Proporciona un análisis estructurado y profesional."""

                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "Eres un asistente experto en contabilidad y impuestos para Guatemala, especializado en normativas SAT."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                    
                    # Mostrar resultado del análisis
                    st.subheader("Análisis de Registros Contables")
                    st.markdown(response.choices[0].message.content)
                    
                    # Opción para descargar el análisis
                    analysis_text = response.choices[0].message.content
                    
                except Exception as e:
                    st.error(f"Error al generar el análisis: {e}")
                    st.warning(
                        "Asegurate de que:\n"
                        "- La clave API de OpenAI es correcta\n"
                        "- Tienes acceso al modelo GPT-4o\n"
                        "- La conexión a internet es estable"
                    )
        
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        st.info("Por favor, asegurate que el archivo está en formato Excel (.xlsx o .xls)")

else:
    st.info("Sube un archivo Excel con tus registros contables para comenzar el análisis")

