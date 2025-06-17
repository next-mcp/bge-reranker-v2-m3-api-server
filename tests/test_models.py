"""Tests for data models."""

import pytest
from pydantic import ValidationError

from bge_reranker_v2_m3_api_server.models import (
    HealthResponse,
    RerankRequest,
    RerankResponse,
    ScoreItem,
)


class TestScoreItem:
    """Test ScoreItem model."""

    def test_valid_score_item(self):
        """Test creating valid ScoreItem."""
        item = ScoreItem(index=0, score=0.95, document="Test document")
        assert item.index == 0
        assert item.score == 0.95
        assert item.document == "Test document"


class TestRerankRequest:
    """Test RerankRequest model."""

    def test_valid_request(self):
        """Test creating valid rerank request."""
        request = RerankRequest(
            query="What is AI?",
            documents=[
                "AI is artificial intelligence",
                "Python is a programming language",
            ],
        )
        assert request.query == "What is AI?"
        assert len(request.documents) == 2
        assert request.normalize is True
        assert request.return_documents is True
        assert request.top_k is None

    def test_empty_query_fails(self):
        """Test that empty query fails validation."""
        with pytest.raises(ValidationError):
            RerankRequest(query="", documents=["test"])

    def test_empty_documents_fails(self):
        """Test that empty documents list fails validation."""
        with pytest.raises(ValidationError):
            RerankRequest(query="test", documents=[])

    def test_with_top_k(self):
        """Test request with top_k parameter."""
        request = RerankRequest(
            query="test", documents=["doc1", "doc2", "doc3"], top_k=2
        )
        assert request.top_k == 2

    def test_invalid_top_k_fails(self):
        """Test that invalid top_k fails validation."""
        with pytest.raises(ValidationError):
            RerankRequest(query="test", documents=["doc1"], top_k=0)


class TestRerankResponse:
    """Test RerankResponse model."""

    def test_valid_response(self):
        """Test creating valid rerank response."""
        score_items = [
            ScoreItem(index=0, score=0.95, document="doc1"),
            ScoreItem(index=1, score=0.85, document="doc2"),
        ]

        response = RerankResponse(
            results=score_items,
            query="test query",
            total_documents=2,
            returned_results=2,
            processing_time_ms=150.5,
        )

        assert len(response.results) == 2
        assert response.query == "test query"
        assert response.total_documents == 2
        assert response.returned_results == 2
        assert response.processing_time_ms == 150.5


class TestHealthResponse:
    """Test HealthResponse model."""

    def test_healthy_response(self):
        """Test creating healthy response."""
        response = HealthResponse(
            status="healthy",
            model_loaded=True,
            version="0.0.0",
            model_name="BAAI/bge-reranker-v2-m3",
        )

        assert response.status == "healthy"
        assert response.model_loaded is True
        assert response.version == "0.0.0"
        assert response.model_name == "BAAI/bge-reranker-v2-m3"
