# 构建阶段：使用 PyTorch CUDA 开发镜像
FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-devel AS builder

# 设置环境变量避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive

# 从官方 uv 镜像复制二进制文件（推荐的最佳实践）
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

# 设置 uv 环境变量
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# 设置工作目录
WORKDIR /app

# 安装GPU版本的依赖（使用默认PyTorch GPU版本）
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# 复制项目代码
COPY . .

# 安装项目
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# 运行阶段：使用 PyTorch CUDA 运行时镜像
FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime AS runtime

# 设置环境变量避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive

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
