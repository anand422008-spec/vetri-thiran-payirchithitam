from config import MAX_INPUT_CHARS

from gemini_client import generate_structured

from models import QuizResponse


async def generate_quiz(
    text: str
) -> QuizResponse:

    text = text[
        :MAX_INPUT_CHARS
    ]


    prompt = f"""
Create exactly 3 multiple-choice
questions from the educational
content below.

For every question:

- Provide exactly 4 options.
- Only one option must be correct.
- correct_answer must contain the
  exact correct option.
- Add a short explanation.
- Questions must be answerable
  from the supplied content.
- Do not create trick questions.

CONTENT:

{text}
"""


    return generate_structured(

        prompt,

        QuizResponse,

        system_instruction=(
            "You create accurate educational "
            "multiple-choice questions."
        ),

        temperature=0.2,

        max_output_tokens=1600,
    )