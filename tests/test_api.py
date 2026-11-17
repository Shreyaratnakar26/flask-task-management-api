import pytest
from app import create_app
from app.routes import _reset


@pytest.fixture
def client():
    _reset()
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "UP"


def test_create_and_list_tasks(client):
    res = client.post("/tasks", json={"title": "Learn Jenkins"})
    assert res.status_code == 201
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_update_and_delete_task(client):
    client.post("/tasks", json={"title": "Write tests"})
    res = client.put("/tasks/1", json={"done": True})
    assert res.get_json()["done"] is True
    assert client.delete("/tasks/1").status_code == 200
    assert client.get("/tasks/1").status_code == 404


def test_create_task_validation(client):
    assert client.post("/tasks", json={}).status_code == 400
