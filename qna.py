from config import MAX_INPUT_CHARS

from gemini_client import generate_text


async def answer_question(
    question: str
) -> str:

    question = question[
        :MAX_INPUT_CHARS
    ]


    prompt = f"""
You are EduGenie, a student-friendly
educational assistant.

Answer the student's question accurately
and clearly.

Rules:

- Start with the direct answer.
- Explain important terms simply.
- Use bullet points when useful.
- If the question is ambiguous, state your assumption.
- Do not invent facts.
- Keep the answer appropriate for students.

Student question:

{question}
"""


    return generate_text(

        prompt,

        system_instruction=(
            "You are a concise and reliable "
            "educational tutor."
        ),

        temperature=0.3,

        max_output_tokens=1000,
    )