"""
summary_module.py
-------------------
Summarizes long educational passages into concise, easy-to-read text
using Gemini.
"""

from gemini_config import get_model


def summarize_text(text: str) -> str:
    try:
        model = get_model()
        prompt = f"Summarize the following text in simple language:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"
