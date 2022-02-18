# TestServer

Simple test server for orchestration and deployment testing.

[![CircleCI](https://circleci.com/gh/cgerull/test-server/tree/development.svg?style=svg)](https://circleci.com/gh/cgerull/test-server/tree/development)
## Usage

### Docker 
Use the docker-compose file to build and run the test server as a container locally.

For swarm testing use the docker-stack.yml configuration. Change to the image value to use your own, customized images.

In Swarm mode you can to add a secret with:

```bash

echo SwarmEtcdSecret | docker secret create my_secret_key -
```

## Server

### HTML response

Point your browser to `http://<name or ip>:8080/`.
The server returns an page with this information:

```bash

Welcome to Testserver
Local server time is 2021-02-25 10:11:37.775058
The server ip is: 192.168.178.40
Platform: macOS-11.2.1-arm64-arm-64bit
System: Darwin
Processor: arm
Architecture: 64bit 
The container name is localhost
The secret key is Only_the_default_secret_key

Your request came from: 127.0.0.1
```

The value of the secret key depends on the place of definition.

### REST interface

Send a GET request with your favorite REST client (cUrl, insomnia, postman).

```bash

curl http://192.168.99.109:8080/api/echo
{"container_name":"d89af7728f6d","local_ip":"10.0.18.3","now":"2020-01-08 11:53:24.647791","remote_ip":"10.255.0.2","secret":"SwarmEtcdSecret\n"}
```

### Server parameters

Configuration by setting environment variables.

```bash

"CONFIG_FILE = ./srv-config.yml"
"PORT=8080"
'LOGFORMAT="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s"'
"LOGLVL=INFO"
"SECRET_KEY=DockerComposeSecret"
# Secret file will overrule SECRET_KEY
"SECRET_FILE=/run/secrets/my_secret_key"
"REDIS_URL = localhost:6379"

```