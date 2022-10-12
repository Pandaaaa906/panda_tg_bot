FROM python:3.8 AS sticker_bot_base
RUN mkdir -p ~/.pip \
    && echo "[global]\nindex-url = https://pypi.mirrors.ustc.edu.cn/simple/" | tee ~/.pip/pip.conf \
    && git config --global http.sslverify false \
    && sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y python3-opencv
COPY requirments.txt /tmp/requirments.txt
RUN pip install -r /tmp/requirments.txt

FROM sticker_bot_base

COPY sticker_bot /sticker_bot
WORKDIR /sticker_bot
RUN mkdir -p /logs
ENTRYPOINT [ "python", "run.py" ]
