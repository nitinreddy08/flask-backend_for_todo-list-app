# app/routes/tasks.py

from flask import Blueprint, jsonify, request
from app.models.task_model import get_all_tasks, get_task, create_task, update_task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(get_all_tasks())

@tasks_bp.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = get_task(task_id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@tasks_bp.route("/api/tasks", methods=["POST"])
def post_task():
    new_task = request.get_json()
    if not new_task:
        return jsonify({"error": "Enter Task"}), 400

    name = new_task.get("name")
    description = new_task.get("description")
    status = new_task.get("status")

    if not name or type(name) != str or name.strip() == "":
        return jsonify({"error": "name is not a string"}), 400
    if not description or len(description) < 10:
        return jsonify({"error": "description error"}), 400
    if status and status not in ("pending", "done"):
        return jsonify({"error": "status must be pending or done"}), 400

    task = {
        "name": name,
        "description": description,
        "status": status or "pending"
    }

    created = create_task(task)
    return jsonify({"success": "task added", "task": created}), 201

@tasks_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
def put_task(task_id):
    existing_task = get_task(task_id)
    if not existing_task:
        return jsonify({"error": "Task not found"}), 404

    updated_data = request.get_json()
    if not updated_data:
        return jsonify({"error": "enter data"}), 400

    name = updated_data.get("name")
    description = updated_data.get("description")
    status = updated_data.get("status")

    if name and (type(name) != str or name.strip() == ""):
        return jsonify({"error": "name is not a string"}), 400
    if description and (type(description) != str or len(description) < 10):
        return jsonify({"error": "description error"}), 400
    if status and status not in ("pending", "done"):
        return jsonify({"error": "status must be pending or done"}), 400

    updated_task = update_task(task_id, updated_data)
    return jsonify({"success": "task updated", "task": updated_task})
