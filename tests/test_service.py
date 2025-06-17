"""Tests for RerankerService."""

from unittest.mock import Mock, patch

import pytest

from bge_reranker_v2_m3_api_server.service import RerankerService


class TestRerankerService:
    """Test RerankerService functionality."""

    def test_service_initialization(self):
        """Test service initialization."""
        service = RerankerService()

        assert service.model_name == "BAAI/bge-reranker-v2-m3"
        assert service.use_fp16 is True
        assert service.device is None
        assert service._model_loaded is False

    def test_custom_initialization(self):
        """Test service initialization with custom parameters."""
        service = RerankerService(
            model_name="custom/model", use_fp16=False, device="cpu"
        )

        assert service.model_name == "custom/model"
        assert service.use_fp16 is False
        assert service.device == "cpu"

    def test_model_not_loaded_initially(self):
        """Test that model is not loaded initially."""
        service = RerankerService()
        assert not service.is_model_loaded()

    @patch("bge_reranker_v2_m3_api_server.service.FlagReranker")
    def test_load_model_success(self, mock_flag_reranker):
        """Test successful model loading."""
        mock_reranker_instance = Mock()
        mock_flag_reranker.return_value = mock_reranker_instance

        service = RerankerService()
        service.load_model()

        assert service.is_model_loaded()
        mock_flag_reranker.assert_called_once_with(
            "BAAI/bge-reranker-v2-m3", use_fp16=True
        )

    def test_load_model_flag_embedding_not_available(self):
        """Test model loading when FlagEmbedding is not available."""
        with patch("bge_reranker_v2_m3_api_server.service.FlagReranker", None):
            service = RerankerService()

            with pytest.raises(ImportError, match="FlagEmbedding is not installed"):
                service.load_model()

    @patch("bge_reranker_v2_m3_api_server.service.FlagReranker")
    def test_load_model_failure(self, mock_flag_reranker):
        """Test model loading failure."""
        mock_flag_reranker.side_effect = Exception("Model loading failed")

        service = RerankerService()

        with pytest.raises(Exception, match="Model loading failed"):
            service.load_model()

        assert not service.is_model_loaded()

    def test_compute_scores_without_model(self):
        """Test computing scores without loaded model."""
        service = RerankerService()

        with pytest.raises(RuntimeError, match="Model is not loaded"):
            service.compute_scores("query", ["doc1", "doc2"])

    @patch("bge_reranker_v2_m3_api_server.service.FlagReranker")
    def test_compute_scores_success(self, mock_flag_reranker):
        """Test successful score computation."""
        mock_reranker_instance = Mock()
        mock_reranker_instance.compute_score.return_value = [0.9, 0.7, 0.3]
        mock_flag_reranker.return_value = mock_reranker_instance

        service = RerankerService()
        service.load_model()

        query = "test query"
        documents = ["doc1", "doc2", "doc3"]

        scores, processing_time = service.compute_scores(query, documents)

        assert scores == [0.9, 0.7, 0.3]
        assert isinstance(processing_time, float)
        assert processing_time >= 0

        # Verify the correct query-document pairs were passed (using tuples)
        expected_pairs = [
            ("test query", "doc1"),
            ("test query", "doc2"),
            ("test query", "doc3"),
        ]
        mock_reranker_instance.compute_score.assert_called_once_with(
            expected_pairs, normalize=True
        )

    @patch("bge_reranker_v2_m3_api_server.service.FlagReranker")
    def test_compute_scores_single_score(self, mock_flag_reranker):
        """Test score computation with single score return."""
        mock_reranker_instance = Mock()
        mock_reranker_instance.compute_score.return_value = (
            0.95  # Single score, not list
        )
        mock_flag_reranker.return_value = mock_reranker_instance

        service = RerankerService()
        service.load_model()

        scores, _ = service.compute_scores("query", ["doc1"])

        assert scores == [0.95]  # Should be converted to list

    @patch("bge_reranker_v2_m3_api_server.service.FlagReranker")
    def test_rerank_success(self, mock_flag_reranker):
        """Test successful reranking."""
        mock_reranker_instance = Mock()
        mock_reranker_instance.compute_score.return_value = [0.3, 0.9, 0.7]
        mock_flag_reranker.return_value = mock_reranker_instance

        service = RerankerService()
        service.load_model()

        query = "test query"
        documents = ["doc1", "doc2", "doc3"]

        results, processing_time = service.rerank(query, documents)

        # Results should be sorted by score (descending)
        assert len(results) == 3
        assert results[0] == (1, 0.9, "doc2")  # Highest score
        assert results[1] == (2, 0.7, "doc3")  # Middle score
        assert results[2] == (0, 0.3, "doc1")  # Lowest score
        assert isinstance(processing_time, float)

    @patch("bge_reranker_v2_m3_api_server.service.FlagReranker")
    def test_rerank_with_top_k(self, mock_flag_reranker):
        """Test reranking with top_k limit."""
        mock_reranker_instance = Mock()
        mock_reranker_instance.compute_score.return_value = [0.3, 0.9, 0.7]
        mock_flag_reranker.return_value = mock_reranker_instance

        service = RerankerService()
        service.load_model()

        query = "test query"
        documents = ["doc1", "doc2", "doc3"]

        results, _ = service.rerank(query, documents, top_k=2)

        # Should return only top 2 results
        assert len(results) == 2
        assert results[0] == (1, 0.9, "doc2")  # Highest score
        assert results[1] == (2, 0.7, "doc3")  # Second highest score

    @patch("bge_reranker_v2_m3_api_server.service.FlagReranker")
    def test_rerank_without_normalization(self, mock_flag_reranker):
        """Test reranking without score normalization."""
        mock_reranker_instance = Mock()
        mock_reranker_instance.compute_score.return_value = [-2.5, 1.8, -0.3]
        mock_flag_reranker.return_value = mock_reranker_instance

        service = RerankerService()
        service.load_model()

        query = "test query"
        documents = ["doc1", "doc2", "doc3"]

        results, _ = service.rerank(query, documents, normalize=False)

        # Verify normalize=False was passed to compute_score (using tuples)
        mock_reranker_instance.compute_score.assert_called_with(
            [("test query", "doc1"), ("test query", "doc2"), ("test query", "doc3")],
            normalize=False,
        )

        # Results should be sorted by score (descending)
        assert results[0] == (1, 1.8, "doc2")  # Highest score
        assert results[1] == (2, -0.3, "doc3")  # Middle score
        assert results[2] == (0, -2.5, "doc1")  # Lowest score
