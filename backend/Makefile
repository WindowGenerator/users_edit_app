SERVICE_DIR = backend
SRC_DIR = $(SERVICE_DIR)/src
VENV = $(SERVICE_DIR)/.venv

HOST = 0.0.0.0
PORT = 80

create-venv:
	python3.9 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r $(SERVICE_DIR)/requirements.txt -r $(SERVICE_DIR)/requirements.dev.txt


start-dev:
	cd backend \
		&& uvicorn src.main:app 
			--host $(HOST) 
			--port $(PORT) 
			--reload
	

format:
	isort --apply --recursive $(SRC_DIR)
	black --skip-string-normalization $(SRC_DIR)