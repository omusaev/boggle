#!/bin/sh

# TODO: wait-for-it.sh
# postgres is slow, just wait a bit
sleep 15
alembic -c ./alembic/alembic.ini upgrade head

gunicorn -c /conf/gunicorn.conf.py app:app
