.PHONY: test docker-build docker-run docker-stop

test:
	echo "Running tests..."
	poetry run python -m unittest discover -v -s tests

docker-build:
	echo "Building Docker image..."
	docker build -t px-kvstore:latest .

docker-run: docker-build
	echo "Ensuring 'kvstore-data' volume exists..."
	docker volume create kvstore-data
	echo "Running server with a persistent named volume..."
	docker run -d --name kvstore-app -p 8000:8000 -v kvstore-data:/data px-kvstore:latest

docker-stop:
	echo "Stopping and removing Docker container..."
	docker stop kvstore-app
	docker rm kvstore-app 