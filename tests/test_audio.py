from io import BytesIO
import wave

import pytest

from ia.speech_service import (
    audio_to_bytes,
    audio_to_openai_file,
    describe_audio,
    get_audio_duration_seconds,
    get_audio_mime_type,
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
