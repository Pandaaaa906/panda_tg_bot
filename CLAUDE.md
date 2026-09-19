# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Telegram bot (built on **Telethon**, MTProto — not python-telegram-bot) that converts images sent "as file" into Telegram-sticker-ready PNGs (max 512px), replying with the result as a document. Python 3.12, packaged with **uv** (`uv.lock` committed, `uv.lock` is authoritative; the legacy `requirments.txt` is stale — do not use it).

## Commands

- Install deps: `uv sync`
- Run locally: `uv run --no-sync -m sticker_bot.run` (requires a populated `.env` — see below)
- Docker: `docker compose up -d --build`
- There are **no tests and no lint/format tooling configured**.

## Configuration

All config is env vars read in `sticker_bot/settings.py`, loaded from `.env` (gitignored):
`api_id`, `api_hash`, `bot_token`, `owner_username` (lowercase), `APP_NAME`, `PROXY_HOST`, `PROXY_PORT`.

**Import-time side effects:** importing `sticker_bot.settings` immediately builds *and connects* the Telethon client (`settings.py:22-26`). `PROXY_PORT` is parsed with `int(getenv('PROXY_PORT'))` at module level, so importing anything without a complete `.env` crashes. Likewise `run.py:17` attaches a loguru sink at the hardcoded Unix path `/app/logs/sticker_bot.log`, which fails at import on Windows unless that absolute path is creatable on the current drive.

## Architecture

Everything lives in `sticker_bot/` (~4 modules):

- `settings.py` — global `client` (Telethon `TelegramClient`), created at import time with optional SOCKS5 proxy. Session files persist in `sticker_bot/session/` (gitignored `*.session`).
- `run.py` — entry point; registers all handlers on the shared `client` and runs `client.run_until_disconnected()`.
  - Catch-all message handler (`run.py:36`) gated by decorators from `utils.py` (`private_chat_only`, `attachment_required`, `with_limited_file_size(8MB)`) replies with inline buttons for resize method. The seam-carving button is owner-gated via a list-slice trick (`run.py:48-55`): `f=1` when the sender isn't `owner_username` (hiding the second button), `f=2` otherwise.
  - `CallbackQuery` handler downloads media to `BytesIO`, validates with `telethon.utils.is_image`, then runs the resize in a **per-request `ProcessPoolExecutor`** (`run.py:90-91`) so numba/JIT-heavy work doesn't block the event loop. Result is re-encoded with `cv2.imencode('.png', ...)` and sent with `force_document=True`.
- `resize_tools.py` — `normal_resize` (plain cv2 fit-within-512) and `seam_carving_resize`. Note the ratio condition in the seam path (`resize_tools.py:26`) is inverted relative to `normal_resize` (`resize_tools.py:35`) — intentional downscale-then-carve, not a bug.
- `seam_carving.py` — vendored content-aware resizing with `@jit` (numba) decorators; numba warnings are suppressed globally (`seam_carving.py:21`). First call pays JIT warmup, hence the "(Very Slow)" button label. Also runnable as a CLI.
- `utils.py` — handler decorators and media helpers.

## Known issues / gotchas

- **Docker layout:** the image copies the package to `/app/sticker_bot/` and relies on `uv run --no-sync -m sticker_bot.run` finding it via the working directory — `WORKDIR /app` must stay *before* `uv sync` in the Dockerfile, otherwise the venv is created in `/` and the runtime venv comes up empty.
- OpenCV is pinned to the headless builds (`opencv-contrib-python-headless`) — the code never needs GUI libs; only core functions (`imdecode`/`imread`/`resize`/`imencode`) are used.
- Env var naming is inconsistent by design: lowercase (`api_id`, `bot_token`) vs uppercase (`PROXY_HOST`).
