# TestServer

Simple test server for orchestration and deployment testing.

[![CircleCI](https://circleci.com/gh/cgerull/test-server/tree/development.svg?style=svg)](https://circleci.com/gh/cgerull/test-server/tree/development)
![Code Quality](https://github.com/cgerull/test-server/actions/workflows/codeql-analysis.yml/badge.svg)
![CodeQL](https://github.com/cgerull/test-server/actions/workflows/codeql-analysis.yml/badge.svg)
![Tests](https://github.com/cgerull/test-server/actions/workflows/unit-tests.yml/badge.svg)
![Publish](https://github.com/cgerull/test-server/actions/workflows/docker-publish.yml/badge.svg)
![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=flat&logo=dependabot&logoColor=white)

## Usage


### Docker

Use the local-testing/docker-compose file to build and run the test server as a container locally.

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


Welcome to Test server
Your request was
remote_addr: 172.22.0.1
url: http://localhost:4080/echo
url_charset: utf-8
referrer: None
user_agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15
App version Testserver version is 0.9.8
Running in Production environment

This page has been viewed 4 times.
```

The value of the secret key depends on the place of definition.

### REST interface

Send a GET request with your favorite REST client (cUrl, insomnia, postman).

```bash

curl http://192.168.99.109:8080/api/echo
{"container_name":"d89af7728f6d","local_ip":"10.0.18.3","now":"2020-01-08 11:53:24.647791","remote_ip":"10.255.0.2","secret":"SwarmEtcdSecret\n"}
```

### Server parameters

Default configuration via test_server/test_server.cfg.

Runtime configuration via environment variables.

| Variable        | Value.               |
| --------------- | -------------------- |
| PORT            | 8080                 |
| ENV             | Development          |
| SECRET_KEY      | MySecretKey          |
| DEBUG           | False                |
| LOGLVL          | INFO                 |
