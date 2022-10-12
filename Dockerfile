FROM python:3.8 AS sticker_bot_base
RUN mkdir ~/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" | tee ~/.pip/pip.conf
RUN apt-get update && apt-get install -y python3-opencv
COPY requirments.txt /tmp/requirments.txt
RUN pip install -r /tmp/requirments.txt

FROM sticker_bot_base

COPY sticker_bot /sticker_bot
WORKDIR /sticker_bot
RUN mkdir -p /logs
ENTRYPOINT [ "python", "run.py" ]
