FROM python:3-alpine
MAINTAINER Nikolay Konovalov <konovalov.nk@gmail.com>

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN apk update && \
 apk add --no-cache inotify-tools && \
 apk add --no-cache procps && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN pip install -r requirements.txt
ADD . /app/

RUN chmod +x /app/start.sh

EXPOSE 8005
