
PYTHON_BINARY ?= $(shell which python3.10)
PYENV_PATH 	  := ./venv/bin/python3.10

.PHONY: venv
venv:
	$(PYTHON_BINARY) -m venv venv
	$(PYENV_PATH) -m pip install --upgrade pip

.PHONY: setup-dev-env
setup-dev-env: venv
	$(PYENV_PATH) -m pip install -r requirements-dev.txt

.PHONY: setup-test-env
setup-test-env: venv
	$(PYENV_PATH) -m pip install -r requirements-test.txt

.PHONY: delete-venv
delete-venv:
	rm -rf ./venv

.PHONY: run-laptop-pipeline
run-laptop-pipeline:
	$(PYENV_PATH) datasets/laptop-dataset/laptop_dataset_pipeline.py

.PHONY: run
run:
	$(PYENV_PATH) gen2rec/src/recommendation_engine.py

.PHONY: start-vecdb
start-vecdb:
	docker run -p 6333:6333 -p 6334:6334 -v $(shell pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant