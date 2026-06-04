import streamlit as st
from streamlit_mic_recorder import mic_recorder


def render_voice_recorder(key="voice_recorder"):
    mode = st.radio(
        "Grabador",
        ["Principal", "Alternativo"],
        horizontal=True,
        key=f"{key}_mode",
        label_visibility="collapsed"
    )

    if mode == "Alternativo":
        return st.audio_input(
            "Grabar consulta de voz",
            sample_rate=16000,
            key=f"{key}_native",
            width="stretch"
        )

    return mic_recorder(
        start_prompt="Grabar",
        stop_prompt="Detener",
        just_once=False,
        use_container_width=True,
        format="wav",
        key=f"{key}_component"
    )
