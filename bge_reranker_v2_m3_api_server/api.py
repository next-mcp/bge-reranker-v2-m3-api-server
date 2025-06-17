"""FastAPI application for BGE Reranker v2-m3 service."""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import __version__
from .models import (
    ErrorResponse,
    HealthResponse,
    RerankRequest,
    RerankResponse,
    ScoreItem,
)
from .service import RerankerService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global reranker service instance
reranker_service: RerankerService | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Manage application lifespan events."""
    global reranker_service

    # Startup
    logger.info("Starting BGE Reranker v2-m3 API Server")

    # Initialize reranker service
    model_name = os.getenv("BGE_MODEL_NAME", "BAAI/bge-reranker-v2-m3")
    use_fp16 = os.getenv("BGE_USE_FP16", "true").lower() == "true"

    reranker_service = RerankerService(model_name=model_name, use_fp16=use_fp16)

    # Load model
    try:
        reranker_service.load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        # Continue startup even if model fails to load
        # This allows the health endpoint to report the error

    yield

    # Shutdown
    logger.info("Shutting down BGE Reranker v2-m3 API Server")


# Create FastAPI app
app = FastAPI(
    title="BGE Reranker v2-m3 API Server",
    description="High-performance multilingual text reranking service using BAAI BGE Reranker v2-m3",
    version=__version__,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def general_exception_handler(_request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error", detail=str(exc), error_code="INTERNAL_ERROR"
        ).model_dump(),
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    global reranker_service

    model_loaded = False
    if reranker_service:
        model_loaded = reranker_service.is_model_loaded()

    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        version=__version__,
        model_name=reranker_service.model_name if reranker_service else "unknown",
    )


@app.post("/rerank", response_model=RerankResponse)
async def rerank_documents(request: RerankRequest):
    """Rerank documents based on relevance to query."""
    global reranker_service

    if not reranker_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Reranker service not initialized",
        )

    if not reranker_service.is_model_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded"
        )

    try:
        # Perform reranking
        results, processing_time = reranker_service.rerank(
            query=request.query,
            documents=request.documents,
            top_k=request.top_k,
            normalize=request.normalize,
        )

        # Format results
        score_items: list[ScoreItem] = []
        for index, score, document in results:
            score_items.append(
                ScoreItem(
                    index=index,
                    score=score,
                    document=document if request.return_documents else "",
                )
            )

        return RerankResponse(
            results=score_items,
            query=request.query,
            total_documents=len(request.documents),
            returned_results=len(score_items),
            processing_time_ms=processing_time,
        )

    except Exception as e:
        logger.error(f"Error during reranking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reranking failed: {e!s}",
        ) from e


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "BGE Reranker v2-m3 API Server",
        "version": __version__,
        "description": "High-performance multilingual text reranking service",
        "docs_url": "/docs",
        "health_url": "/health",
    }
