# FinancerAI

FinancerAI es una aplicación desarrollada con Streamlit que permite analizar información financiera contenida en archivos Excel mediante Inteligencia Artificial. Además, incorpora un asistente de voz capaz de responder preguntas relacionadas con los datos cargados utilizando modelos de OpenAI.

## Características

### Gestión de archivos Excel

* Carga de archivos Excel.
* Validación básica de archivos.
* Lectura automática de datos mediante Pandas.
* Vista previa de registros.
* Estadísticas generales del conjunto de datos:

  * Número de registros.
  * Número de columnas.
  * Cantidad de valores nulos.

### Análisis financiero con IA

* Generación automática de:

  * Resumen financiero.
  * Estimación de ISR.
  * Estimación de IVA.
  * Identificación de riesgos fiscales.
  * Recomendaciones financieras.
* Contextualización basada en legislación y prácticas contables de Guatemala.

### Asistente de voz

* Grabación de preguntas mediante micrófono.
* Transcripción automática utilizando Whisper.
* Consulta de información financiera mediante lenguaje natural.
* Respuestas generadas por IA.
* Conversión de respuestas a voz mediante Text-to-Speech.
* Historial de conversaciones.

## Arquitectura del Proyecto

```text
ProyF/
│
├── app.py
│
├── backend/
│   ├── excel_processor.py
│   ├── tax_calculator.py
│   └── validations.py
│
├── frontend/
│   ├── dashboard.py
│   ├── upload_view.py
│   └── voice_view.py
│
├── ia/
│   ├── openai_client.py
│   ├── openai_service.py
│   ├── prompts.py
│   └── speech_service.py
│
├── tests/
│   ├── test_ai.py
│   ├── test_audio.py
│   └── test_excel.py
│
├── requirements.txt
└── .env
```

## Tecnologías Utilizadas

* Python 3
* Streamlit
* OpenAI API
* Pandas
* NumPy
* OpenPyXL
* Whisper
* Text-to-Speech (OpenAI)
* Pytest
* Python Dotenv

## Requisitos

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=tu_api_key
```

## Ejecución

Iniciar la aplicación con:

```bash
streamlit run app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

## Flujo de Uso

### 1. Cargar archivo Excel

El usuario selecciona un archivo Excel que contiene información financiera.

### 2. Validación

El sistema verifica:

* Que el archivo exista.
* Que el tamaño sea válido.
* Que contenga información.
* Que posea suficientes columnas para ser procesado.

### 3. Dashboard

Se muestra:

* Tabla de datos.
* Cantidad de registros.
* Cantidad de columnas.
* Valores faltantes.

### 4. Análisis Inteligente

Al presionar **Analizar registros con IA**, el sistema envía la información a OpenAI para generar un análisis financiero completo.

### 5. Chat de Voz

El usuario puede:

* Grabar una pregunta.
* Obtener una transcripción automática.
* Recibir una respuesta generada por IA.
* Escuchar la respuesta mediante audio sintetizado.

### 6. Historial

Las conversaciones quedan registradas durante la sesión actual para consulta posterior.

## Pruebas

Ejecutar todas las pruebas:

```bash
pytest
```

Ejecutar una prueba específica:

```bash
pytest tests/test_excel.py
```

## Seguridad

* La clave de OpenAI se almacena mediante variables de entorno.
* No se incluyen credenciales dentro del código fuente.
* Se realizan validaciones básicas sobre archivos y entradas de usuario.

## Posibles Mejoras Futuras

* Dashboard financiero avanzado con gráficos.
* Exportación de reportes PDF.
* Cálculo automático de impuestos basado en normativa SAT.
* Base de datos para almacenamiento histórico.
* Gestión de usuarios y autenticación.
* Integración con sistemas contables externos.
* Análisis predictivo financiero.
* Soporte para múltiples formatos de archivo.

## Autores

Proyecto desarrollado como herramienta de apoyo para análisis financiero asistido por Inteligencia Artificial y procesamiento de voz.
