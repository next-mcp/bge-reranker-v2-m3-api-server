"""Command line interface for BGE Reranker API Server."""

import argparse
import logging
import os

import uvicorn


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="BGE Reranker v2-m3 API Server")

    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )

    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to (default: 8000)"
    )

    parser.add_argument(
        "--workers", type=int, default=1, help="Number of worker processes (default: 1)"
    )

    parser.add_argument(
        "--model-name",
        default="BAAI/bge-reranker-v2-m3",
        help="BGE model name or path (default: BAAI/bge-reranker-v2-m3)",
    )

    parser.add_argument(
        "--use-fp16",
        action="store_true",
        default=True,
        help="Use FP16 for faster inference (default: True)",
    )

    parser.add_argument(
        "--no-fp16", action="store_false", dest="use_fp16", help="Disable FP16"
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Log level (default: INFO)",
    )

    parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Set environment variables for the service
    os.environ["BGE_MODEL_NAME"] = args.model_name
    os.environ["BGE_USE_FP16"] = str(args.use_fp16).lower()

    # Run the server
    uvicorn.run(
        "bge_reranker_v2_m3_api_server.api:app",
        host=args.host,
        port=args.port,
        workers=args.workers if not args.reload else 1,
        reload=args.reload,
        log_level=args.log_level.lower(),
    )


if __name__ == "__main__":
    main()
