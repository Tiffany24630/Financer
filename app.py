import streamlit as st
from dotenv import load_dotenv

from frontend.upload_view import render_upload
from frontend.dashboard import render_dashboard
from frontend.voice_view import render_voice_recorder

from backend.validations import (
    validate_file,
    validate_dataframe
)

from backend.excel_processor import (
    read_excel,
    dataframe_to_text
)

from ia.openai_service import (
    analyze_financial_data,
    ask_assistant
)

from ia.speech_service import (
    audio_to_bytes,
    describe_audio,
    generate_speech,
    get_audio_duration_seconds,
    get_audio_mime_type,
    transcribe_audio
)

load_dotenv()

st.set_page_config(
    page_title="FinancerAI",
    layout="wide"
)

st.title("FinancerAI")

excel_text = ""

# -------------------------
# EXCEL
# -------------------------

uploaded_file = render_upload()

if uploaded_file:

    valid, message = validate_file(uploaded_file)

    if not valid:
        st.error(message)
        st.stop()

    df = read_excel(uploaded_file)

    valid, message = validate_dataframe(df)

    if not valid:
        st.error(message)
        st.stop()

    render_dashboard(df)

    excel_text = dataframe_to_text(df)

    if st.button(
        "Analizar registros con IA",
        use_container_width=True
    ):

        with st.spinner("Analizando..."):

            result = analyze_financial_data(
                excel_text
            )

            st.subheader(
                "Resultado del análisis"
            )

            st.markdown(result)

# -------------------------
# VOZ
# -------------------------

st.markdown("---")

st.header("Chat de Voz")

if "history" not in st.session_state:
    st.session_state.history = []

if "voice_recorder_version" not in st.session_state:
    st.session_state.voice_recorder_version = 0

recorder_key = f"voice_recorder_{st.session_state.voice_recorder_version}"

audio = render_voice_recorder(key=recorder_key)

if audio:
    audio_info = describe_audio(audio)

    if audio_info["valid"]:
        st.success(
            "Audio detectado correctamente"
        )
    else:
        st.warning(audio_info["error"])

    try:
        st.audio(
            audio_to_bytes(audio),
            format=get_audio_mime_type(audio)
        )
    except (TypeError, ValueError) as e:
        st.warning(str(e))

    duration_seconds = get_audio_duration_seconds(audio)

    if duration_seconds is not None:
        st.write(
            f"Duración: {duration_seconds:.2f} segundos"
        )

    process_col, reset_col = st.columns(2)

    with process_col:
        process_audio = st.button(
            "Procesar audio",
            use_container_width=True,
            disabled=not audio_info["valid"],
            key=f"process_audio_{recorder_key}"
        )

    with reset_col:
        reset_audio = st.button(
            "Volver a grabar",
            use_container_width=True,
            key=f"reset_audio_{recorder_key}"
        )

    if reset_audio:
        st.session_state.voice_recorder_version += 1
        st.rerun()

    if process_audio:

        with st.spinner(
            "Transcribiendo..."
        ):

            try:

                if not audio_info["valid"]:
                    raise ValueError(audio_info["error"])

                question = transcribe_audio(
                    audio
                )

                st.subheader(
                    "Transcripción"
                )

                st.write(question)

                answer = ask_assistant(
                    question,
                    excel_text
                )

                st.subheader(
                    "Respuesta"
                )

                st.markdown(answer)

                st.session_state.history.append(
                    {
                        "pregunta": question,
                        "respuesta": answer
                    }
                )

                audio_b64 = generate_speech(
                    answer
                )

                html = f"""
                <audio autoplay controls>
                    <source
                    src="data:audio/mp3;base64,{audio_b64}"
                    type="audio/mpeg">
                </audio>
                """

                st.markdown(
                    html,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(str(e))

# -------------------------
# HISTORIAL
# -------------------------

if st.session_state.history:

    st.markdown("---")

    st.subheader(
        "Historial"
    )

    for item in reversed(
        st.session_state.history
    ):

        with st.chat_message("user"):
            st.write(item["pregunta"])

        with st.chat_message("assistant"):
            st.write(item["respuesta"])
