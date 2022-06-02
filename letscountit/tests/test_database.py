import pytest
import os
from letscountit.db.db import Database

def test_get_db_connection():
    os.environ['ENV'] = "TEST"
    db_obj = Database()
    conn = db_obj.connect()
    assert isinstance(conn, object)
    assert conn != None

def test_connect_db(_mock_db_connection):
    os.environ['ENV'] = "TEST"
    db_obj = Database()
    #db_obj.db_settings['database'] = 'letscountit_local'
    db_obj.db_settings['user'] = 'root'
    db_obj.db_settings['host'] = 'localhost'
    db_obj.db_settings['port'] = 26257
    db_obj.db_settings['password'] = ''
    db_obj.db_settings['application_name'] = 'letscountit'
    db_obj.db_settings['sslmode'] = 'disable'
    conn = db_obj.connect()
    sql = "CREATE DATABASE IF NOT EXISTS letscountit"
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()

