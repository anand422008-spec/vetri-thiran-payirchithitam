from gemini_client import generate_structured

from models import LearningPathResponse


async def get_learning_recommendations(

    topic: str,

    level: str = "beginner",

    time_per_day: int = 30,

) -> LearningPathResponse:


    prompt = f"""
Create a personalized learning path
for the topic:

{topic}

Learner level:

{level}

Available study time:

{time_per_day} minutes per day.

Requirements:

- Start with the fundamentals.
- Progress toward advanced concepts.
- Match the learner's level.
- Give practical study steps.
- Include estimated study time.
- Suggest useful resource types.
- Do not invent URLs.
- Include study tips.
- Keep the learning path manageable.
"""


    result = generate_structured(

        prompt,

        LearningPathResponse,

        system_instruction=(
            "You are an educational learning-path "
            "designer. Create practical and accurate "
            "study plans."
        ),

        temperature=0.3,

        max_output_tokens=1800,
    )


    result.topic = topic

    result.learner_level = level

    result.daily_minutes = time_per_day


    return result