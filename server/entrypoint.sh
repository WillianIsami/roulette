#! /usr/bin/sh
python3 api/manage.py migrate

exec "$@"
