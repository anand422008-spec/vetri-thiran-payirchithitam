from typing import Type, TypeVar

from pydantic import BaseModel

from google.genai import types

from config import (
    GEMINI_MODEL,
    get_gemini_client,
)


T = TypeVar(
    "T",
    bound=BaseModel
)


# =====================================================
# Normal text generation
# =====================================================

def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    client = get_gemini_client()


    config_kwargs = {

        "temperature": temperature,

        "max_output_tokens":
            max_output_tokens,

    }


    if system_instruction:

        config_kwargs[
            "system_instruction"
        ] = system_instruction


    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(
            **config_kwargs
        ),
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


# =====================================================
# Structured JSON generation
# =====================================================

def generate_structured(
    prompt: str,
    schema: Type[T],
    *,
    system_instruction: str | None = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1800,
) -> T:

    client = get_gemini_client()


    config_kwargs = {

        "temperature": temperature,

        "max_output_tokens":
            max_output_tokens,

        "response_mime_type":
            "application/json",

        "response_schema":
            schema,

    }


    if system_instruction:

        config_kwargs[
            "system_instruction"
        ] = system_instruction


    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(
            **config_kwargs
        ),
    )


    text = getattr(
        response,
        "text",
        None
    )


    if not text:

        raise RuntimeError(
            "Gemini returned an empty structured response."
        )


    try:

        return schema.model_validate_json(
            text
        )

    except Exception as exc:

        raise RuntimeError(
            "Gemini returned invalid JSON: "
            f"{exc}"
        ) from exc