#!/bin/sh

alembic -c ./alembic/alembic.ini upgrade head

gunicorn -c /conf/gunicorn.conf.py app:app
