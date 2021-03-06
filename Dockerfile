FROM python:3.6 AS sticker_bot_base
RUN mkdir ~/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" | tee ~/.pip/pip.conf
COPY requirments /tmp/requirments
RUN pip install -r /tmp/requirments

FROM sticker_bot_base

COPY sticker_bot /sticker_bot
WORKDIR /sticker_bot
RUN mkdir -p /logs
ENTRYPOINT [ "python", "run.py" ]
