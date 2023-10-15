
PYTHON_BINARY ?= $(shell which python3.10)
PYENV_PATH 	  := ./venv/bin/python3.10

.PHONY: venv
venv:
	$(PYTHON_BINARY) -m venv venv

.PHONY: setup-dev-env
setup-dev-env: venv
	$(PYENV_PATH) -m pip install -r requirements-dev.txt

.PHONY: setup-test-env
setup-test-env: venv
	$(PYENV_PATH) -m pip install -r requirements-test.txt

.PHONY: setup-chat-interface
setup-chat-interface:
	$(PYENV_PATH) -m pip install -r chat-interface/requirements.txt

.PHONY: setup-evaluation-system
setup-evaluation-system:
	$(PYENV_PATH) -m pip install -r evaluation-system/requirements.txt

.PHONY: setup-prompt-constructor
setup-prompt-constructor:
	$(PYENV_PATH) -m pip install -r prompt-constructor/requirements.txt

.PHONY: setup-recommendation-engine
setup-recommendation-engine:
	$(PYENV_PATH) -m pip install -r recommendation-engine/requirements.txt

.PHONY: delete-venv
delete-venv:
	rm -rf ./venv
