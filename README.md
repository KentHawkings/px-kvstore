# PhysicsX Tech Test Submission by Kent Hawkings

This project is a simple key-value store built in Python, exposing a RESTful HTTP interface for CRUD operations. The entire implementation relies solely on Python's standard library, with no external dependencies.

## Getting Started

### Prerequisites

- Python 3.7+
- Docker

### Running the Server Locally with Docker

1. **Build the Docker image**:

    ```sh
    make docker-build
    ```

2. **Run the Docker container**:

    ```sh
    make docker-run
    ```

    The server will be accessible at `http://localhost:8000`.

## Testing the Solution

To run the tests, execute the following command from the root of the project:

```sh
make test
```

This command will discover and run all tests in the `tests` directory.

## API Usage

You can interact with the key-value store using any HTTP client, such as `curl`.

- **Create/Update a key-value pair**:

    ```sh
    curl -X POST -H "Content-Type: application/json" -d '{"value": "your_value"}' http://localhost:8000/store/your_key
    ```

- **Retrieve a value by key**:

    ```sh
    curl http://localhost:8000/your_key
    ```

- **Delete a key**:

    ```sh
    curl -X DELETE http://localhost:8000/your_key
    ```


## Incomplete Features

While I've implemented a DB to allow for persistence our our key-value store I wasn't able to finish the implementation in time. As such the app defaults to using the in-memory DB which means data doesn't actually persist between runs. I don't think this would take long to fix at all but it has knock-on effects on the tests and requires updating the makefile to ensure our directory is mounted.