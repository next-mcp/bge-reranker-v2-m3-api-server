"""BGE Reranker v2-m3 API Server.

A FastAPI-based service for the BAAI BGE Reranker v2-m3 model,
providing high-performance multilingual text reranking capabilities.
"""

__version__ = "0.0.0"
__author__ = "yarnovo"
__email__ = "yarnb@qq.com"
__description__ = "FastAPI server for BGE Reranker v2-m3 model"

from .models import RerankRequest, RerankResponse, ScoreItem
from .service import RerankerService

__all__ = [
    "RerankRequest",
    "RerankResponse",
    "RerankerService",
    "ScoreItem",
]
