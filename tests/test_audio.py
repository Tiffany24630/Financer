import base64
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import wave
import pytest
from ia.speech_service import (
    audio_to_bytes,
    audio_to_openai_file,
    describe_audio,
    generate_speech,
    get_audio_duration_seconds,
    get_audio_mime_type,
    transcribe_audio,
)

class FakeUploadedAudio:
    name = "audio.wav"
    type = "audio/wav"

    def __init__(self, audio_bytes):
        self._audio_bytes = audio_bytes

    def getvalue(self):
        return self._audio_bytes

def build_wav_bytes(duration_seconds=0.1, sample_rate=8000):
    buffer = BytesIO()
    frame_count = int(duration_seconds * sample_rate)

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"\0\0" * frame_count)

    return buffer.getvalue()

def test_mic_recorder_payload_is_supported():
    wav_bytes = build_wav_bytes()
    audio = {
        "bytes": wav_bytes,
        "format": "wav",
        "sample_rate": 8000,
        "sample_width": 2,
        "id": 1,
    }

    assert audio_to_bytes(audio) == wav_bytes
    assert get_audio_mime_type(audio) == "audio/wav"

def test_audio_to_openai_file_uses_recorder_metadata():
    wav_bytes = build_wav_bytes()
    audio_file = audio_to_openai_file({
        "bytes": wav_bytes,
        "format": "wav",
    })

    filename, file_obj, mime_type = audio_file

    assert filename == "audio.wav"
    assert file_obj.read() == wav_bytes
    assert mime_type == "audio/wav"

def test_audio_to_openai_file_supports_webm():
    webm_bytes = b"webm-bytes" * 80

    audio_file = audio_to_openai_file({
        "bytes": webm_bytes,
        "format": "webm",
    })

    filename, file_obj, mime_type = audio_file

    assert filename == "audio.webm"
    assert file_obj.read() == webm_bytes
    assert mime_type == "audio/webm"

def test_streamlit_audio_input_file_is_supported():
    wav_bytes = build_wav_bytes()
    audio = FakeUploadedAudio(wav_bytes)

    filename, file_obj, mime_type = audio_to_openai_file(audio)

    assert audio_to_bytes(audio) == wav_bytes
    assert filename == "audio.wav"
    assert file_obj.read() == wav_bytes
    assert mime_type == "audio/wav"

def test_audio_duration_reads_wav_header():
    audio = {
        "bytes": build_wav_bytes(duration_seconds=0.25),
        "format": "wav",
    }

    assert get_audio_duration_seconds(audio) == pytest.approx(0.25)

def test_describe_audio_reports_valid_metadata():
    audio = {
        "bytes": build_wav_bytes(duration_seconds=0.25),
        "format": "wav",
    }

    info = describe_audio(audio)

    assert info["valid"] is True
    assert info["bytes"] > 512
    assert info["format"] == "wav"
    assert info["mime_type"] == "audio/wav"
    assert info["duration_seconds"] == pytest.approx(0.25)

def test_short_audio_raises_clear_error():
    with pytest.raises(ValueError, match="demasiado corta"):
        audio_to_bytes({"bytes": b"tiny", "format": "wav"})

def test_empty_audio_raises_clear_error():
    with pytest.raises(ValueError, match="vacia"):
        audio_to_bytes({"bytes": b"", "format": "wav"})

def test_transcribe_audio_uses_whisper_api_and_returns_trimmed_text():
    audio = {
        "bytes": build_wav_bytes(duration_seconds=0.25),
        "format": "wav",
    }
    client = MagicMock()
    client.audio.transcriptions.create.return_value = SimpleNamespace(
        text="  consulta transcrita  "
    )

    with patch("ia.speech_service.get_openai_client", return_value=client):
        result = transcribe_audio(audio, language="es")

    assert result == "consulta transcrita"
    request = client.audio.transcriptions.create.call_args.kwargs
    assert request["model"] == "whisper-1"
    assert request["language"] == "es"

    filename, file_obj, mime_type = request["file"]
    assert filename == "audio.wav"
    assert file_obj.read() == audio["bytes"]
    assert mime_type == "audio/wav"

def test_transcribe_audio_accepts_string_response():
    audio = {
        "bytes": build_wav_bytes(duration_seconds=0.25),
        "format": "wav",
    }
    client = MagicMock()
    client.audio.transcriptions.create.return_value = "  texto directo  "

    with patch("ia.speech_service.get_openai_client", return_value=client):
        assert transcribe_audio(audio) == "texto directo"

def test_transcribe_audio_rejects_empty_transcription():
    audio = {
        "bytes": build_wav_bytes(duration_seconds=0.25),
        "format": "wav",
    }
    client = MagicMock()
    client.audio.transcriptions.create.return_value = SimpleNamespace(text=" ")

    with patch("ia.speech_service.get_openai_client", return_value=client):
        with pytest.raises(RuntimeError, match="No se pudo transcribir"):
            transcribe_audio(audio)

def test_transcribe_audio_rejects_invalid_audio_before_api_call():
    client = MagicMock()

    with patch("ia.speech_service.get_openai_client", return_value=client):
        with pytest.raises(ValueError, match="demasiado corta"):
            transcribe_audio({"bytes": b"tiny", "format": "wav"})

    client.audio.transcriptions.create.assert_not_called()

def test_generate_speech_uses_tts_api_and_returns_base64_audio():
    client = MagicMock()
    audio_content = b"fake-mp3-content"
    client.audio.speech.create.return_value = SimpleNamespace(
        content=audio_content
    )

    with patch("ia.speech_service.get_openai_client", return_value=client):
        result = generate_speech("  Respuesta de prueba  ")

    assert result == base64.b64encode(audio_content).decode()
    client.audio.speech.create.assert_called_once_with(
        model="tts-1",
        voice="nova",
        input="Respuesta de prueba",
        response_format="mp3",
    )

def test_generate_speech_reads_response_without_content_attribute():
    client = MagicMock()
    speech_response = MagicMock(spec=["read"])
    speech_response.read.return_value = b"audio-from-reader"
    client.audio.speech.create.return_value = speech_response

    with patch("ia.speech_service.get_openai_client", return_value=client):
        result = generate_speech("Respuesta")

    assert result == base64.b64encode(b"audio-from-reader").decode()
    speech_response.read.assert_called_once_with()

def test_generate_speech_rejects_empty_text_before_api_call():
    client = MagicMock()

    with patch("ia.speech_service.get_openai_client", return_value=client):
        with pytest.raises(ValueError, match="No hay texto"):
            generate_speech("  ")

    client.audio.speech.create.assert_not_called()