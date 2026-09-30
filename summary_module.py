from gemini_client import generate_text


async def summarize_text(
    text: str
):

    prompt = f"""
You are EduGenie,
an educational summarization assistant.

Summarize the following educational
content.

Requirements:

1. Keep the important information.
2. Remove repetition.
3. Use simple language.
4. Make it useful for exam revision.
5. Use headings and bullet points.
6. Do not add information that is
   not present in the original text.

Content:

{text}
"""

    summary = generate_text(
        prompt
    )

    return {
        "module": "Summary",
        "summary": summary
    }