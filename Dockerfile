FROM python:3.8

WORKDIR /home

RUN pip install -U pip requests
COPY *.py ./

ARG api_key
ENV API_KEY $api_key

ENTRYPOINT ["python", "server.py"]

