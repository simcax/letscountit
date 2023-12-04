import os

import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer

from letscountit.db.db import Database


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(
        str(pytestconfig.rootdir), "letscountit", "tests", "docker-compose.yml"
    )


@pytest.fixture(scope="session")
def db_connection(docker_services, docker_ip):
    """
    :param docker_services: pytest-docker plugin fixture
    :param docker_ip: pytest-docker plugin fixture
    :return: psycopg2 connection class
    """
    db_settings = {
        "database": "test_database",
        "user": "root",
        "host": docker_ip,
        "password": "",
        "port": docker_services.port_for("crdb", 26257),
        "application_name": "letscountit",
        "sslmode": "disable",
    }
    # dbc = psycopg2.connect(**db_settings)
    try:
        dbc = psycopg2.connect(**db_settings)
        dbc.autocommit = True
        return dbc
    except psycopg2.DatabaseError as error:
        conn = False
        print("Error connecting to database %s - %s", db_settings["database"], error)
        return conn


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
    pg_port = 5432
    try:
        with PostgresContainer("postgres:16.1").with_bind_ports(
            pg_port, pg_port
        ) as postgres:
            db_obj = Database()
            db_obj.db_settings["database"] = postgres.POSTGRES_DB
            db_obj.db_settings["user"] = postgres.POSTGRES_USER
            db_obj.db_settings["host"] = "localhost"
            db_obj.db_settings["port"] = pg_port
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
