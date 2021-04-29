#!/bin/sh
#
    gunicorn wsgi:app \
    --bind="0.0.0.0:5000" \
    --workers=2 \
    --access-logformat="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s" \
    --access-logfile="-" \
    --error-logfile="-" \
    --log-level="INFO"
