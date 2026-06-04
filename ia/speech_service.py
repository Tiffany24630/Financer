import base64
import os
import wave
from io import BytesIO

from ia.openai_client import get_openai_client

AUDIO_MIME_TYPES = {
    "wav": "audio/wav",
    "wave": "audio/wav",
    "webm": "audio/webm",
    "mp3": "audio/mpeg",
    "mpeg": "audio/mpeg",
    "mp4": "audio/mp4",
    "m4a": "audio/mp4",
    "ogg": "audio/ogg",
}

DEFAULT_AUDIO_FORMAT = "wav"
MIN_AUDIO_BYTES = 512


def get_audio_format(audio):
    if isinstance(audio, dict):
        audio_format = audio.get("format") or DEFAULT_AUDIO_FORMAT
    elif hasattr(audio, "type") and getattr(audio, "type"):
        audio_format = getattr(audio, "type")
    elif hasattr(audio, "name") and getattr(audio, "name"):
        _, extension = os.path.splitext(getattr(audio, "name"))
        audio_format = extension or DEFAULT_AUDIO_FORMAT
    else:
        audio_format = DEFAULT_AUDIO_FORMAT

    audio_format = str(audio_format).lower().strip().lstrip(".")

    if "/" in audio_format:
        audio_format = audio_format.split("/")[-1]

    if audio_format == "x-wav":
        return "wav"
    if audio_format == "mpeg":
        return "mp3"

    return audio_format or DEFAULT_AUDIO_FORMAT


def get_audio_mime_type(audio):
    if hasattr(audio, "type") and getattr(audio, "type"):
        return getattr(audio, "type")

    return AUDIO_MIME_TYPES.get(
        get_audio_format(audio),
        "application/octet-stream"
    )


def audio_to_bytes(audio):
    if audio is None:
        raise ValueError("No se recibio audio para procesar.")

    if isinstance(audio, dict):
        audio_bytes = audio.get("bytes")
    elif isinstance(audio, (bytes, bytearray, memoryview)):
        audio_bytes = bytes(audio)
    elif hasattr(audio, "getvalue"):
        audio_bytes = audio.getvalue()
    elif hasattr(audio, "read"):
        try:
            audio.seek(0)
        except (AttributeError, OSError):
            pass

        audio_bytes = audio.read()

        try:
            audio.seek(0)
        except (AttributeError, OSError):
            pass
    elif hasattr(audio, "export"):
        buffer = BytesIO()
        audio.export(out_f=buffer, format=DEFAULT_AUDIO_FORMAT)
        buffer.seek(0)
        audio_bytes = buffer.getvalue()
    else:
        raise TypeError(
            "Formato de audio no soportado. Graba audio desde el componente de voz."
        )

    if not audio_bytes:
        raise ValueError("La grabacion de audio esta vacia.")

    if len(audio_bytes) < MIN_AUDIO_BYTES:
        raise ValueError(
            "La grabacion es demasiado corta. Graba de nuevo hablando cerca del microfono."
        )

    return bytes(audio_bytes)


def audio_to_openai_file(audio):
    audio_bytes = audio_to_bytes(audio)
    audio_format = get_audio_format(audio)
    filename = getattr(audio, "name", None) or f"audio.{audio_format}"

    if "." not in os.path.basename(filename):
        filename = f"{filename}.{audio_format}"

    return (
        filename,
        BytesIO(audio_bytes),
        get_audio_mime_type(audio)
    )


def get_audio_duration_seconds(audio):
    try:
        audio_bytes = audio_to_bytes(audio)
    except (TypeError, ValueError):
        return None

    if get_audio_format(audio) in {"wav", "wave"}:
        try:
            with wave.open(BytesIO(audio_bytes), "rb") as wav_file:
                frame_rate = wav_file.getframerate()

                if frame_rate:
                    return wav_file.getnframes() / float(frame_rate)
        except (EOFError, wave.Error):
            pass

    return None


def describe_audio(audio):
    try:
        audio_bytes = audio_to_bytes(audio)
    except (TypeError, ValueError) as e:
        return {
            "valid": False,
            "error": str(e),
            "bytes": 0,
            "format": get_audio_format(audio),
            "mime_type": get_audio_mime_type(audio),
            "duration_seconds": None,
        }

    return {
        "valid": True,
        "error": "",
        "bytes": len(audio_bytes),
        "format": get_audio_format(audio),
        "mime_type": get_audio_mime_type(audio),
        "duration_seconds": get_audio_duration_seconds(audio),
    }


def transcribe_audio(audio, language="es"):
    audio_info = describe_audio(audio)

    if not audio_info["valid"]:
        raise ValueError(audio_info["error"])

    transcript = get_openai_client().audio.transcriptions.create(
        model="whisper-1",
        file=audio_to_openai_file(audio),
        language=language
    )

    if isinstance(transcript, str):
        text = transcript
    else:
        text = getattr(transcript, "text", "")

    text = text.strip()

    if not text:
        raise RuntimeError("No se pudo transcribir el audio. Intenta grabar de nuevo.")

    return text


def generate_speech(text):
    text = str(text or "").strip()

    if not text:
        raise ValueError("No hay texto para convertir a audio.")

    speech = get_openai_client().audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
        response_format="mp3"
    )

    content = getattr(speech, "content", None)

    if content is None:
        content = speech.read()

    return base64.b64encode(
        content
    ).decode()
