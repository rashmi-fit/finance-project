.PHONY: help install test run clean

help:
	@echo "Finance Analytics - Spark Project"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run unit tests"
	@echo "  make run        - Run the main application"
	@echo "  make clean      - Clean generated files"

install:
	pip install -r requirements.txt

test:
	pytest src/test/python/ -v

run:
	python src/main/python/finance_analytics.py

clean:
	rm -rf .pytest_cache spark-warehouse metastore_db derby.log
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
