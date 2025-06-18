# BGE Reranker v2-m3 API Server

> [English](README_EN.md) | 中文

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

基于 [BAAI BGE Reranker v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) 模型的高性能多语言文本重排序 FastAPI 服务。

## 🌟 项目背景

BGE Reranker v2-m3 是由北京人工智能研究院（BAAI）开发的先进的多语言文本重排序模型。该模型具有以下特点：

- **多语言支持**：支持中文、英文及其他多种语言
- **高性能**：基于 bge-m3 模型优化，推理速度快
- **轻量级**：模型体积相对较小，易于部署
- **强大的重排序能力**：在多个评测基准上表现优异

本项目将该模型封装为 FastAPI 服务，提供简单易用的 HTTP API 接口，方便集成到各种应用场景中。

## ✨ 主要特性

- 🚀 **高性能 FastAPI 服务**：异步处理，支持高并发
- 🌍 **多语言重排序**：支持中英文及其他多种语言
- 📊 **灵活的参数配置**：支持分数归一化、返回数量限制等
- 🔧 **完整的开发工具链**：集成 ruff、pyright、pytest
- 📦 **便捷的安装部署**：支持 pip 安装和 Docker 部署
- 📖 **完整的文档和示例**：提供详细的使用文档和代码示例
- 🔄 **自动化 CI/CD**：GitHub Actions 自动化测试和发布

## 📦 安装

### 从源码安装

```bash
git clone https://github.com/yourusername/bge-reranker-v2-m3-api-server.git
cd bge-reranker-v2-m3-api-server

# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖（包含所有开发和生产依赖）
uv sync

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 安装 pre-commit 钩子
bge-reranker-pre-commit-install
```

## 🚀 快速开始

### 启动服务

使用命令行启动服务：

```bash
bge-reranker-server --host 0.0.0.0 --port 8000
```

或者使用 Python 模块：

```bash
python -m bge_reranker_v2_m3_api_server.cli --host 0.0.0.0 --port 8000
```

### 基本使用

服务启动后，可以通过 HTTP API 进行文本重排序：

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

### cURL 示例

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

## 📚 API 文档

### 健康检查

**GET** `/health`

检查服务状态和模型加载情况。

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "0.1.0",
  "model_name": "BAAI/bge-reranker-v2-m3"
}
```

### 文档重排序

**POST** `/rerank`

对文档进行重排序。

#### 请求参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 查询文本 |
| `documents` | array[string] | ✅ | - | 待排序的文档列表 |
| `top_k` | integer | ❌ | null | 返回的结果数量，null表示返回全部 |
| `normalize` | boolean | ❌ | true | 是否使用sigmoid函数归一化分数 |
| `return_documents` | boolean | ❌ | true | 是否在结果中返回文档内容 |

#### 响应格式

```json
{
  "results": [
    {
      "index": 0,
      "score": 0.9234,
      "document": "文档内容..."
    }
  ],
  "query": "查询文本",
  "total_documents": 3,
  "returned_results": 2,
  "processing_time_ms": 45.67
}
```

### 交互式文档

服务启动后，访问以下地址查看完整的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ 本地开发

### 环境准备

```bash
# 克隆项目
git clone https://github.com/yourusername/bge-reranker-v2-m3-api-server.git
cd bge-reranker-v2-m3-api-server

# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装所有依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 安装 pre-commit hooks
bge-reranker-pre-commit-install
```

### 🏷️ 版本管理

项目使用 `uv` 作为一站式包管理器，支持自动版本管理类似 npm 的功能。

#### 查看当前版本

```bash
# 查看项目当前版本
uv version

# 查看详细版本信息（JSON格式）
uv version --output-format json
```

#### 更新版本号

使用语义化版本控制，支持自动更新 `pyproject.toml` 中的版本号：

```bash
# 增加补丁版本 (1.0.0 -> 1.0.1)
uv version --bump patch

# 增加次版本 (1.0.1 -> 1.1.0)  
uv version --bump minor

# 增加主版本 (1.1.0 -> 2.0.0)
uv version --bump major

# 设置具体版本号
uv version 1.2.3
```

#### 预发布版本管理

项目完全支持 **PEP 440** 标准的预发布版本号，包括：

```bash
# Alpha 版本 (1.0.0 -> 1.0.0a1)
uv version 1.0.0a1

# Beta 版本 (1.0.0a1 -> 1.0.0b1)  
uv version 1.0.0b1

# Release Candidate 版本 (1.0.0b1 -> 1.0.0rc1)
uv version 1.0.0rc1

# 开发版本 (用于持续开发)
uv version 1.0.0.dev1
```

#### 发布流程最佳实践

1. **开发阶段**：
   ```bash
   # 开发版本
   uv version 1.1.0.dev1
   uv version 1.1.0.dev2
   ```

2. **预发布阶段**：
   ```bash
   # Alpha 测试
   uv version 1.1.0a1
   uv version 1.1.0a2
   
   # Beta 测试  
   uv version 1.1.0b1
   uv version 1.1.0b2
   
   # Release Candidate
   uv version 1.1.0rc1
   ```

3. **正式发布**：
   ```bash
   # 正式版本
   uv version 1.1.0
   ```

#### 版本与Docker标签的对应关系

- **正式版本**（如 `1.0.0`）：同时推送 `1.0.0` 和 `latest` 标签
- **预发布版本**（如 `1.0.0a1`, `1.0.0b1`, `1.0.0rc1`）：**仅推送版本号标签**，不推送 `latest`

这确保 `latest` 标签始终指向最新的稳定版本，而预发布版本不会影响生产环境的用户。

#### 自动化工作流

结合 Git 标签的完整发布流程：

```bash
# 1. 更新版本号
uv version --bump minor  # 例如：1.0.0 -> 1.1.0

# 2. 提交版本更改
git add pyproject.toml
git commit -m "chore: bump version to $(uv version --short)"

# 3. 创建 Git 标签
git tag "v$(uv version --short)"

# 4. 推送代码和标签
git push origin main
git push origin "v$(uv version --short)"

# 5. 发布 Docker 镜像（自动使用 pyproject.toml 中的版本号）
./scripts/publish-docker-utf8.bat
```

#### 使用预览模式

在实际修改前预览版本变更：

```bash
# 预览版本变更（不实际修改文件）
uv version --bump patch --dry-run
uv version 2.0.0 --dry-run
```

### 代码检查

项目提供了预设的脚本命令：

```bash
# 代码格式化
bge-reranker-format

# 代码质量检查
bge-reranker-lint

# 运行测试
bge-reranker-test

# 执行所有检查（格式化 + lint + 类型检查 + 测试）
bge-reranker-check

# 更新 pre-commit 仓库
bge-reranker-pre-commit-update
```

### 开发模式启动

```bash
# 启动开发服务器（支持热重载）
bge-reranker-server --reload --log-level DEBUG
```

## 🧪 测试

### 运行测试

使用预设的脚本命令：

```bash
# 运行测试（包含覆盖率报告）
bge-reranker-test
```

或者直接使用 pytest：

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=bge_reranker_v2_m3_api_server --cov-report=html

# 运行特定测试文件
pytest tests/test_models.py -v
```

### 测试 API

```bash
# 运行示例脚本
python examples/basic_usage.py

# 或查看 cURL 示例
cat examples/curl_examples.md
```

## 🐳 Docker 部署

### 使用预构建镜像（推荐）

```bash
# 拉取最新稳定版本
docker pull yarnovo/bge-reranker-v2-m3-api-server:latest

# 运行容器
docker run -d \
  --name bge-reranker-server \
  -p 8000:8000 \
  -v ./models:/root/.cache/huggingface/hub \
  --restart unless-stopped \
  yarnovo/bge-reranker-v2-m3-api-server:latest
```

### 使用 Docker Compose（推荐）

**基础部署：**
```bash
# 使用预定义配置启动服务
docker compose up -d

# 查看日志
docker compose logs -f bge-reranker
```

**启动服务：**
```bash
# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

### 本地构建

```bash
# 构建镜像
docker build -t bge-reranker-v2-m3-api-server .

# 运行
docker run -d \
  --name bge-reranker-server \
  -p 8000:8000 \
  -v ./models:/root/.cache/huggingface/hub \
  bge-reranker-v2-m3-api-server
```

### 手动构建和发布到Docker Hub

如果您需要构建多平台镜像或自定义配置，可以手动构建并发布到Docker Hub：

#### 1. 准备工作

```bash
# 登录Docker Hub
docker login

# 设置镜像名称（替换为您的Docker Hub用户名）
export DOCKER_USERNAME=your-docker-username
export IMAGE_NAME=$DOCKER_USERNAME/bge-reranker-v2-m3-api-server
export VERSION=latest  # 或者指定版本号如 v1.0.0
```

#### 2. 单平台构建（推荐用于快速测试）

```bash
# 构建AMD64镜像
docker build -t $IMAGE_NAME:$VERSION-amd64 .

# 推送镜像
docker push $IMAGE_NAME:$VERSION-amd64

# 创建并推送latest标签
docker tag $IMAGE_NAME:$VERSION-amd64 $IMAGE_NAME:latest
docker push $IMAGE_NAME:latest
```

#### 3. 多平台构建（需要buildx）

```bash
# 创建并使用buildx构建器
docker buildx create --use --name multiplatform-builder
docker buildx inspect --bootstrap

# 构建并推送多平台镜像
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $IMAGE_NAME:$VERSION \
  -t $IMAGE_NAME:latest \
  --push .

# 验证镜像已推送
docker buildx imagetools inspect $IMAGE_NAME:$VERSION
```

#### 4. 完整的发布脚本

创建一个发布脚本 `scripts/publish-docker.sh`：

```bash
#!/bin/bash
set -e

# 配置
DOCKER_USERNAME=${DOCKER_USERNAME:-"your-docker-username"}
IMAGE_NAME="$DOCKER_USERNAME/bge-reranker-v2-m3-api-server"
VERSION=${1:-"latest"}

echo "🚀 开始构建和发布Docker镜像..."
echo "镜像名称: $IMAGE_NAME"
echo "版本标签: $VERSION"

# 检查是否已登录Docker Hub
if ! docker info | grep -q "Username"; then
    echo "❌ 请先登录Docker Hub: docker login"
    exit 1
fi

# 检查是否支持多平台构建
if ! docker buildx version > /dev/null 2>&1; then
    echo "⚠️  buildx不可用，使用单平台构建"
    
    # 单平台构建
    echo "🔨 构建AMD64镜像..."
    docker build -t $IMAGE_NAME:$VERSION .
    
    echo "📤 推送镜像..."
    docker push $IMAGE_NAME:$VERSION
    
    if [ "$VERSION" != "latest" ]; then
        docker tag $IMAGE_NAME:$VERSION $IMAGE_NAME:latest
        docker push $IMAGE_NAME:latest
    fi
else
    echo "🔨 多平台构建中..."
    
    # 创建buildx构建器（如果不存在）
    if ! docker buildx ls | grep -q multiplatform-builder; then
        docker buildx create --use --name multiplatform-builder
        docker buildx inspect --bootstrap
    else
        docker buildx use multiplatform-builder
    fi
    
    # 多平台构建并推送
    TAGS="-t $IMAGE_NAME:$VERSION"
    if [ "$VERSION" != "latest" ]; then
        TAGS="$TAGS -t $IMAGE_NAME:latest"
    fi
    
    docker buildx build \
      --platform linux/amd64,linux/arm64 \
      $TAGS \
      --push .
fi

echo "✅ 镜像发布完成！"
echo "📋 查看镜像信息："
echo "   docker pull $IMAGE_NAME:$VERSION"
echo "   docker buildx imagetools inspect $IMAGE_NAME:$VERSION"
```

**使用发布脚本：**

**Linux/macOS:**
```bash
# 给脚本执行权限
chmod +x scripts/publish-docker.sh

# 发布latest版本
./scripts/publish-docker.sh

# 发布指定版本
./scripts/publish-docker.sh v1.0.0
```

**Windows:**
```bat
REM 方式1：英文版本（推荐，避免乱码）
scripts\publish-docker.bat

REM 方式2：中文UTF-8版本
scripts\publish-docker-utf8.bat

REM 方式3：PowerShell版本（推荐，支持彩色输出和中文）
powershell -ExecutionPolicy Bypass -File scripts\publish-docker-simple.ps1

REM 发布指定版本
scripts\publish-docker.bat v1.0.0
powershell -ExecutionPolicy Bypass -File scripts\publish-docker-simple.ps1 -Version v1.0.0
```

#### 5. 验证发布结果

```bash
# 检查镜像信息
docker buildx imagetools inspect $IMAGE_NAME:$VERSION

# 拉取并测试镜像
docker pull $IMAGE_NAME:$VERSION
docker run --rm -p 8000:8000 $IMAGE_NAME:$VERSION

# 测试API
curl http://localhost:8000/health
```

#### 6. 发布注意事项

- **首次发布**：确保在Docker Hub上已创建对应的仓库
- **版本标签**：建议使用语义化版本号（如 v1.0.0）
- **镜像大小**：多平台构建会增加总体镜像大小
- **网络环境**：构建时需要下载PyTorch镜像（约8GB），确保网络稳定
- **资源需求**：多平台构建需要更多CPU和内存资源

#### 7. 自动化发布（可选）

如果您想要自动化发布流程，可以考虑：

- **GitHub Actions**：仅在tag推送时触发构建
- **GitLab CI/CD**：使用GitLab的Docker registry
- **Docker Hub自动构建**：连接GitHub仓库自动构建

**GitHub Actions示例配置（仅tag触发）：**

```yaml
# 在.github/workflows/docker-publish.yml
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

### Docker 配置说明

#### 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `BGE_MODEL_NAME` | `BAAI/bge-reranker-v2-m3` | BGE 模型名称或路径 |
| `BGE_USE_FP16` | `true` | 是否使用 FP16 加速推理 |
| `BGE_DEVICE` | `auto` | 设备选择 (auto/cpu/cuda) |
| `UVICORN_HOST` | `0.0.0.0` | 绑定主机 |
| `UVICORN_PORT` | `8000` | 绑定端口 |

#### 数据卷挂载

- `./models:/root/.cache/huggingface/hub` - 缓存下载的模型文件
- `./logs:/app/logs` - 日志文件持久化

#### 健康检查

容器内置健康检查，通过 `/health` 端点监控服务状态：

```bash
# 检查容器健康状态
docker inspect --format='{{.State.Health.Status}}' bge-reranker-server
```

## ⚙️ 配置

### 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `BGE_MODEL_NAME` | `BAAI/bge-reranker-v2-m3` | BGE 模型名称或路径 |
| `BGE_USE_FP16` | `true` | 是否使用 FP16 加速推理 |

### 命令行参数

```bash
bge-reranker-server --help
```

## 📊 性能优化

### 推理加速

- **FP16**: 启用半精度推理（默认开启）
- **批处理**: API 支持批量处理多个文档
- **模型缓存**: 模型加载后常驻内存

### 内存优化

- 使用 `--workers 1` 避免多进程重复加载模型
- 根据可用 GPU 内存调整批处理大小

## 🤝 贡献

欢迎贡献代码！请按照以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发规范

- 使用 ruff 进行代码格式化和检查
- 使用 pyright 进行类型检查
- 添加相应的测试用例
- 更新文档和示例

## 📄 许可证

本项目基于 Apache 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [BAAI](https://www.baai.ac.cn/) 提供的优秀 BGE Reranker v2-m3 模型
- [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) 项目提供的模型实现
- [FastAPI](https://fastapi.tiangolo.com/) 提供的高性能 Web 框架

## 📞 支持

如果你遇到问题或有任何建议，请：

- 查看 [GitHub Issues](https://github.com/yourusername/bge-reranker-v2-m3-api-server/issues)
- 创建新的 Issue
- 查看项目文档和示例

---

**注意**: 首次启动时需要下载模型文件（约 568MB），请确保网络连接稳定。
