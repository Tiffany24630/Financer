import pandas as pd

MAX_FILE_SIZE_MB = 10

def validate_file(uploaded_file):

    if uploaded_file is None:
        return False, "No se seleccionó archivo"

    size = uploaded_file.size / (1024 * 1024)

    if size > MAX_FILE_SIZE_MB:
        return False, "Archivo demasiado grande"

    return True, "Archivo válido"


def validate_dataframe(df):

    if df.empty:
        return False, "El archivo está vacío"

    if len(df.columns) < 2:
        return False, "Muy pocas columnas"

    return True, "Datos válidos"