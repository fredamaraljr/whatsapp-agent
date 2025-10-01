ifeq (,$(wildcard .env))
$(error .env file is missing. Please create one based on .env.example)
endif

include .env

CHECK_DIRS := .

ava-build:
	docker compose build

ava-run:
	docker compose up --build -d

ava-stop:
	docker compose stop

ava-delete:
	@if exist "long_term_memory" rmdir /s /q "long_term_memory"
	@if exist "short_term_memory" rmdir /s /q "short_term_memory"
	@if exist "generated_images" rmdir /s /q "generated_images"
	docker compose down

format-fix:
	uv run ruff format $(CHECK_DIRS) 
	uv run ruff check --select I --fix $(CHECK_DIRS)

lint-fix:
	uv run ruff check --fix $(CHECK_DIRS)

format-check:
	uv run ruff format --check $(CHECK_DIRS) 
	uv run ruff check -e $(CHECK_DIRS)
	uv run ruff check --select I -e $(CHECK_DIRS)

lint-check:
	uv run ruff check $(CHECK_DIRS)