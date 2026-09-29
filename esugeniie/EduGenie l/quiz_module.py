"""
quiz_module.py
---------------
Generates 3 multiple-choice questions (4 options each) from a topic or
passage of text, using Gemini. Output is parsed into a Python list of
dicts: [{"question": ..., "options": [...], "answer": ...}, ...]
"""

import json
import re

from gemini_config import get_model


def clean_json_block(text: str) -> str:
    """Strip ```json ... ``` markdown fences if Gemini adds them."""
    return re.sub(r"```(?:json)?\n?(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    try:
        model = get_model()

        prompt = f"""
You are a quiz generator.

From the following passage or topic, create 3 multiple-choice questions.
Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, and return ONLY the JSON array,
with no extra commentary, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage / Topic:
{text}
"""
        response = model.generate_content(prompt)
        quiz_text = response.text.strip()

        # Clean markdown code blocks if any
        cleaned_text = clean_json_block(quiz_text)

        quiz_data = json.loads(cleaned_text)

        # Basic validation so the frontend never breaks on malformed data
        valid_quiz = []
        for q in quiz_data:
            if (
                isinstance(q, dict)
                and "question" in q
                and "options" in q
                and "answer" in q
                and isinstance(q["options"], list)
                and len(q["options"]) >= 2
            ):
                valid_quiz.append(q)

        if not valid_quiz:
            raise ValueError("No valid questions parsed from model response.")

        return valid_quiz

    except json.JSONDecodeError as e:
        return [{"error": f"Failed to parse quiz JSON: {e}"}]
    except Exception as e:
        return [{"error": f"Error generating quiz: {e}"}]
