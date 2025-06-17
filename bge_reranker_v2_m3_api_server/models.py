"""Data models for the BGE Reranker API."""

from typing import Any

from pydantic import BaseModel, Field


class ScoreItem(BaseModel):
    """Individual score item for reranking results."""

    index: int = Field(..., description="Original index of the document")
    score: float = Field(..., description="Relevance score")
    document: str = Field(..., description="The document text")


class RerankRequest(BaseModel):
    """Request model for reranking API."""

    query: str = Field(..., description="The search query", min_length=1)
    documents: list[str] = Field(
        ..., description="List of documents to rerank", min_length=1, max_length=1000
    )
    top_k: int | None = Field(
        None, description="Number of top results to return (default: return all)", ge=1
    )
    normalize: bool = Field(
        True, description="Whether to normalize scores using sigmoid function"
    )
    return_documents: bool = Field(
        True, description="Whether to return document text in results"
    )


class RerankResponse(BaseModel):
    """Response model for reranking API."""

    results: list[ScoreItem] = Field(..., description="Ranked results")
    query: str = Field(..., description="The original query")
    total_documents: int = Field(..., description="Total number of input documents")
    returned_results: int = Field(..., description="Number of results returned")
    processing_time_ms: float = Field(
        ..., description="Processing time in milliseconds"
    )


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether the model is loaded")
    version: str = Field(..., description="API version")
    model_name: str = Field(..., description="Name of the loaded model")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: str | dict[str, Any] | None = Field(
        None, description="Additional error details"
    )
    error_code: str | None = Field(None, description="Error code")
