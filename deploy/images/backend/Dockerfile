FROM python:3.6-alpine

RUN apk add --no-cache --virtual .build-deps \
    gcc

RUN pip install pipenv

ADD ./src/backend /app
ADD ./deploy/images/backend/gunicorn.conf.py /conf/

WORKDIR /app

RUN pipenv install --system

CMD ["gunicorn", "-c", "/conf/gunicorn.conf.py", "app:app"]