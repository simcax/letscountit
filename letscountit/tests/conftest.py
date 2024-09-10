import os

import psycopg2
import pytest
from faker import Faker
from testcontainers.postgres import PostgresContainer

from letscountit.db.db import Database
from uuid import uuid4, UUID


fake = Faker()

pytest.db_user = fake.name()
pytest.db_password = fake.password()
pytest.db_port = 5432


@pytest.fixture()
def _mock_db_connection(mocker, db_connection):
    """
    This will alter application database connection settings, once and for all the tests
    in unit tests module.
    :param mocker: pytest-mock plugin fixture
    :param db_connection: connection class
    :return: True upon successful monkey-patching
    """
    mocker.patch("letscountit.db.db", db_connection)
    return True


@pytest.fixture(scope="session")
def db_conn():
    """
    Base test fixture to get a database connection.
    """

    try:
        with PostgresContainer(
            "postgres:16.1", user=pytest.db_user, password=pytest.db_password
        ).with_bind_ports(pytest.db_port, pytest.db_port) as postgres:
            db_obj = Database()
            db_obj.db_settings["database"] = postgres.POSTGRES_DB
            db_obj.db_settings["user"] = postgres.POSTGRES_USER
            db_obj.db_settings["host"] = "localhost"
            db_obj.db_settings["port"] = pytest.db_port
            db_obj.db_settings["password"] = postgres.POSTGRES_PASSWORD
            db_obj.db_settings["application_name"] = "letscountit"
            db_obj.db_settings["sslmode"] = "disable"
            db_obj.connect()
            yield db_obj
            db_obj.disconnect()
    except psycopg2.DatabaseError as error:
        conn = False
        print(f"Error connecting to database: {error}")
        yield conn

@pytest.fixture()
def uuid_value():
    """
    Base test fixture to get a UUID value.
    """
    return str(uuid4())

@pytest.fixture()
def hex_str_to_uuid_str():
    def hex_str_to_uuid_str(hex_uuid):
        return str(UUID(hex_uuid))
    return hex_str_to_uuid_str