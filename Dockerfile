FROM python:alpine3.8


COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt


COPY . /app
WORKDIR /app



ENTRYPOINT ["./gunicorn_starter.sh"]