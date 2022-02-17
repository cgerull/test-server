FROM alpine:3.15
# Use alpine linux as base image

RUN apk --no-cache add \
    gcc \
    python3 \
    python3-dev \
    py3-pip \
    libc-dev \
    libffi-dev \
    openssl-dev \
    curl \
 && adduser --disabled-password web \
 && mkdir -p /home/web/log/ \
 && chown -R web.web /home/web/

USER web
WORKDIR /home/web
COPY app /home/web/app
COPY requirements.txt run_gunicorn.sh wsgi.py /home/web/

ENV PATH=$PATH:/home/web/.local/bin \
    PORT=8080 \
    ERRLOG="-" \
    ACCESSLOG="-" \
    LOGFORMAT="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s" \
    LOGLVL=INFO \
    SECRET_KEY=DockerFileSecret

# Install application
RUN pip install --user -r requirements.txt

EXPOSE 8080

CMD sh run_gunicorn.sh

HEALTHCHECK --interval=15s --timeout=5s --retries=5 CMD curl --fail http://localhost:8080/ping || exit 1