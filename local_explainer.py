from transformers import pipeline


MODEL_NAME = (
    "MBZUAI/LaMini-Flan-T5-783M"
)


def explain_with_local_model(
    topic: str,
    level: str
):

    generator = pipeline(
        "text2text-generation",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )

    prompt = f"""
Explain {topic}
to a {level} student.

Use:

1. Simple definition
2. How it works
3. Real-world example
4. Important points
5. Short summary
"""

    result = generator(
        prompt,
        max_new_tokens=300,
        do_sample=False
    )

    return result[0][
        "generated_text"
    ].strip()