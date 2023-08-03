# define the name of the virtual environment directory
VENV := .venv
REGISTRY := cgerull
IMAGE := testserver
BUILDX_PLATFORMS := "amd64 arm64 arm32make "
TAG := 0.9.8
PY_FILES := test_server/*.py
TEMPLATES := test_server/templates/*

# default target, when make executed without arguments
help:           	## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install_modules:	## Install development requirements
	pip install --upgrade pip &&\
	pip install -r requirements-dev.txt

lint:			## Run pylint
	pylint --disable=R,C,E0237,E1101,W0511 test_server

test:lint			## Execute python unit tests
	pytest -vv --junitxml=test-results.xml --cov-report term-missing --cov=test_server tests/test_*.py

run:test 			## Run application local in python
	export ENV=development && \
	export TOOLS_ENABLED=False && \
	./run_gunicorn.sh

format:
	black *.py

testserver.tar: Dockerfile $(PY_FILES) $(TEMPLATES)	## Build docker image and save as archive
	docker build -t testserver:latest .
	@docker save testserver -o testserver-latest.tar;

scan: 	testserver.tar	## Scan docker image
	@docker load -i testserver-latest.tar
	docker scout cves testserver:latest

push:	scan		## Push to registry, parameters are REGISTRY, IMAGE and TAG
	@docker load -i testserver-latest.tar
	@docker tag testserver:latest $(REGISTRY)/$(IMAGE):$(TAG)
	docker push $(REGISTRY)/$(IMAGE):$(TAG)

clean:		## Clean all artefacts
	find . -type f -name '*.pyc' -delete
	rm testserver.tar

all: install_modules lint test testserver.tar scan push clean   ## Run all commands

build: testserver.tar

cross-build:	## Build for configure architectures and pushes to docker hub.
	@docker buildx create --name mybuilder --use
	@docker buildx build --platform ${BUILDX_PLATFORMS} -t ${PROD_IMAGE} --push ./app

up:		## Run docker-compose and start the container
	@docker-compose up -d

down:		## Run docker-compose and stop the container
	@docker-compose down

check-health:	## Check if container is healthy
	sleep 15
	@docker ps | grep test-server | grep "(healthy)"

.PHONY: all venv run clean scan push help cross-build
