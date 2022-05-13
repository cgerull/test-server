#!/bin/sh
#
# Init database if defined
# export FLASK_ENV=development
# export FLASK_APP=test_server
# export DB_TYPE=sqlite
flask init-db 

# Start the application server
#     --worker-class=gevent \
NUM_WORKERS=2
TIMEOUT=120
gunicorn wsgi:app \
    --bind="0.0.0.0:8080" \
    --workers="${NUM_WORKERS}" \
    --timeout="${TIMEOUT}" \
    --access-logformat="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s" \
    --access-logfile="-" \
    --error-logfile="-" \
    --log-level="INFO"
