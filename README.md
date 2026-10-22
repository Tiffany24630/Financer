# FinancerAI

FinancerAI is an AI-assisted financial data analysis application built with Python and Streamlit. It allows users to upload Excel files, inspect their data, generate financial insights with OpenAI, and interact with the loaded information through voice-based questions.

The project combines **data processing, AI integration, financial analysis, speech processing, and automated testing** in a single application.

## Features

### Financial data processing

- Upload Excel files.
- Validate uploaded files before processing.
- Read and process financial data using Pandas.
- Preview uploaded records.
- Display basic dataset statistics:
  - Number of records
  - Number of columns
  - Missing values

### AI-assisted financial analysis

The application can generate:

- Financial summaries
- ISR estimates
- IVA estimates
- Fiscal risk identification
- Financial recommendations

The analysis is contextualized using legislation and accounting practices from Guatemala.

### Voice assistant

FinancerAI also supports voice-based interaction with the financial data:

1. Record a question using a microphone.
2. Transcribe the question using Whisper.
3. Process the question using the loaded financial information.
4. Generate an AI response using OpenAI.
5. Convert the response to audio using Text-to-Speech.

Conversation history is available during the current application session.

---

## Architecture

```text
FinancerAI/
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

The project separates the main responsibilities into data processing, interface components, AI services, speech processing, and tests.

---

## Technology Stack

### Application

- Python 3
- Streamlit

### Data processing

- Pandas
- NumPy
- OpenPyXL

### AI and speech

- OpenAI API
- Whisper
- OpenAI Text-to-Speech

### Testing and configuration

- Pytest
- Python Dotenv

---

## How it works

### 1. Upload financial data

The user uploads an Excel file containing financial information.

### 2. Validate the file

The application checks that:

- The file exists.
- The file size is valid.
- The file contains data.
- The file contains enough columns to be processed.

### 3. Inspect the dataset

The dashboard displays the uploaded records and basic information about the dataset, including record count, column count, and missing values.

### 4. Generate an AI analysis

The user can request an AI-assisted analysis of the loaded records.

The application sends the relevant financial information to OpenAI and generates a structured financial analysis.

### 5. Ask questions using voice

The user can record a question instead of typing it.

```text
Voice input
    ↓
Whisper transcription
    ↓
Financial data + user question
    ↓
OpenAI analysis
    ↓
Generated response
    ↓
Text-to-Speech
    ↓
Audio response
```

---

## Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key
```

The API key is loaded through environment variables rather than being included directly in the source code.

> Do not commit your `.env` file or expose your API key.

---

## Running the application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Testing

Run the complete test suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_excel.py
```

The repository includes tests for:

- Excel processing
- AI functionality
- Audio functionality

---

## Project Structure

The application follows a modular structure:

- `backend/` — financial data processing, tax calculations, and validation.
- `frontend/` — Streamlit views and dashboard components.
- `ia/` — OpenAI integration, prompts, and speech services.
- `tests/` — automated tests for the main application components.

---

## Security

The project uses environment variables for the OpenAI API key instead of storing credentials directly in the source code.

Input files are also subject to basic validation before processing.

For production use, additional controls would be appropriate depending on the deployment environment and the sensitivity of the financial information being processed.

---

## Future Improvements

Possible extensions include:

- Advanced financial dashboards and visualizations.
- PDF report generation.
- Automated tax calculations based on SAT regulations.
- Persistent database storage.
- User authentication and account management.
- Integration with external accounting systems.
- Predictive financial analysis.
- Support for additional file formats.

---

## Contributors

This project was developed as a collaborative project by:

- Jefferson Calderón
- Tiffany Salazar
- Giancarlo
- Luis

---

## Project Focus

FinancerAI explores how AI can be combined with structured financial data and natural-language interaction to make financial information easier to analyze.

The project brings together several areas of software development:

**Data processing → AI integration → Voice interaction → Financial analysis → Automated testing**
