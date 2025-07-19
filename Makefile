.PHONY: test test-unit test-integration test-coverage test-pyglet install-test clean help

help:			## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-test:		## Install test dependencies
	pip install -r requirements-test.txt

test:			## Run all tests
	pytest tests/ -v

test-unit:		## Run only unit tests
	pytest tests/unit/ -v -m unit

test-integration:	## Run only integration tests  
	pytest tests/integration/ -v -m integration

test-pyglet:		## Run pyglet compatibility tests
	pytest tests/ -v -m pyglet

test-coverage:		## Run tests with coverage report
	pytest tests/ --cov=pycat --cov-report=html --cov-report=term-missing

test-fast:		## Run tests excluding slow tests
	pytest tests/ -v -m "not slow"

test-headless:		## Run tests in headless mode (for CI)
	PYGLET_HEADLESS=1 pytest tests/ -v

clean:			## Clean up test artifacts
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
