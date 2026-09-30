import os
import json

from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

from dotenv import load_dotenv

load_dotenv()


MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


class GeminiConfigurationError(
    RuntimeError
):
    pass


@lru_cache(maxsize=1)
def get_client():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to .env"
        )

    return genai.Client(
        api_key=api_key
    )


def generate_text(
    prompt: str,
    temperature: float = 0.3
):

    client = get_client()

    response = client.models.generate_content(

        model=MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(
            temperature=temperature
        )
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


def generate_json(
    prompt: str,
    schema: dict
):

    client = get_client()

    response = client.models.generate_content(

        model=MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.2,

            response_mime_type="application/json",

            response_schema=schema
        )
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return json.loads(text)