from faker import Faker
import pytest
from pytest import FixtureRequest
from testcontainers.postgres import PostgresContainer

from settings import Settings
from db.connection import Connection
from customers.customers import delete_all_customers


@pytest.fixture(scope='session', autouse=True)
def setup(request: FixtureRequest):
    postgres = PostgresContainer("postgres:16-alpine")
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)

    settings = Settings(
        pg_host=postgres.get_container_host_ip(),
        pg_port=postgres.get_exposed_port(5432),
        pg_username=postgres.username,
        pg_password=postgres.password,
        pg_database=postgres.dbname
    )

    conn = Connection.init(settings)
    conn.init_db()


@pytest.fixture(scope='function', autouse=True)
def cleanup_per_test():
    yield
    delete_all_customers()


@pytest.fixture(scope='session')
def faker():
    faker = Faker()
    faker.seed_instance(0)
    yield faker
