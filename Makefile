# define the name of the virtual environment directory
VENV := .venv
REGISTRY := cgerull
IMAGE := testserver
BUILDX_PLATFORMS := "amd64 arm64 arm32 "
TAG := 1.0.4
PY_FILES := test_server/*.py
TEMPLATES := test_server/templates/*

# default target, when make executed without arguments
help:           	## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv:			## Create a virtual environment
	@[ -d $(VENV) ] || (python3 -m venv $(VENV) && \
	echo "Virtual environment created in $(VENV)") || true
	@[ -z "$(VIRTUAL_ENV)" ] && (echo "Run '. $(VENV)/bin/activate' to activate the virtual environment"&& exit 1) || true

install:		## Install development requirements
	$(typeset -f deactivate > /dev/null) || (echo "No virtual environment active" && exit 1)
	pip install --upgrade pip &&\
	pip install -r requirements-dev.txt

lint:			## Run pylint
	@[ -z "$(VIRTUAL_ENV)" ] && (echo "No virtual environment active. Run 'source $(VENV)/bin/activate' first." && exit 1) || true
	pylint --disable=R,C,E0237,E1101,W0511 test_server

test:lint		## Execute python unit tests
	@[ -z "$(VIRTUAL_ENV)" ] && (echo "No virtual environment active. Run 'source $(VENV)/bin/activate' first." && exit 1) || true
	pytest -vv --junitxml=reports/test-results.xml --cov-report=html:reports --cov=test_server tests/test_*.py

run:test 		## Run application local in python
	@[ -z "$(VIRTUAL_ENV)" ] && (echo "No virtual environment active. Run 'source $(VENV)/bin/activate' first." && exit 1) || true
	export ENV=development && \
	export TOOLS_ENABLED=False && \
	./run_gunicorn.sh

testserver.tar: Dockerfile $(PY_FILES) $(TEMPLATES)	## Build docker image and save as archive
	@[ -d $(VENV) ] || (echo "Virtual environment not found, run 'make venv' first" && exit 1)
	@[ -x $(which docker) ] || (echo "Docker not found, please install or start Docker" && exit 1)
	docker build -t testserver:latest .
	@docker save testserver -o testserver-latest.tar;

scan: 	testserver.tar	## Scan docker image
	@docker load -i testserver-latest.tar
	docker scout cves testserver:latest


  ## Run all commands

push: scan 		## Build for configure architectures and pushes to docker hub.
	PROD_IMAGE=$(REGISTRY)/$(IMAGE):$(TAG)
	@docker buildx create --name mybuilder --append --use
	@docker buildx build --platform ${BUILDX_PLATFORMS} -t ${PROD_IMAGE} --push ./app

clean:		## Clean all artefacts
	find . -type f -name '*.pyc' -delete
	rm -f testserver.tar
	@deactivate || echo "No virtual environment to deactivate"
	rm -rf $(VENV)
	rm -rf reports
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf __pycache__
	rm -rf instance

all: venv install lint test scan push

.PHONY: all venv lint run clean scan push help
