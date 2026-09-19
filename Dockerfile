FROM python:3.12-slim AS sticker_bot_base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1 \
    UV_CACHE_DIR=/tmp/.uv/ \
    UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple" \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_DEV=1

# 创建虚拟环境并安装Python依赖
RUN --mount=type=cache,target=/tmp/.uv/ \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# 激活虚拟环境
ENV PATH="/app/.venv/bin:$PATH"

FROM sticker_bot_base

COPY sticker_bot /app/sticker_bot/
COPY pyproject.toml /app/

RUN mkdir -p /app/logs

ENTRYPOINT [ "uv", "run", "--no-sync", "-m", "sticker_bot.run" ]
