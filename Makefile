.PHONY: test test-all test-unit test-integration test-manual test-coverage test-pyglet test-fast test-headless install-test clean help

help:			## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-test:		## Install test dependencies
	pip install -r tests/requirements-test.txt

test:			## Run all tests (excluding manual tests)
	cd tests && pytest --ignore=manual -v

test-all:		## Run all tests including manual tests
	cd tests && pytest -v

test-unit:		## Run only unit tests
	cd tests && pytest unit/ -v -m unit

test-integration:	## Run only integration tests  
	cd tests && pytest integration/ -v -m integration

test-manual:		## Run manual/visual tests
	cd tests/manual && python test_visual_transformations.py

test-pyglet:		## Run pyglet compatibility tests
	cd tests && pytest --ignore=manual -v -m pyglet

test-coverage:		## Run tests with coverage report
	cd tests && pytest --ignore=manual --cov=pycat --cov-report=html --cov-report=term-missing

test-fast:		## Run tests excluding slow tests
	cd tests && pytest --ignore=manual -v -m "not slow"

test-headless:		## Run tests in headless mode (for CI)
	cd tests && python -m pytest --ignore=manual -v --tb=short

clean:			## Clean up test artifacts
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
