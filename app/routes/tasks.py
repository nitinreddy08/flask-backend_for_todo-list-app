from flask import jsonify, request, Blueprint
from app.models.task_model import Task
from app import db
from flask_login import login_required, current_user
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__)

def validate_task_data(data, is_update=False):
    errors = {}
    
    if not is_update or "name" in data:
        name = data.get("name", "")
        if not name or not isinstance(name, str) or not name.strip():
            errors["name"] = "Name is required and must be a non-empty string"
    
    if not is_update or "description" in data:
        description = data.get("description", "")
        if not description or not isinstance(description, str) or len(description.strip()) < 10:
            errors["description"] = "Description must be at least 10 characters long"
    
    if not is_update or "status" in data:
        status = data.get("status", "pending")
        if status not in ["pending", "done"]:
            errors["status"] = "Status must be either 'pending' or 'done'"
    
    if not is_update or "priority" in data:
        priority = data.get("priority", "medium")
        if priority not in ["low", "medium", "high"]:
            errors["priority"] = "Priority must be 'low', 'medium', or 'high'"
    
    return errors

@tasks_bp.route("/tasks", methods=["GET"])
@login_required
def all_tasks():
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
        return jsonify({
            "status": "success",
            "data": [task.to_dict() for task in tasks]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch tasks",
            "error": str(e)
        }), 500

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
@login_required
def get_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({
                "status": "error",
                "message": "Task not found"
            }), 404
        return jsonify({
            "status": "success",
            "data": task.to_dict()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch task",
            "error": str(e)
        }), 500

@tasks_bp.route("/tasks", methods=["POST"])
@login_required
def create_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400

        errors = validate_task_data(data)
        if errors:
            return jsonify({
                "status": "error",
                "message": "Validation failed",
                "errors": errors
            }), 400

        new_task = Task(
            name=data["name"],
            description=data["description"],
            status=data.get("status", "pending"),
            priority=data.get("priority", "medium"),
            user_id=current_user.id
        )
        
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Task created successfully",
            "data": new_task.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to create task",
            "error": str(e)
        }), 500

@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({
                "status": "error",
                "message": "Task not found"
            }), 404

        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400

        errors = validate_task_data(data, is_update=True)
        if errors:
            return jsonify({
                "status": "error",
                "message": "Validation failed",
                "errors": errors
            }), 400

        for field in ["name", "description", "status", "priority"]:
            if field in data:
                setattr(task, field, data[field])

        task.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Task updated successfully",
            "data": task.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to update task",
            "error": str(e)
        }), 500

@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({
                "status": "error",
                "message": "Task not found"
            }), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Task deleted successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to delete task",
            "error": str(e)
        }), 500