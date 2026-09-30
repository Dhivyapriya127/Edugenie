from typing import Literal

from pydantic import BaseModel, Field


Level = Literal[
    "beginner",
    "intermediate",
    "advanced"
]


class QARequest(BaseModel):

    question: str = Field(
        ...,
        min_length=2,
        max_length=8000
    )


class ExplainRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=2,
        max_length=4000
    )

    level: Level = "beginner"


class QuizRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=20,
        max_length=20000
    )


class SummaryRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=20,
        max_length=30000
    )


class LearningPathRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=2,
        max_length=2000
    )

    level: Level = "beginner"

    hours_per_week: int = Field(
        default=5,
        ge=1,
        le=40
    )