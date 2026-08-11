# Module 3 — Support Assistant

## Overview

This module implements a small Retrieval-Augmented Generation (RAG)
support assistant for Zepto policy questions.

The system includes:

- 8 Zepto policy documents
- Local sentence-transformer embeddings
- ChromaDB vector storage
- LangGraph StateGraph
- Pydantic structured output
- FastAPI REST API
- Docker containerization

The graded baseline uses `MOCK_LLM=1`.

No LLM API key is required for the graded implementation.

---

# 1. Graded Mock Mode

The required graded mode is:

```text
MOCK_LLM=1