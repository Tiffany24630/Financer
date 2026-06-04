from ia.openai_client import get_openai_client


def analyze_financial_data(excel_text):

    prompt = f"""
Eres un contador experto en Guatemala.

Analiza los siguientes registros:

{excel_text}

Genera:

1. Resumen financiero
2. ISR estimado
3. IVA estimado
4. Riesgos fiscales
5. Recomendaciones
"""

    response = get_openai_client().chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Eres un contador experto en Guatemala."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content or ""


def ask_assistant(question, excel_context=""):

    prompt = f"""
Contexto financiero:

{excel_context}

Pregunta:

{question}
"""

    response = get_openai_client().chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Eres un contador experto en Guatemala."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content or ""
