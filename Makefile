.PHONY: install test lint suite api frontend clean
install:
	python3 -m pip install -e '.[dev]'
test:
	pytest
lint:
	ruff check backend tests
suite:
	agentshield suite
api:
	uvicorn agentshield.api:app --app-dir backend --reload
frontend:
	cd frontend && npm run dev
clean:
	rm -f agentshield.db
	rm -rf reports .pytest_cache
