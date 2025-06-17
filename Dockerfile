# 构建阶段：使用轻量级镜像安装依赖（适合GitHub Actions资源限制）
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# 设置 uv 环境变量
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# 安装必要的编译工具（最小化安装）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装CPU版本的PyTorch（避免下载大型CUDA包）
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev --extra-index-url https://download.pytorch.org/whl/cpu

# 复制项目代码
COPY . .

# 安装项目
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --extra-index-url https://download.pytorch.org/whl/cpu

# 运行阶段：使用最小的Python镜像
FROM python:3.12-slim AS runtime

# 从构建阶段复制Python环境和应用
COPY --from=builder /app /app

# 设置 PATH 包含虚拟环境
ENV PATH="/app/.venv/bin:$PATH"

# 设置工作目录
WORKDIR /app

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["bge-reranker-server", "--host", "0.0.0.0", "--port", "8000"] 
