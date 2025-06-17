# 构建阶段：使用官方 uv 镜像构建应用
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# 设置 uv 环境变量
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# 设置工作目录
WORKDIR /app

# 使用缓存和绑定挂载安装依赖（不安装项目本身）
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# 复制项目代码（使用 .dockerignore 排除不需要的文件）
COPY . .

# 安装项目（非开发模式，适合生产环境）
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# 生产阶段：使用匹配的 Python 基础镜像
FROM python:3.12-slim-bookworm AS runtime

# 从构建阶段复制应用程序
COPY --from=builder /app /app

# 设置 PATH 包含虚拟环境
ENV PATH="/app/.venv/bin:$PATH"

# 设置工作目录
WORKDIR /app

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["bge-reranker-server", "--host", "0.0.0.0", "--port", "8000"] 
