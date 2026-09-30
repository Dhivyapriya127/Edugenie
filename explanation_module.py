import os

from gemini_client import generate_text


async def explain_concept(
    topic: str,
    level: str = "beginner"
):

    provider = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini"
    ).lower()


    # Optional local model
    if provider == "local":

        try:

            from local_explainer import (
                explain_with_local_model
            )

            result = explain_with_local_model(
                topic,
                level
            )

            return {
                "module": "Explanation",
                "provider": "LaMini-Flan-T5",
                "explanation": result
            }

        except Exception as error:

            print(
                "Local model failed:",
                error
            )


    # Gemini explanation

    prompt = f"""
You are EduGenie's
concept explanation tutor.

Explain:

{topic}

Learner level:

{level}

Use this structure:

1. What is it?
2. How does it work?
3. Simple real-world example
4. Important points
5. Common mistake
6. One-line summary

Use simple language.
Avoid unnecessary technical jargon.
"""

    answer = generate_text(
        prompt
    )

    return {
        "module": "Explanation",
        "provider": "Gemini",
        "explanation": answer
    }