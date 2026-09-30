import os

from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


# -----------------------------
# Gemini configuration
# -----------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


# -----------------------------
# Optional local explanation
# -----------------------------

LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
).strip()


USE_LOCAL_EXPLANATION = (
    os.getenv(
        "USE_LOCAL_EXPLANATION",
        "false"
    ).lower()
    == "true"
)


# -----------------------------
# Application configuration
# -----------------------------

APP_ENV = os.getenv(
    "APP_ENV",
    "development"
)


MAX_INPUT_CHARS = int(
    os.getenv(
        "MAX_INPUT_CHARS",
        "12000"
    )
)


# -----------------------------
# Gemini client
# -----------------------------

@lru_cache(maxsize=1)
def get_gemini_client():

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please create a .env file and add your Gemini API key."
        )

    from google import genai

    return genai.Client(
        api_key=GEMINI_API_KEY
    )