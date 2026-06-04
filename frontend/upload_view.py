import streamlit as st

def render_upload():
    uploaded_file = st.file_uploader(
        "Sube tu archivo Excel con registros contables",
        type=["xlsx", "xls"]
    )

    return uploaded_file