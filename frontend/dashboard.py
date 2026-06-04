import streamlit as st

def render_dashboard(df):

    st.subheader("Vista previa de datos")

    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registros", len(df))

    with col2:
        st.metric("Columnas", len(df.columns))

    with col3:
        st.metric("Valores nulos", df.isnull().sum().sum())