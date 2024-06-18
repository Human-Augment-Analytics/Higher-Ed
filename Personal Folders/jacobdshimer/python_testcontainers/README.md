# Python Testcontainers Example

Before running, follow these steps:

1. Create a new python 3.12.3 environment.
2. Install all of the requirements with `pip install -r requirements.txt`.
3. Startup the postgres container with `docker compose up -d`

To run the main.py, use the following command: `PG_HOST=localhost PG_PORT=5432 PG_USERNAME=postgres PG_PASSWORD=example PG_DATABASE=postgres python main.py`

To run the pytest, use the following command: `PYTHONPATH=. pytest`
