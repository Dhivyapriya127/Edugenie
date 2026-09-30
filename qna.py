from gemini_client import generate_text


async def answer_question(question: str):

    prompt = f"""
You are EduGenie,
an AI educational assistant.

Answer the student's question accurately.

Follow these rules:

1. Use simple language.
2. Explain difficult terms.
3. Give examples when useful.
4. Do not invent facts.
5. Use bullet points where appropriate.
6. Keep the answer easy for students.
7. End with a short Key Takeaway.

Student Question:

{question}
"""

    answer = generate_text(prompt)

    return {
        "module": "Q&A",
        "answer": answer
    }