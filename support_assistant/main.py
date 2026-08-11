from fastapi import FastAPI

from pydantic import BaseModel, Field

from rag_pipeline import (
    SupportResponse,
    ask_question
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(

    title="Zepto Support Assistant",

    description=(
        "RAG-based Zepto policy support assistant"
    ),

    version="1.0.0"

)


# ============================================================
# REQUEST MODEL
# ============================================================

class AskRequest(BaseModel):

    query: str = Field(
        min_length=1,
        description="Customer question"
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "service":
            "Zepto Support Assistant",

        "status":
            "running",

        "mock_llm":
            True

    }


# ============================================================
# POST /ask
# ============================================================

@app.post(

    "/ask",

    response_model=SupportResponse

)
def ask(

    request: AskRequest

):

    return ask_question(
        request.query
    )