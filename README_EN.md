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

### 🏷️ Version Management

The project uses `uv` as a one-stop package manager, supporting automatic version management similar to npm functionality.

#### View Current Version

```bash
# View project current version
uv version

# View detailed version information (JSON format)
uv version --output-format json
```

#### Update Version Number

Using semantic versioning, supports automatic updates to version numbers in `pyproject.toml`:

```bash
# Increment patch version (1.0.0 -> 1.0.1)
uv version --bump patch

# Increment minor version (1.0.1 -> 1.1.0)  
uv version --bump minor

# Increment major version (1.1.0 -> 2.0.0)
uv version --bump major

# Set specific version number
uv version 1.2.3
```

#### Version Number Format Specification

The project follows **PEP 440** version specification, with format: `[N!]N(.N)*[{a|b|rc}N][.postN][.devN]`

**Version Type Details:**

- **Stable versions**: `1.0.0`, `2.1.3` - Official release versions
- **Pre-release versions**: Include the following types
  - **Alpha versions**: `1.0.0a1`, `1.0.0a2` - Early development versions, features may be incomplete
  - **Beta versions**: `1.0.0b1`, `1.0.0b2` - Features basically complete, undergoing testing
  - **Release Candidate**: `1.0.0rc1`, `1.0.0rc2` - Release candidate version, close to final version
  - **Development versions**: `1.0.0.dev1`, `1.0.0.dev2` - Development versions, used for builds during development
  - **Post-release versions**: `1.0.0.post1`, `1.0.0.post2` - Fix versions, for small fixes to released versions

#### Pre-release Version Management

The project fully supports **PEP 440** standard pre-release version numbers:

```bash
# Alpha version (1.0.0 -> 1.0.0a1)
uv version 1.0.0a1

# Beta version (1.0.0a1 -> 1.0.0b1)  
uv version 1.0.0b1

# Release Candidate version (1.0.0b1 -> 1.0.0rc1)
uv version 1.0.0rc1

# Development version (for continuous development)
uv version 1.0.0.dev1

# Post-release version (for small fixes)
uv version 1.0.0.post1
```

#### Release Process Best Practices

1. **Development Phase**:
   ```bash
   # Development versions
   uv version 1.1.0.dev1
   uv version 1.1.0.dev2
   ```

2. **Pre-release Phase**:
   ```bash
   # Alpha testing
   uv version 1.1.0a1
   uv version 1.1.0a2
   
   # Beta testing  
   uv version 1.1.0b1
   uv version 1.1.0b2
   
   # Release Candidate
   uv version 1.1.0rc1
   ```

3. **Official Release**:
   ```bash
   # Stable version
   uv version 1.1.0
   ```

#### Version and Docker Tag Correspondence

- **Stable versions** (e.g., `1.0.0`): Push both `1.0.0` and `latest` tags
- **Pre-release versions**: **Only push version number tags and `prerelease` tag**, do not push `latest`
  - Alpha versions (e.g., `v1.0.0a1`, `v1.0.0a2`): Push `1.0.0a1` and `prerelease`
  - Beta versions (e.g., `v1.0.0b1`, `v1.0.0b2`): Push `1.0.0b1` and `prerelease`
  - RC versions (e.g., `v1.0.0rc1`, `v1.0.0rc2`): Push `1.0.0rc1` and `prerelease`
  - Dev versions (e.g., `v1.0.0.dev1`, `v1.0.0.dev2`): Push `1.0.0.dev1` and `prerelease`
  - Post versions (e.g., `v1.0.0.post1`, `v1.0.0.post2`): Push `1.0.0.post1` and `prerelease`

This ensures the `latest` tag always points to the latest stable version, while the `prerelease` tag points to the latest pre-release version, ensuring pre-release versions don't affect production environment users.

#### Automated Workflow

Complete release process combined with Git tags:

```bash
# 1. Update version number
uv version --bump minor  # e.g.: 1.0.0 -> 1.1.0

# 2. Commit version changes
git add pyproject.toml
git commit -m "chore: bump version to $(uv version --short)"

# 3. Create Git tag
git tag "v$(uv version --short)"

# 4. Push code and tags
git push origin main
git push origin "v$(uv version --short)"

# 5. Publish Docker image (automatically uses version from pyproject.toml)
./scripts/publish-docker-utf8.bat
```

#### Using Preview Mode

Preview version changes before actually modifying:

```bash
# Preview version changes (don't actually modify files)
uv version --bump patch --dry-run
uv version 2.0.0 --dry-run
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

### Manual Build and Publish to Docker Hub

If you need to build multi-platform images or custom configurations, you can manually build and publish to Docker Hub:

#### 1. Preparation

```bash
# Login to Docker Hub
docker login

# Set image name (replace with your Docker Hub username)
export DOCKER_USERNAME=your-docker-username
export IMAGE_NAME=$DOCKER_USERNAME/bge-reranker-v2-m3-api-server
export VERSION=latest  # or specify version like v1.0.0
```

#### 2. Single Platform Build (Recommended for quick testing)

```bash
# Build AMD64 image
docker build -t $IMAGE_NAME:$VERSION-amd64 .

# Push image
docker push $IMAGE_NAME:$VERSION-amd64

# Create and push latest tag
docker tag $IMAGE_NAME:$VERSION-amd64 $IMAGE_NAME:latest
docker push $IMAGE_NAME:latest
```

#### 3. Multi-Platform Build (requires buildx)

```bash
# Create and use buildx builder
docker buildx create --use --name multiplatform-builder
docker buildx inspect --bootstrap

# Build and push multi-platform image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $IMAGE_NAME:$VERSION \
  -t $IMAGE_NAME:latest \
  --push .

# Verify image is pushed
docker buildx imagetools inspect $IMAGE_NAME:$VERSION
```

#### 4. Complete Publish Script

Create a publish script `scripts/publish-docker.sh`:

```bash
#!/bin/bash
set -e

# Configuration
DOCKER_USERNAME=${DOCKER_USERNAME:-"your-docker-username"}
IMAGE_NAME="$DOCKER_USERNAME/bge-reranker-v2-m3-api-server"
VERSION=${1:-"latest"}

echo "🚀 Starting Docker image build and publish..."
echo "Image name: $IMAGE_NAME"
echo "Version tag: $VERSION"

# Check if logged into Docker Hub
if ! docker info | grep -q "Username"; then
    echo "❌ Please login to Docker Hub first: docker login"
    exit 1
fi

# Check if buildx is supported
if ! docker buildx version > /dev/null 2>&1; then
    echo "⚠️  buildx not available, using single platform build"
    
    # Single platform build
    echo "🔨 Building AMD64 image..."
    docker build -t $IMAGE_NAME:$VERSION .
    
    echo "📤 Pushing image..."
    docker push $IMAGE_NAME:$VERSION
    
    if [ "$VERSION" != "latest" ]; then
        docker tag $IMAGE_NAME:$VERSION $IMAGE_NAME:latest
        docker push $IMAGE_NAME:latest
    fi
else
    echo "🔨 Multi-platform building..."
    
    # Create buildx builder (if not exists)
    if ! docker buildx ls | grep -q multiplatform-builder; then
        docker buildx create --use --name multiplatform-builder
        docker buildx inspect --bootstrap
    else
        docker buildx use multiplatform-builder
    fi
    
    # Multi-platform build and push
    TAGS="-t $IMAGE_NAME:$VERSION"
    if [ "$VERSION" != "latest" ]; then
        TAGS="$TAGS -t $IMAGE_NAME:latest"
    fi
    
    docker buildx build \
      --platform linux/amd64,linux/arm64 \
      $TAGS \
      --push .
fi

echo "✅ Image publish completed!"
echo "📋 View image info:"
echo "   docker pull $IMAGE_NAME:$VERSION"
echo "   docker buildx imagetools inspect $IMAGE_NAME:$VERSION"
```

**Using the publish script:**

**Linux/macOS:**
```bash
# Give script execute permission
chmod +x scripts/publish-docker.sh

# Publish latest version
./scripts/publish-docker.sh

# Publish specific version
./scripts/publish-docker.sh v1.0.0
```

**Windows:**
```bat
REM Publish latest version
scripts\publish-docker.bat

REM Publish specific version
scripts\publish-docker.bat v1.0.0
```

#### 5. Verify Publish Results

```bash
# Check image info
docker buildx imagetools inspect $IMAGE_NAME:$VERSION

# Pull and test image
docker pull $IMAGE_NAME:$VERSION
docker run --rm -p 8000:8000 $IMAGE_NAME:$VERSION

# Test API
curl http://localhost:8000/health
```

#### 6. Publishing Notes

- **First publish**: Ensure the corresponding repository is created on Docker Hub
- **Version tags**: Recommend using semantic versioning (like v1.0.0)
- **Image size**: Multi-platform builds will increase overall image size
- **Network environment**: Building requires downloading PyTorch image (~8GB), ensure stable network
- **Resource requirements**: Multi-platform builds require more CPU and memory resources

#### 7. Automated Publishing (Optional)

If you want to automate the publishing process, consider:

- **GitHub Actions**: Trigger builds only on tag pushes
- **GitLab CI/CD**: Use GitLab's Docker registry
- **Docker Hub auto-build**: Connect GitHub repository for automatic builds

**GitHub Actions example configuration (tag-triggered only):**

```yaml
# In .github/workflows/docker-publish.yml
name: Publish Docker Image

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/bge-reranker-v2-m3-api-server:latest
            ${{ secrets.DOCKER_USERNAME }}/bge-reranker-v2-m3-api-server:${{ github.ref_name }}
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
