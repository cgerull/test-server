# define the name of the virtual environment directory
VENV := venv
REGISTRY = cgerull
IMAGE = test-server
TAG = 0.5.0
PY_FILES = app/*.py
TEMPLATES = app/TEMPLATES/*

# default target, when make executed without arguments
# all: push
help:           ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: requirements.txt	## Create python venv
	python3 -m venv $(VENV)
	source ./$(VENV)/bin/activate
	./$(VENV)/bin/pip install --update pip
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: ## Activate venv environment
	source ./$(VENV)/bin/activate	

test-server.tar : Dockerfile $(PY_FILES) $(TEMPLATES)	## Build docker image and save as archive
	docker build -t test-server .
	@docker save test-server -o test-server.tar

scan : 	test-server.tar		## Scan docker image
	@docker load -i test-server.tar
	docker scan test-server

push:	scan		## Push to registry, parameters are REGISTRY, IMAGE and TAG
	@docker load -i test-server.tar
	@docker tag test-server $(REGISTRY)/$(IMAGE):$(TAG)
	docker push $(REGISTRY)/$(IMAGE):$(TAG)

run: venv 		## Run local flask development server
	./$(VENV)/bin/python -m flask run

clean:		## Clean all artefacts
	if [ $(which deactivate) ]; then
	  deactivate
	fi
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	rm test-server.tar

.PHONY: all venv run clean scan push help
