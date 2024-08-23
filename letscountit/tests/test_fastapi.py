from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import api
from letscountit.db.edgedb import Database
import json
from uuid import UUID

def test_get_counter_by_uuid(uuid_value):
    app = api.app
    assert isinstance(app, object)
    client = TestClient(app)
    # Add a counter to the database directly
    db = Database()
    db.insert_counter(uuid_value, "test")
    # Now test we can retrieve it by the API
    test_url = f"/counter/{uuid_value}"
    response = client.get(test_url)
    assert response.status_code == 200
    assert json.loads(response.text) == f'{{"uuid": "{uuid_value}", "name": "test", "count": 0}}'

def test_add_new_counter_api(uuid_value, hex_str_to_uuid_str):
    app = api.app
    assert isinstance(app, object)
    client = TestClient(app)
    name = "testname"
    test_url = f"/counter/new/{uuid_value}/{name}"
    response = client.post(test_url)
    assert response.status_code == 200
    assert isinstance(response.text, str)
    # Test the counter was added
    db = Database()
    row =  db.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    assert hex_str_to_uuid_str(row.uuid.hex) == uuid_value
    assert row.name == name
    # Now clean up
    db.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    row =  db.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    assert row is None

def test_create_counter_api():
    """Test creating a counter via the API"""
    app = api.app
    client = TestClient(app)
    name = "testname"
    test_url = f"/counter/create/{name}"
    response = client.post(test_url)
    assert response.status_code == 200
    assert isinstance(response.text, str)
    result = json.loads(response.text)
    assert isinstance(result, dict)
    assert "uuid" in result
    assert isinstance(UUID(result["uuid"]), UUID)
    # Now clean up
    db = Database()
    db.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=result["uuid"])
    row =  db.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=result["uuid"])
    assert row is None

