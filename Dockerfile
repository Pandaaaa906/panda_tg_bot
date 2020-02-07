FROM python:3.6
COPY . /app
WORKDIR /app/tg_sticker_bot
RUN python run.py
