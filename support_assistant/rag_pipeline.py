import os

from pathlib import Path

from typing import TypedDict, List


import chromadb

from sentence_transformers import SentenceTransformer


from pydantic import BaseModel, Field


from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "zepto_policies"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# MOCK_LLM
# ============================================================

def mock_llm_enabled():

    value = os.getenv(
        "MOCK_LLM",
        "1"
    )

    return value != "0"


# ============================================================
# PYDANTIC RESPONSE
# ============================================================

class SupportResponse(BaseModel):

    answer: str

    sources: List[str] = Field(
        default_factory=list
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )


# ============================================================
# LANGGRAPH STATE
# ============================================================

class GraphState(TypedDict, total=False):

    query: str

    intent: str

    retrieved_documents: List[str]

    retrieved_ids: List[str]

    answer: str

    sources: List[str]

    confidence: float


# ============================================================
# CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# ============================================================
# MOCK CLASSIFICATION KEYWORDS
# ============================================================

POLICY_KEYWORDS = [

    "delivery",

    "return",

    "refund",

    "membership",

    "tracking",

    "cancel",

    "gift card",

    "support hours"

]


# ============================================================
# STRUCTURED PROMPT
# ============================================================

PROMPT_TEMPLATE = """
ROLE:
You are Zepto's customer support assistant.

CONTEXT:
You must answer the customer's question using only
the retrieved Zepto policy context.

TASK:
Answer the customer's question accurately and concisely
using the retrieved policy information.

FORMAT:
Return a JSON object containing:
- answer
- sources
- confidence

LENGTH:
Keep the answer concise and directly relevant.

NEGATIVE CONSTRAINT:
Do not answer using information that is not present
in the provided context.
Do not invent or assume Zepto policies.

FEW-SHOT EXAMPLE:

Customer question:
How long can I report a damaged grocery item?

Retrieved context:
Grocery and perishable items may be reported for a return
within 24 hours of delivery if damaged, spoiled, or incorrect.

Expected answer:
{
    "answer": "Damaged grocery items should be reported within 24 hours of delivery.",
    "sources": ["doc_02"],
    "confidence": 1.0
}

Customer question:
{query}

Retrieved context:
{context}
"""


# ============================================================
# MOCK INTENT CLASSIFIER
# ============================================================

def mock_classify_intent(
    query: str
):

    query_lower = query.lower()

    for keyword in POLICY_KEYWORDS:

        if keyword in query_lower:

            return "policy_question"

    return "general_question"


# ============================================================
# OPTIONAL REAL LLM INTENT CLASSIFIER
# ============================================================

def real_classify_intent(
    query: str
):

    try:

        from langchain_groq import ChatGroq

    except ImportError:

        raise RuntimeError(
            "Install langchain-groq to use MOCK_LLM=0."
        )

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GROQ_API_KEY is required when MOCK_LLM=0."
        )

    llm = ChatGroq(

        model="llama-3.1-8b-instant",

        temperature=0,

        api_key=api_key

    )

    prompt = f"""
Classify the following customer question as exactly one:

policy_question
general_question

Use policy_question when the question concerns:

delivery
return
refund
membership
tracking
cancel
gift card
support hours

Question:
{query}

Return only the classification.
"""

    response = llm.invoke(
        prompt
    )

    result = response.content.strip()

    if result == "policy_question":

        return "policy_question"

    return "general_question"


# ============================================================
# NODE 1 — CLASSIFY INTENT
# ============================================================

def classify_intent(
    state: GraphState
):

    query = state["query"]

    if mock_llm_enabled():

        intent = mock_classify_intent(
            query
        )

    else:

        intent = real_classify_intent(
            query
        )

    print(
        f"[classify_intent] {intent}"
    )

    return {

        **state,

        "intent": intent

    }


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_documents(
    query: str,
    top_k: int = 3
):

    query_embedding = embedding_model.encode(

        query,

        normalize_embeddings=True

    ).tolist()

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )

    documents = results[
        "documents"
    ][0]

    metadatas = results[
        "metadatas"
    ][0]

    distances = results[
        "distances"
    ][0]

    ids = []

    for metadata in metadatas:

        ids.append(
            metadata["document_id"]
        )

    return (
        documents,
        ids,
        distances
    )


# ============================================================
# OPTIONAL REAL LLM GENERATION
# ============================================================

def real_generate_answer(

    query: str,

    documents: List[str],

    ids: List[str]

):

    try:

        from langchain_groq import ChatGroq

    except ImportError:

        raise RuntimeError(
            "Install langchain-groq to use MOCK_LLM=0."
        )

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GROQ_API_KEY is required."
        )

    llm = ChatGroq(

        model="llama-3.1-8b-instant",

        temperature=0,

        api_key=api_key

    )

    context = "\n\n".join(
        documents
    )

    prompt = PROMPT_TEMPLATE.format(

        query=query,

        context=context

    )

    last_error = None

    # Initial attempt + 2 retries = 3 total attempts.

    for attempt in range(3):

        try:

            corrective_instruction = ""

            if attempt > 0:

                corrective_instruction = """

CORRECTION:
Your previous response failed Pydantic validation.

Return ONLY valid JSON in exactly this structure:

{
    "answer": "string",
    "sources": ["document_id"],
    "confidence": 0.0
}

Do not include markdown.
The confidence must be between 0 and 1.
"""

            response = llm.invoke(

                prompt +

                corrective_instruction

            )

            raw_output = response.content.strip()

            import json

            parsed = json.loads(
                raw_output
            )

            validated = SupportResponse.model_validate(
                parsed
            )

            return validated

        except Exception as error:

            last_error = error

            print(
                f"LLM validation attempt "
                f"{attempt + 1} failed: {error}"
            )

    return SupportResponse(

        answer=(
            "ERROR: The LLM response failed "
            "validation after three attempts."
        ),

        sources=[],

        confidence=0.0

    )


# ============================================================
# NODE 2 — RETRIEVE AND ANSWER
# ============================================================

def retrieve_and_answer(
    state: GraphState
):

    query = state["query"]

    print(
        "[retrieve_and_answer] "
        "Retrieving top 3 chunks..."
    )

    (
        documents,
        ids,
        distances

    ) = retrieve_documents(

        query,

        top_k=3

    )

    if not documents:

        return {

            **state,

            "retrieved_documents": [],

            "retrieved_ids": [],

            "answer":
                "No relevant policy information was found.",

            "sources": [],

            "confidence": 0.0

        }


    # ========================================================
    # MOCK MODE
    # ========================================================

    if mock_llm_enabled():

        top_chunk = documents[0]

        top_chunk_snippet = top_chunk[:200]

        answer = (

            "Based on the retrieved context: "

            + top_chunk_snippet

        )

        return {

            **state,

            "retrieved_documents": documents,

            "retrieved_ids": ids,

            "answer": answer,

            "sources": ids,

            "confidence": 1.0

        }


    # ========================================================
    # REAL LLM MODE
    # ========================================================

    validated = real_generate_answer(

        query,

        documents,

        ids

    )

    return {

        **state,

        "retrieved_documents": documents,

        "retrieved_ids": ids,

        "answer": validated.answer,

        "sources": validated.sources,

        "confidence": validated.confidence

    }


# ============================================================
# NODE 3 — DIRECT ANSWER
# ============================================================

def direct_answer(
    state: GraphState
):

    query = state["query"]

    # ========================================================
    # MOCK MODE
    # ========================================================

    if mock_llm_enabled():

        answer = (
            "I can only answer questions about "
            "Zepto policies right now."
        )

        return {

            **state,

            "answer": answer,

            "sources": [],

            "confidence": 1.0

        }


    # ========================================================
    # OPTIONAL REAL LLM MODE
    # ========================================================

    try:

        from langchain_groq import ChatGroq

    except ImportError:

        return {

            **state,

            "answer":
                "ERROR: Install langchain-groq.",

            "sources": [],

            "confidence": 0.0

        }

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:

        return {

            **state,

            "answer":
                "ERROR: GROQ_API_KEY is not configured.",

            "sources": [],

            "confidence": 0.0

        }

    llm = ChatGroq(

        model="llama-3.1-8b-instant",

        temperature=0,

        api_key=api_key

    )

    prompt = f"""
You are a Zepto customer support assistant.

Answer the following general question directly.

Question:
{query}
"""

    response = llm.invoke(
        prompt
    )

    return {

        **state,

        "answer":
            response.content,

        "sources": [],

        "confidence": 0.8

    }


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

def route_after_classification(
    state: GraphState
):

    if state["intent"] == "policy_question":

        return "retrieve_and_answer"

    return "direct_answer"


# ============================================================
# BUILD LANGGRAPH
# ============================================================

def build_graph():

    workflow = StateGraph(
        GraphState
    )

    # Three required nodes.

    workflow.add_node(

        "classify_intent",

        classify_intent

    )

    workflow.add_node(

        "retrieve_and_answer",

        retrieve_and_answer

    )

    workflow.add_node(

        "direct_answer",

        direct_answer

    )

    # START → classify_intent

    workflow.add_edge(

        START,

        "classify_intent"

    )

    # Conditional routing.

    workflow.add_conditional_edges(

        "classify_intent",

        route_after_classification,

        {

            "retrieve_and_answer":
                "retrieve_and_answer",

            "direct_answer":
                "direct_answer"

        }

    )

    # Final nodes → END

    workflow.add_edge(

        "retrieve_and_answer",

        END

    )

    workflow.add_edge(

        "direct_answer",

        END

    )

    return workflow.compile()


# ============================================================
# CREATE GRAPH
# ============================================================

graph = build_graph()


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def ask_question(
    query: str
):

    if not query or not query.strip():

        return SupportResponse(

            answer="Please provide a question.",

            sources=[],

            confidence=0.0

        )

    result = graph.invoke(

        {

            "query":
                query.strip()

        }

    )

    return SupportResponse(

        answer=result.get(
            "answer",
            ""
        ),

        sources=result.get(
            "sources",
            []
        ),

        confidence=result.get(
            "confidence",
            0.0
        )

    )


# ============================================================
# LOCAL TESTING
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("MODULE 3 LANGGRAPH TEST")
    print("=" * 70)

    print(
        "MOCK_LLM =",
        os.getenv(
            "MOCK_LLM",
            "1"
        )
    )

    # --------------------------------------------------------
    # POLICY QUESTION
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("TEST 1: POLICY QUESTION")
    print("-" * 70)

    policy_response = ask_question(

        "How much is the delivery fee?"

    )

    print(
        policy_response.model_dump_json(
            indent=2
        )
    )

    # --------------------------------------------------------
    # GENERAL QUESTION
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("TEST 2: GENERAL QUESTION")
    print("-" * 70)

    general_response = ask_question(

        "What is the capital of India?"

    )

    print(
        general_response.model_dump_json(
            indent=2
        )
    )