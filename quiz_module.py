from gemini_client import generate_json


QUIZ_SCHEMA = {

    "type": "object",

    "properties": {

        "questions": {

            "type": "array",

            "minItems": 3,
            "maxItems": 3,

            "items": {

                "type": "object",

                "properties": {

                    "question": {
                        "type": "string"
                    },

                    "options": {

                        "type": "array",

                        "minItems": 4,
                        "maxItems": 4,

                        "items": {
                            "type": "string"
                        }
                    },

                    "correct_answer": {
                        "type": "string"
                    },

                    "explanation": {
                        "type": "string"
                    }
                },

                "required": [
                    "question",
                    "options",
                    "correct_answer",
                    "explanation"
                ]
            }
        }
    },

    "required": [
        "questions"
    ]
}


async def generate_quiz(
    text: str
):

    prompt = f"""
You are EduGenie,
an educational quiz generator.

Create exactly 3 multiple-choice
questions from the following content.

Rules:

1. Exactly 3 questions.
2. Each question must have exactly 4 options.
3. Only one option is correct.
4. The correct_answer must exactly
   match one of the options.
5. Questions should test understanding.
6. Provide a short explanation.
7. Return only JSON matching the schema.

Content:

{text}
"""

    data = generate_json(
        prompt,
        QUIZ_SCHEMA
    )

    return {
        "module": "Quiz",
        **data
    }