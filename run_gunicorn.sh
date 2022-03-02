#!/bin/sh
#
# Init database if defined
export FLASK_ENVIRONMENT=development
export FLASK_APP=test_server
export DB_TYPE=sqlite
flask init-db 

# Start the application server
gunicorn wsgi:app \
    --bind="0.0.0.0:8080" \
    --workers=2 \
    # --worker-class=gevent \
    --timeout=90 \
    --access-logformat="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s" \
    --access-logfile="-" \
    --error-logfile="-" \
    --log-level="INFO"
