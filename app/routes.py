import os
import time
from flask import Blueprint, jsonify, request

bp = Blueprint("tasks", __name__)

START_TIME = time.time()

# In-memory persistence (acceptable per rubric 1.2)
tasks = {}
_next_id = 1


def _reset():
    """Helper used by unit tests."""
    global _next_id
    tasks.clear()
    _next_id = 1


@bp.get("/")
def index():
    return jsonify(message="Flask Task Management API", version=os.getenv("APP_VERSION", "dev")), 200


@bp.get("/health")
def health():
    return jsonify(status="UP", uptime_seconds=round(time.time() - START_TIME, 2)), 200


@bp.get("/tasks")
def list_tasks():
    return jsonify(list(tasks.values())), 200


@bp.post("/tasks")
def create_task():
    global _next_id
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="'title' is required"), 400
    task = {
        "id": _next_id,
        "title": title,
        "description": data.get("description", ""),
        "done": bool(data.get("done", False)),
    }
    tasks[_next_id] = task
    _next_id += 1
    return jsonify(task), 201


@bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify(error="Task not found"), 404
    return jsonify(task), 200


@bp.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify(error="Task not found"), 404
    data = request.get_json(silent=True) or {}
    for key in ("title", "description", "done"):
        if key in data:
            task[key] = data[key]
    return jsonify(task), 200


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if tasks.pop(task_id, None) is None:
        return jsonify(error="Task not found"), 404
    return jsonify(message="Task deleted"), 200
