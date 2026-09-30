from typing import List, Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


# =====================================================
# General response
# =====================================================

class APITextResponse(BaseModel):

    result: str


# =====================================================
# Question Answering
# =====================================================

class QARequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=12000
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):

        value = value.strip()

        if not value:

            raise ValueError(
                "Question cannot be empty."
            )

        return value


# =====================================================
# Explanation
# =====================================================

class ExplainRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value):

        value = value.strip()

        if not value:

            raise ValueError(
                "Topic cannot be empty."
            )

        return value


# =====================================================
# Quiz
# =====================================================

class QuizRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=12000
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):

        value = value.strip()

        if not value:

            raise ValueError(
                "Quiz content cannot be empty."
            )

        return value


class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str


class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


# =====================================================
# Summary
# =====================================================

class SummaryRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):

        value = value.strip()

        if not value:

            raise ValueError(
                "Text cannot be empty."
            )

        return value


# =====================================================
# Learning Path
# =====================================================

class LearningPathRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=3000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"

    time_per_day: int = Field(
        default=30,
        ge=10,
        le=240
    )

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value):

        value = value.strip()

        if not value:

            raise ValueError(
                "Topic cannot be empty."
            )

        return value


class LearningStep(BaseModel):

    order: int

    title: str

    difficulty: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]

    description: str

    estimated_minutes: int = Field(
        ge=5,
        le=10080
    )


class LearningPathResponse(BaseModel):

    topic: str

    learner_level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]

    daily_minutes: int

    steps: List[LearningStep]

    resources: List[str]

    study_tips: List[str]