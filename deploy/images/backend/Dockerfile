FROM python:3.6-alpine

RUN apk add --no-cache --virtual .build-deps \
    gcc

RUN pip install pipenv

ADD ./deploy/images/backend/gunicorn.conf.py /conf/
ADD ./deploy/images/backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD ./src/backend /app

WORKDIR /app

RUN pipenv install --system

ENTRYPOINT ["/entrypoint.sh"]