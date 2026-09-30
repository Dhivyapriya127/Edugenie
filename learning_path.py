from gemini_client import generate_text


async def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    hours_per_week: int = 5
):

    prompt = f"""
You are EduGenie,
a personalized learning advisor.

Create a structured learning path.

Topic:

{topic}

Current Level:

{level}

Study Time:

{hours_per_week} hours per week

Include:

1. Learning goal
2. Prerequisites
3. Beginner stage
4. Intermediate stage
5. Advanced stage
6. Six-week learning schedule
7. Practice exercises
8. Mini project ideas
9. How to measure progress
10. Recommended types of resources

Resource examples may include:

- YouTube
- Official documentation
- Books
- Practice websites
- Online courses

Do not invent exact URLs.

Make the plan practical
for a college student.
"""

    result = generate_text(
        prompt
    )

    return {
        "module": "Learning Path",
        "learning_path": result
    }