import pytest
import psycopg2
import os
import letscountit.db.db

@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir),'letscountit','tests', "docker-compose.yml")

@pytest.fixture(scope='session')
def db_connection(docker_services, docker_ip):
    """
    :param docker_services: pytest-docker plugin fixture
    :param docker_ip: pytest-docker plugin fixture
    :return: psycopg2 connection class
    """
    db_settings = {
        'database'        : 'test_database',
        'user'            : 'root',
        'host'            : docker_ip,
        'password'        : '',
        'port'            : docker_services.port_for('crdb', 26257),
        'application_name': 'letscountit',
        'sslmode'         : 'disable',
    }
    #dbc = psycopg2.connect(**db_settings)
    try:
        dbc = psycopg2.connect(**db_settings)
    except psycopg2.DatabaseError as error:
        conn = False
        print("Error connecting to database %s - %s",db_settings['database'], error)
    dbc.autocommit = True
    return dbc


@pytest.fixture(autouse=True)
def _mock_db_connection(mocker, db_connection):
    """
    This will alter application database connection settings, once and for all the tests
    in unit tests module.
    :param mocker: pytest-mock plugin fixture
    :param db_connection: connection class
    :return: True upon successful monkey-patching
    """
    mocker.patch('letscountit.db.db', db_connection)
    return True