"""
learning_path.py
------------------
Generates a personalized, structured learning path (beginner -> advanced)
for any topic the learner names, using Gemini.
"""

from gemini_config import get_model


def get_learning_recommendations(topic: str) -> str:
    try:
        model = get_model()

        prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics,
order of learning, and useful resources (videos, articles, or books).
Include beginner, intermediate, and advanced levels if needed.
Keep it well organized with clear headings and bullet points.
"""
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text
        elif hasattr(response, "parts") and response.parts:
            return response.parts[0].text
        else:
            return "❌ Could not extract content from Gemini response."

    except Exception as e:
        return f"❌ Error occurred: {e}"
