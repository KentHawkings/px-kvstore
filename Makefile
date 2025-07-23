.PHONY: test

test:
	echo "Running tests..."
	poetry run python -m unittest discover -v -s tests 