import os

import pytest

from letscountit.db.db import Database
from letscountit.db.edgedb import Database as EdgeDatabase
from edgedb import Client
from uuid import uuid4, UUID

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

def test_get_db_connection_edge_object():
    """Test getting an edgedb database connection"""
    db_obj = Database()
    assert isinstance(db_obj, object)

def test_get_edge_db_client():
    """Test getting an edgedb database client"""
    db_obj = EdgeDatabase()
    assert isinstance(db_obj.client, Client)

def test_edge_db_query(hex_str_to_uuid_str):
    """Testing querying the edgedb database"""
    db_obj = EdgeDatabase()
    uuid = str(uuid4())
    db_obj.query("""
        INSERT counter{
                 uuid := <uuid>$uuid, 
                 name := <str>$name
                 } 
        """, uuid=uuid, name="test")
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid)
    db_uuid = hex_str_to_uuid_str(row.uuid.hex)
    assert  db_uuid == uuid
    assert row.name == "test"
    db_obj.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid)
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid)
    assert row is None

def test_edgedb_insert_counter(uuid_value, hex_str_to_uuid_str):
    """Test inserting a counter into the edgedb database"""
    db_obj = EdgeDatabase()
    db_obj.insert_counter(uuid_value, "test")
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    db_uuid = hex_str_to_uuid_str(row.uuid.hex)
    assert  db_uuid == uuid_value
    assert row.name == "test"
    db_obj.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    assert row is None

def test_edgedb_insert_counter_no_uuid():
    """Test inserting a counter into the edgedb database without a uuid"""
    db_obj = EdgeDatabase()
    with pytest.raises(TypeError):
        db_obj.insert_counter(None, "test")

def test_edgedb_insert_counter_no_name():
    """Test inserting a counter into the edgedb database without a name"""
    db_obj = EdgeDatabase()
    with pytest.raises(TypeError):
        db_obj.insert_counter(str(uuid4()), None)

def test_edgedb_update_counter(uuid_value):
    """Test updating a counter in the edgedb database"""
    db_obj = EdgeDatabase()
    db_obj.insert_counter(uuid_value, "test")
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    db_obj.update_counter(uuid_value, 1)
    row =  db_obj.query("SELECT counter{uuid, count} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    assert row[0].count == 1
    db_obj.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    assert len(row) == 0

def test_edgedb_get_counter_by_id(uuid_value, hex_str_to_uuid_str):
    """Test getting a counter by id from the edgedb database"""
    db_obj = EdgeDatabase()
    counter = db_obj.insert_counter(uuid_value, "test")
    counter_id = counter.id.hex
    result = db_obj.get_counter_by_id(counter_id)
    assert hex_str_to_uuid_str(result.uuid.hex) == uuid_value
    assert result.name == "test"
    assert result.count == 0
    db_obj.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    assert row is None

def test_edgedb_create_counter():
    """Test creating a counter in the edgedb database"""
    db_obj = EdgeDatabase()
    counter = db_obj.create_counter("test")
    counter_id = counter.id.hex
    assert counter.name == "test"
    assert counter.count == 0
    assert counter.uuid is not None
    assert isinstance(counter.uuid, UUID)
    db_obj.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=counter.uuid)
    row =  db_obj.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=counter.uuid)
    assert row is None

def test_edgedb_create_counter_no_name():
    """Test creating a counter in the edgedb database without a name"""
    db_obj = EdgeDatabase()
    with pytest.raises(TypeError):
        db_obj.create_counter(None)
