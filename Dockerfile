FROM python:3.8

WORKDIR /home

RUN pip install -U pip requests && \
    pip install -U gunicorn
COPY *.py ./

ARG api_key
ENV API_KEY $api_key

ENTRYPOINT ["gunicorn"  , "-b", "0.0.0.0:8123", "server:application"]
