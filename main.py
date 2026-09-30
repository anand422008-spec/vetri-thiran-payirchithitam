from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import (
    ExplainRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
    APITextResponse,
    QuizResponse,
    LearningPathResponse,
)

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent
(BASE_DIR / "static").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "templates").mkdir(parents=True, exist_ok=True)


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description="AI-powered educational assistant",
    version="1.0.0",
)


# -----------------------------
# Static files
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# -----------------------------
# Templates
# -----------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# -----------------------------
# Home Page (FIXED HERE)
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"context": "data"})
    
    
    


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# -----------------------------
# Question Answering
# -----------------------------

@app.post(
    "/qa",
    response_model=APITextResponse
)
async def qa(request: QARequest):

    try:

        result = await answer_question(
            request.question
        )

        return APITextResponse(
            result=result
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Concept Explanation
# -----------------------------

@app.post(
    "/explain",
    response_model=APITextResponse
)
async def explain(request: ExplainRequest):

    try:

        result = await explain_topic(
            request.topic
        )

        return APITextResponse(
            result=result
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Quiz Generation
# -----------------------------

@app.post(
    "/quiz",
    response_model=QuizResponse
)
async def quiz(request: QuizRequest):

    try:

        return await generate_quiz(
            request.text
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Summarization
# -----------------------------

@app.post(
    "/summarize",
    response_model=APITextResponse
)
async def summarize(request: SummaryRequest):

    try:

        result = await summarize_text(
            request.text
        )

        return APITextResponse(
            result=result
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Learning Path
# -----------------------------

@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse
)
async def learning_path(
    request: LearningPathRequest
):

    try:

        return await get_learning_recommendations(
            topic=request.topic,
            level=request.level,
            time_per_day=request.time_per_day,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )