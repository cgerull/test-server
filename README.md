# Echo Server

Simple test server for orchestration and deployment testing.

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

Welcome to the demo webserver

Local server time is 2021-01-08 11:49:21.861499
The server ip is: 10.0.18.4
The container name is 27f2a1769ce1
The secret key is SwarmEtcdSecret

Your request came from: 10.255.0.2
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

"PORT=8080"
'LOGFORMAT="%(h)s %(l)s %(t)s %({Server-IP}o)s %(l)s %(r)s %(s)s %(b)s %(a)s"'
"LOGLVL=INFO"
"SECRET_KEY=DockerComposeSecret"
```