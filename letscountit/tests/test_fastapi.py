import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from letscountit import api
from uuid import uuid4


def test_get_counter_api():
    app = api.app
    assert isinstance(app, object)
    client = TestClient(app)
    uid = uuid4()
    test_url = f"/counter/{uid}"
    print(test_url)
    response = client.get(test_url)
    assert response.status_code == 200
    assert isinstance(response.text, str)


