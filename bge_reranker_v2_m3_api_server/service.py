"""BGE Reranker service implementation."""

import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FlagEmbedding import FlagReranker
else:
    try:
        from FlagEmbedding import FlagReranker
    except ImportError:
        FlagReranker = None  # type: ignore

logger = logging.getLogger(__name__)


class RerankerService:
    """Service class for BGE Reranker v2-m3 model."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-v2-m3",
        use_fp16: bool = True,
        device: str | None = None,
    ):
        """Initialize the reranker service.

        Args:
            model_name: Name or path of the BGE reranker model
            use_fp16: Whether to use FP16 for faster inference
            device: Device to load the model on (cuda/cpu)
        """
        self.model_name = model_name
        self.use_fp16 = use_fp16
        self.device = device
        self._reranker: FlagReranker | None = None
        self._model_loaded = False

    def load_model(self) -> None:
        """Load the BGE reranker model."""
        if FlagReranker is None:
            raise ImportError(
                "FlagEmbedding is not installed. Please install it with: "
                "pip install FlagEmbedding"
            )

        try:
            logger.info(f"Loading BGE reranker model: {self.model_name}")
            self._reranker = FlagReranker(self.model_name, use_fp16=self.use_fp16)
            self._model_loaded = True
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def is_model_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._model_loaded and self._reranker is not None

    def compute_scores(
        self,
        query: str,
        documents: list[str],
        normalize: bool = True,
    ) -> tuple[list[float], float]:
        """Compute relevance scores for query-document pairs.

        Args:
            query: The search query
            documents: List of documents to score
            normalize: Whether to normalize scores using sigmoid

        Returns:
            Tuple of (scores, processing_time_ms)
        """
        if not self.is_model_loaded():
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        start_time = time.time()

        try:
            # Prepare query-document pairs
            pairs = [(query, doc) for doc in documents]

            # Compute scores
            scores = self._reranker.compute_score(pairs, normalize=normalize)  # type: ignore

            # Ensure scores is a list and convert to float
            if not isinstance(scores, list):
                scores = [scores]
            # Convert all scores to Python float, handling numpy types
            scores = [float(score) if score is not None else 0.0 for score in scores]

            processing_time = (time.time() - start_time) * 1000  # Convert to ms

            return scores, processing_time

        except Exception as e:
            logger.error(f"Error computing scores: {e}")
            raise

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int | None = None,
        normalize: bool = True,
    ) -> tuple[list[tuple[int, float, str]], float]:
        """Rerank documents based on relevance to query.

        Args:
            query: The search query
            documents: List of documents to rerank
            top_k: Number of top results to return (None for all)
            normalize: Whether to normalize scores

        Returns:
            Tuple of (ranked_results, processing_time_ms)
            where ranked_results is list of (index, score, document) tuples
        """
        scores, processing_time = self.compute_scores(query, documents, normalize)

        # Create (index, score, document) tuples
        results = [
            (i, score, doc)
            for i, (score, doc) in enumerate(zip(scores, documents, strict=False))
        ]

        # Sort by score (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        # Apply top_k limit if specified
        if top_k is not None:
            results = results[:top_k]

        return results, processing_time
