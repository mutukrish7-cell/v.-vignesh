"""
gemini_config.py
-----------------
Central place that loads the Google Gemini API key and configures the
google-generativeai SDK. Every module that needs Gemini imports `genai`
and `GEMINI_MODEL_NAME` from here instead of configuring the SDK itself.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load variables from a .env file placed in the project root
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model name used across the app. You can override it in .env with
# GEMINI_MODEL_NAME=models/gemini-1.5-flash (cheaper/faster) if you like.
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-1.5-pro")

_configured = False


def configure_gemini():
    """Configure the Gemini SDK once. Safe to call multiple times."""
    global _configured
    if _configured:
        return
    if not GEMINI_API_KEY:
        # We don't raise here so the server can still start (e.g. so you
        # can explore the frontend UI) — the individual endpoints will
        # return a clear error message instead of crashing the app.
        print(
            "⚠️  WARNING: GEMINI_API_KEY is not set. Create a .env file "
            "(see .env.example) and add your key, otherwise AI-powered "
            "endpoints will return an error."
        )
        return
    genai.configure(api_key=GEMINI_API_KEY)
    _configured = True


def get_model(model_name: str = None):
    """Return a ready-to-use GenerativeModel instance."""
    configure_gemini()
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file to use "
            "this feature."
        )
    return genai.GenerativeModel(model_name=model_name or GEMINI_MODEL_NAME)
