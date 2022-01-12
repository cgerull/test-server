# define the name of the virtual environment directory
VENV := venv
REGISTRY := cgerull
IMAGE := test-server
TAG =: 0.8.1
PY_FILES := app/*.py
TEMPLATES := app/TEMPLATES/*

# default target, when make executed without arguments
# all: push
help:           ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C,E0237,E1101 test_server

test:
	pytest -vv --cov-report term-missing --cov=test_server tests/test_*.py

format:
	black *.py

test-server: Dockerfile $(PY_FILES) $(TEMPLATES)	## Build docker image and save as archive
	docker build -t test-server .
	@docker save test-server -o test-server.tar;

scan: 	test-server	## Scan docker image
	@docker load -i test-server.tar
	docker scan test-server

push:	scan		## Push to registry, parameters are REGISTRY, IMAGE and TAG
	@docker load -i test-server.tar
	@docker tag test-server $(REGISTRY)/$(IMAGE):$(TAG)
	docker push $(REGISTRY)/$(IMAGE):$(TAG)

clean:		## Clean all artefacts
	find . -type f -name '*.pyc' -delete
	rm test-server.tar

all: install lint test test-server.tar scan push clean   ## Run all commands

build: test-server scan push clean

.PHONY: all venv run clean scan push help zsh bash
