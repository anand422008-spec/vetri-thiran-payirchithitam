from config import (
    LOCAL_EXPLANATION_MODEL,
    USE_LOCAL_EXPLANATION,
)

from gemini_client import generate_text


LOCAL_PIPELINE = None


# =====================================================
# Local LaMini explanation
# =====================================================

def local_explanation(
    topic: str
) -> str:

    global LOCAL_PIPELINE


    try:

        from transformers import pipeline


        if LOCAL_PIPELINE is None:

            LOCAL_PIPELINE = pipeline(

                "text2text-generation",

                model=LOCAL_EXPLANATION_MODEL,

                tokenizer=LOCAL_EXPLANATION_MODEL,
            )


        prompt = (
            "Explain the following concept "
            "to a beginner in simple language. "
            "Use a short definition, key points "
            "and one simple example. "
            f"Concept: {topic}"
        )


        result = LOCAL_PIPELINE(

            prompt,

            max_new_tokens=250,

            do_sample=False,
        )


        return result[
            0
        ][
            "generated_text"
        ].strip()


    except Exception:

        return ""


# =====================================================
# Main explanation function
# =====================================================

async def explain_topic(
    topic: str
) -> str:


    if USE_LOCAL_EXPLANATION:

        result = local_explanation(
            topic
        )

        if result:

            return result


    prompt = f"""
Explain "{topic}" to a learner
who may have no prior knowledge.

Use this structure:

1. Simple definition
2. How it works
3. Key points
4. One easy example
5. One-line recap

Keep the explanation concise,
simple and educational.
"""


    return generate_text(

        prompt,

        system_instruction=(
            "You are a patient teacher "
            "who simplifies difficult concepts."
        ),

        temperature=0.3,

        max_output_tokens=900,
    )