# 单阶段构建：使用 PyTorch 官方镜像（已包含Python 3.12和所有AI依赖）
FROM nvcr.io/nvidia/pytorch:24.12-py3

# 安装 uv 包管理器
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

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

# 设置 PATH 包含虚拟环境
ENV PATH="/app/.venv/bin:$PATH"

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["bge-reranker-server", "--host", "0.0.0.0", "--port", "8000"] 
