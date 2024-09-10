from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import main
from letscountit.db.edgedb import Database
import json
from uuid import UUID


def test_get_counter_by_uuid(uuid_value):
    app = main.app
    assert isinstance(app, object)
    client = TestClient(app)
    # Add a counter to the database directly
    db = Database()
    db.insert_counter(uuid_value, "test")
    # Now test we can retrieve it by the API
    test_url = f"/counter/{uuid_value}"
    response = client.get(test_url)
    assert response.status_code == 200
    assert (
        json.loads(response.text)
        == f'{{"uuid": "{uuid_value}", "name": "test", "count": 0}}'
    )


def test_add_new_counter_api(uuid_value, hex_str_to_uuid_str):
    app = main.app
    assert isinstance(app, object)
    client = TestClient(app)
    name = "testname"
    test_url = f"/counter/new/{uuid_value}/{name}"
    response = client.post(test_url)
    assert response.status_code == 200
    assert isinstance(response.text, str)
    # Test the counter was added
    db = Database()
    row = db.query(
        "SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value
    )
    assert hex_str_to_uuid_str(row.uuid.hex) == uuid_value
    assert row.name == name
    # Now clean up
    db.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid_value)
    row = db.query(
        "SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid_value
    )
    assert row is None


def test_create_counter_api():
    """Test creating a counter via the API"""
    app = main.app
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
    row = db.query(
        "SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=result["uuid"]
    )
    assert row is None


def test_increase_counter_api():
    """Tests increasing a counter using the api"""
    app = main.app
    client = TestClient(app)
    name = "testname"
    test_url = f"/counter/create/{name}"
    response = client.post(test_url)
    result = json.loads(response.text)
    uuid = result["uuid"]
    test_url = f"/counter/increase/{uuid}"
    response = client.post(test_url)
    assert response.status_code == 200
    result = json.loads(response.text)
    assert result["count"] == 1
    # Now clean up
    db = Database()
    db.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid)
    row = db.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid)
    assert row is None


def test_decrease_counter_api():
    """Tests decreasing a counter using the api"""
    app = main.app
    client = TestClient(app)
    name = "testname"
    test_url = f"/counter/create/{name}"
    response = client.post(test_url)
    result = json.loads(response.text)
    uuid = result["uuid"]
    test_url = f"/counter/decrease/{uuid}"
    response = client.post(test_url)
    assert response.status_code == 200
    result = json.loads(response.text)
    assert result["count"] == -1
    # Now clean up
    db = Database()
    db.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid)
    row = db.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid)
    assert row is None


def test_list_all_counters_api():
    """Tests the API for listing all counters"""
    app = main.app
    client = TestClient(app)
    test_url = "/counters/list"
    response = client.get(test_url)
    assert response.status_code == 200
    assert isinstance(response.text, str)
    result = json.loads(response.text)
    assert isinstance(result, list)
    assert len(result) > 0
    for counter in result:
        assert "uuid" in counter
        assert "name" in counter
        assert "count" in counter
        assert isinstance(UUID(counter["uuid"]), UUID)
        assert isinstance(counter["name"], str)
        assert isinstance(counter["count"], int)
        assert counter["count"] >= 0


def test_create_counter_with_initial_value():
    """Tests creating a counter with an initial value"""
    app = main.app
    client = TestClient(app)
    name = "testname"
    initial_value = 12
    test_url = f"/counter/create/{name}/{initial_value}"
    response = client.post(test_url)
    result = json.loads(response.text)
    uuid = result["uuid"]
    assert response.status_code == 200
    result = json.loads(response.text)
    assert result["count"] == str(initial_value)
    # Now clean up
    db = Database()
    db.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid)
    row = db.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid)
    assert row is None


def test_update_counter_with_value():
    """Tests updating a counter with a value"""
    app = main.app
    client = TestClient(app)
    name = "testname"
    initial_value = 12
    test_url = f"/counter/create/{name}/{initial_value}"
    response = client.post(test_url)
    result = json.loads(response.text)
    uuid = result["uuid"]
    new_value = 15
    test_url = f"/counter/update/{uuid}/{new_value}"
    response = client.post(test_url)
    assert response.status_code == 200
    result = json.loads(response.text)
    assert result["count"] == new_value
    # Now clean up
    db = Database()
    db.query("DELETE counter FILTER .uuid = <uuid>$uuid", uuid=uuid)
    row = db.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid)
    assert row is None
