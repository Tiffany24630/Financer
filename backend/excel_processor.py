import pandas as pd

def read_excel(uploaded_file):

    return pd.read_excel(uploaded_file)


def dataframe_to_text(df):

    return df.to_string()


def get_summary(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "null_values": int(df.isnull().sum().sum())
    }