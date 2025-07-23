.PHONY: test docker-build docker-run docker-stop

test:
	echo "Running tests..."
	poetry run python -m unittest discover -v -s tests

docker-build:
	echo "Building Docker image..."
	docker build -t px-kvstore:latest .

docker-run: docker-build
	echo "Running server in detached Docker container..."
	docker run -d --name kvstore-app -p 8000:8000 px-kvstore:latest

docker-stop:
	echo "Stopping and removing Docker container..."
	docker stop kvstore-app || true
	docker rm kvstore-app || true 