"""
qna.py
------
Handles general knowledge / academic question answering using Gemini 1.5 Pro.
"""

from gemini_config import get_model


def answer_question_with_gemini(question: str) -> str:
    try:
        model = get_model()
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in QnA: {e}"
