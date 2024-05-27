
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

.PHONY: run

.PHONY: run-ui
run-ui:
	streamlit run gen2rec/user-interface/chat_interface.py


.PHONY: run-book-ui
run-book-ui:
	python gen2rec/user-interface/client_interface.py --category "BOOK" --server_port 8001

.PHONY: run-game-ui
run-game-ui:
	python gen2rec/user-interface/client_interface.py --category "GAME" --server_port 8002

.PHONY: run-house-ui
run-house-ui:
	python gen2rec/user-interface/client_interface.py --category "HOUSE" --server_port 8003

.PHONY: run-laptop-ui
run-laptop-ui:
	python gen2rec/user-interface/client_interface.py --category "LAPTOP" --server_port 8004

.PHONY: run-movie-ui
run-movie-ui:
	python gen2rec/user-interface/client_interface.py --category "MOVIE" --server_port 8005

.PHONY: run-music-ui
run-music-ui:
	python gen2rec/user-interface/client_interface.py --category "MUSIC" --server_port 8006

.PHONY: run-news-ui
run-news-ui:
	python gen2rec/user-interface/client_interface.py --category "NEWS" --server_port 8007

.PHONY: run-vehicle-ui
run-vehicle-ui:
	python gen2rec/user-interface/client_interface.py --category "VEHICLE" --server_port 8008
