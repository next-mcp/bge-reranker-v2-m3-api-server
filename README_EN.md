# BGE Reranker v2-m3 API Server

> English | [中文](README.md)

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

High-performance multilingual text reranking FastAPI service based on [BAAI BGE Reranker v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) model.

## 🌟 Project Background

BGE Reranker v2-m3 is an advanced multilingual text reranking model developed by Beijing Academy of Artificial Intelligence (BAAI). The model features:

- **Multilingual Support**: Supports Chinese, English, and other languages
- **High Performance**: Optimized based on bge-m3 model with fast inference speed
- **Lightweight**: Relatively small model size, easy to deploy
- **Powerful Reranking Capability**: Excellent performance on multiple evaluation benchmarks

This project wraps the model as a FastAPI service, providing simple and easy-to-use HTTP API interfaces for integration into various application scenarios.

## ✨ Key Features

- 🚀 **High-performance FastAPI Service**: Asynchronous processing with high concurrency support
- 🌍 **Multilingual Reranking**: Supports Chinese, English, and other languages
- 📊 **Flexible Parameter Configuration**: Supports score normalization, return count limiting, etc.
- 🔧 **Complete Development Toolchain**: Integrated with ruff, pyright, pytest
- 📦 **Convenient Installation and Deployment**: Supports source code installation and Docker deployment
- 📖 **Complete Documentation and Examples**: Provides detailed usage documentation and code examples
- 🔄 **Automated CI/CD**: GitHub Actions automated testing and release

## 📦 Installation

### Source Code Installation

```bash
git clone https://github.com/yourusername/bge-reranker-v2-m3-api-server.git
cd bge-reranker-v2-m3-api-server

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies (including all dev and production dependencies)
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install pre-commit hooks
bge-reranker-pre-commit-install
```

## 🚀 Quick Start

### Starting the Service

Start the service using command line:

```bash
bge-reranker-server --host 0.0.0.0 --port 8000
```

Or using Python module:

```bash
python -m bge_reranker_v2_m3_api_server.cli --host 0.0.0.0 --port 8000
```

### Basic Usage

After the service starts, you can perform text reranking through HTTP API:

```python
import httpx

async def rerank_example():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/rerank",
            json={
                "query": "什么是人工智能？",
                "documents": [
                    "人工智能是计算机科学的一个分支。",
                    "今天天气很好。",
                    "机器学习是人工智能的核心技术。"
                ],
                "top_k": 2
            }
        )
        return response.json()
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "人工智能技术",
    "documents": [
      "深度学习是人工智能的重要分支",
      "今天的天气很不错",
      "机器学习算法在AI中应用广泛"
    ]
  }'
```

## 📚 API Documentation

### Health Check

**GET** `/health`

Check service status and model loading status.

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "0.1.0",
  "model_name": "BAAI/bge-reranker-v2-m3"
}
```

### Document Reranking

**POST** `/rerank`

Rerank documents.

#### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ | - | Query text |
| `documents` | array[string] | ✅ | - | List of documents to be ranked |
| `top_k` | integer | ❌ | null | Number of results to return, null means return all |
| `normalize` | boolean | ❌ | true | Whether to normalize scores using sigmoid function |
| `return_documents` | boolean | ❌ | true | Whether to return document content in results |

#### Response Format

```json
{
  "results": [
    {
      "index": 0,
      "score": 0.9234,
      "document": "Document content..."
    }
  ],
  "query": "Query text",
  "total_documents": 3,
  "returned_results": 2,
  "processing_time_ms": 45.67
}
```

### Interactive Documentation

After the service starts, visit the following addresses to view complete API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Local Development

### Environment Setup

```bash
# Clone project
git clone https://github.com/yourusername/bge-reranker-v2-m3-api-server.git
cd bge-reranker-v2-m3-api-server

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install pre-commit hooks
bge-reranker-pre-commit-install
```

### Code Checks

The project provides preset script commands:

```bash
# Code formatting
bge-reranker-format

# Code quality check
bge-reranker-lint

# Run tests
bge-reranker-test

# Execute all checks (formatting + lint + type check + tests)
bge-reranker-check

# Update pre-commit repositories
bge-reranker-pre-commit-update
```

### Development Mode Startup

```bash
# Start development server (supports hot reload)
bge-reranker-server --reload --log-level DEBUG
```

## 🧪 Testing

### Running Tests

Using preset script commands:

```bash
# Run tests (including coverage report)
bge-reranker-test
```

### Testing API

```bash
# Run example script
python examples/basic_usage.py

# Or view cURL examples
cat examples/curl_examples.md
```

## 🐳 Docker Deployment

### Using Pre-built Image (Recommended)

```bash
# Pull latest stable version
docker pull yarnovo/bge-reranker-v2-m3-api-server:latest

# Run container
docker run -d \
  --name bge-reranker-server \
  -p 8000:8000 \
  -v ./models:/root/.cache/huggingface/hub \
  --restart unless-stopped \
  yarnovo/bge-reranker-v2-m3-api-server:latest
```

### Using Docker Compose (Recommended)

**Basic deployment:**
```bash
# Start service using predefined configuration
docker compose up -d

# View logs
docker compose logs -f bge-reranker
```

**Start service:**
```bash
# Start service
docker compose up -d

# View logs
docker compose logs -f

# Stop service
docker compose down
```

### Local Build

```bash
# Build image
docker build -t bge-reranker-v2-m3-api-server .

# Run
docker run -d \
  --name bge-reranker-server \
  -p 8000:8000 \
  -v ./models:/root/.cache/huggingface/hub \
  bge-reranker-v2-m3-api-server
```

### Docker Configuration

#### Environment Variables

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `BGE_MODEL_NAME` | `BAAI/bge-reranker-v2-m3` | BGE model name or path |
| `BGE_USE_FP16` | `true` | Whether to use FP16 for inference acceleration |
| `BGE_DEVICE` | `auto` | Device selection (auto/cpu/cuda) |
| `UVICORN_HOST` | `0.0.0.0` | Bind host |
| `UVICORN_PORT` | `8000` | Bind port |

#### Volume Mounting

- `./models:/root/.cache/huggingface/hub` - Cache downloaded model files
- `./logs:/app/logs` - Log file persistence

#### Health Check

Built-in health check monitors service status through `/health` endpoint:

```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' bge-reranker-server
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `BGE_MODEL_NAME` | `BAAI/bge-reranker-v2-m3` | BGE model name or path |
| `BGE_USE_FP16` | `true` | Whether to use FP16 for inference acceleration |

### Command Line Arguments

```bash
bge-reranker-server --help
```

## 📊 Performance Optimization

### Inference Acceleration

- **FP16**: Enable half-precision inference (enabled by default)
- **Batch Processing**: API supports batch processing of multiple documents
- **Model Caching**: Model remains in memory after loading

### Memory Optimization

- Use `--workers 1` to avoid multiple processes loading the model repeatedly
- Adjust batch size based on available GPU memory

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork this project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

### Development Standards

- Use ruff for code formatting and checking
- Use pyright for type checking
- Add corresponding test cases
- Update documentation and examples

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [BAAI](https://www.baai.ac.cn/) for providing the excellent BGE Reranker v2-m3 model
- [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) project for model implementation
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance web framework

## 📞 Support

If you encounter issues or have suggestions, please:

- Check [GitHub Issues](https://github.com/yourusername/bge-reranker-v2-m3-api-server/issues)
- Create a new Issue
- Review project documentation and examples

---

**Note**: Model files (approximately 568MB) need to be downloaded on first startup. Please ensure a stable network connection. 
