from config import MAX_INPUT_CHARS

from gemini_client import generate_text


async def summarize_text(
    text: str
) -> str:

    text = text[
        :MAX_INPUT_CHARS
    ]


    prompt = f"""
Summarize the following educational
passage for a student.

Requirements:

- Preserve the main ideas.
- Preserve important facts.
- Remove repetition.
- Remove unnecessary details.
- Use simple language.
- Use bullet points when useful.
- Do not add information that
  is not present.

PASSAGE:

{text}
"""


    return generate_text(

        prompt,

        system_instruction=(
            "You are an expert academic summarizer."
        ),

        temperature=0.2,

        max_output_tokens=900,
    )