#!/bin/sh
#
    gunicorn wsgi:app \
    --bind="0.0.0.0:${PORT}" \
    --workers=2 \
    --access-logformat="${LOGFORMAT}" \
    --access-logfile="-" \
    --error-logfile="-" \
    --log-level="${LOGLVL}"
