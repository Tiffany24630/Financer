import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


@lru_cache(maxsize=1)
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Configura OPENAI_API_KEY en el archivo .env para usar las funciones de IA."
        )

    return OpenAI(api_key=api_key)
