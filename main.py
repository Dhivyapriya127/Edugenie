from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import (
    QARequest,
    ExplainRequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest
)

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# -----------------------------
# Static files
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


# -----------------------------
# Templates
# -----------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "EduGenie"
        }
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie"
    }


# -----------------------------
# Q&A API
# -----------------------------

@app.post("/qa")
async def qa(request: QARequest):

    return await answer_question(
        request.question
    )


# -----------------------------
# Explanation API
# -----------------------------

@app.post("/explain")
async def explain(request: ExplainRequest):

    return await explain_concept(
        request.topic,
        request.level
    )


# -----------------------------
# Quiz API
# -----------------------------

@app.post("/quiz")
async def quiz(request: QuizRequest):

    return await generate_quiz(
        request.text
    )


# -----------------------------
# Summary API
# -----------------------------

@app.post("/summarize")
async def summarize(request: SummaryRequest):

    return await summarize_text(
        request.text
    )


# -----------------------------
# Learning Path API
# -----------------------------

@app.post("/learn/recommendations")
async def recommendations(
    request: LearningPathRequest
):

    return await get_learning_recommendations(
        request.topic,
        request.level,
        request.hours_per_week
    )