# define the name of the virtual environment directory
VENV := .venv
REGISTRY := cgerull
IMAGE := testserver
TAG := 0.8.1
PY_FILES := test_server/*.py
TEMPLATES := test_server/TEMPLATES/*

# default target, when make executed without arguments
# all: push
help:           ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install_modules:
	pip install --upgrade pip &&\
	pip install -r dev-requirements.txt

lint:
	pylint --disable=R,C,E0237,E1101 test_server

test:
	pytest -vv --junitxml=test-results.xml --cov-report term-missing --cov=test_server tests/test_*.py

format:
	black *.py

testserver.tar: Dockerfile $(PY_FILES) $(TEMPLATES)	## Build docker image and save as archive
	docker build -t testserver:latest .
	@docker save testserver -o testserver-latest.tar;

scan: 	testserver.tar	## Scan docker image
	@docker load -i testserver-latest.tar
	docker scan testserver:latest

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
