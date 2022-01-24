SERVICE_DIR = backend
SRC_DIR = $(SERVICE_DIR)/src
VENV = $(SERVICE_DIR)/.venv
LOGS = $(SERVICE_DIR)/.logs

HOST = 0.0.0.0
PORT = 80

TEST_POSTGRES_NAME = test-postgres

create-venv:
	python3.9 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r $(SERVICE_DIR)/requirements.txt


start-dev:
	mkdir -p $(LOGS) \
		&& cd backend \
		&& uvicorn src.main:app 
			--host $(HOST) 
			--port $(PORT) 
			--reload

stop-dev:
	docker stop $(TEST_POSTGRES_NAME)

start-postgres-dev:
	docker run --rm \
		--name $(TEST_POSTGRES_NAME) \
		-e POSTGRES_PASSWORD=secret \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_DB=users_db \
		-p 5432:5432 \
		-d postgres