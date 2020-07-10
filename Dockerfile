FROM python:3.6 AS tg_sticker_bot_base
COPY . /app
WORKDIR /app
RUN mkdir ~/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" | tee ~/.pip/pip.conf
RUN pip install -r requirments

FROM tg_sticker_bot_base

WORKDIR /app/tg_sticker_bot
RUN mkdir -p /logs
ENV PROXY_HOST=192.168.1.2
ENV PROXY_PORT=8087
ENTRYPOINT [ "python", "run.py" ]
