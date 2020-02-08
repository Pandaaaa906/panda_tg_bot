FROM python:3.6
COPY . /app
WORKDIR /app
RUN mkdir ~/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" | tee ~/.pip/pip.conf
RUN pip install -r requirments
CMD [ "python", "tg_sticker_bot/run.py" ]
