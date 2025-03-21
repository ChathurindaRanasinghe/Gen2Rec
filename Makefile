
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




.PHONY: run-ui
run-ui:
	python fe/client_interface.py

.PHONY: run-laptop-ui
run-laptop-ui:
	panel serve fe/usecases/laptop_usecase.py

.PHONY: run-movie-ui
run-movie-ui:
	panel serve fe/usecases/movie_usecase.py

.PHONY: run-news-ui
run-news-ui:
	panel serve fe/usecases/news_usecase.py


# .PHONY: start-vecdb
# start-vecdb:
# 	docker run -p 6333:6333 -p 6334:6334 -v $(shell pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant

.PHONY: start-redis
start-redis:
	docker run -d -p 6379:6379 -p 8001:8001 -v $(shell pwd)/redis-local-data/:/data redis/redis-stack:latest

.PHONY: run
run:
	fastapi run be/api.py

# export PYTHONPATH="${PYTHONPATH}:$(pwd)"

