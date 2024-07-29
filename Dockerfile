FROM alpine:3.20
# Use alpine linux as base image
ARG DOCKER_TAG

RUN apk update --no-cache \
 && apk upgrade --no-cache \
 && apk --no-cache add \
    python3 \
    py3-pip \
 && adduser --disabled-password web \
 && mkdir -p /home/web/log/ \
 && chown -R web.web /home/web/

USER web
WORKDIR /home/web
COPY --chown=web:web test_server /home/web/test_server
COPY --chown=web:web requirements.txt run_gunicorn.sh wsgi.py /home/web/

ENV PATH=$PATH:/home/web/.local/bin \
    VERSION=$DOCKER_TAG \
    PORT=8080 \
    ERRLOG="-" \
    ACCESSLOG="-" \
    LOGFORMAT="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s" \
    LOGLVL=INFO \
    SECRET_KEY=DockerFileSecret

# Install application
# RUN pip install --user -r requirements.txt --break-system-packages
RUN python3 -m venv venv \
 && . venv/bin/activate \
 && pip install --upgrade pip \
 && pip install -r requirements.txt


EXPOSE 8080

CMD sh run_gunicorn.sh

HEALTHCHECK --interval=15s --timeout=5s --retries=5 CMD wget --spider http://localhost:8080/health || exit 1
