.PHONY: install lint test-unit test-e2e test ci clean

install:
	pip install -r requirements.txt

lint:
	python -m compileall src

test-unit:
	pytest tests/unit -v --cov=src --cov-config=.coveragerc --cov-report=term

test-e2e:
	chmod +x scripts/e2e.sh
	./scripts/e2e.sh

test: lint test-unit test-e2e

ci: install test

clean:
	rm -f usage.db
	pkill -9 -f uvicorn || true
