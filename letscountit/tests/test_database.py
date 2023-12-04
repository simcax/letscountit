import os

import pytest

from letscountit.db.db import Database


def test_get_db_connection(db_conn):
    os.environ["ENV"] = "TEST"
    print(db_conn)
    assert isinstance(db_conn, object)


def test_connect_db(db_conn):
    os.environ["ENV"] = "TEST"
    db_obj = db_conn
    db_name = "letscountit"
    sql = f"SELECT 'CREATE DATABASE {db_name}' WHERE NOT EXISTS \
        (SELECT FROM pg_database WHERE datname = '{db_name}')"
    with db_obj.conn.cursor() as cur:
        cur.execute(sql)
        db_obj.conn.commit()
