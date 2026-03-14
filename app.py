"""AUTX Agent: Text Summarizer

A minimal AUTX-compatible agent that summarizes text using OpenAI.
Accepts POST requests with {"prompt": "..."} and returns a summary.
"""

import os

from fastapi import FastAPI, Header
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="AUTX Agent: Summarizer", version="1.0.0")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

SYSTEM_PROMPT = (
    "You are a concise summarizer. Given any text, produce a clear, "
    "accurate summary in 2-3 sentences. Preserve key facts and numbers. "
    "Do not add opinions or information not present in the original text."
)


class RequestBody(BaseModel):
    prompt: str


class SummaryResponse(BaseModel):
    response: str
    model: str


@app.post("/", response_model=SummaryResponse)
async def summarize(
    body: RequestBody,
    x_autx_protocol: str | None = Header(default=None),
):
    """Summarize the provided text."""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": body.prompt},
        ],
        max_tokens=256,
        temperature=0.3,
    )
    return SummaryResponse(
        response=completion.choices[0].message.content or "",
        model="gpt-4o-mini",
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
