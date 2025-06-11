from flask import jsonify, request, Blueprint
from app.models.task_model import Task
from app import db
from flask_login import login_required, current_user


tasks_bp = Blueprint("tasks",__name__)

@tasks_bp.route("/")
def first():
    return "Hello"

@tasks_bp.route("/api/tasks",methods=["GET"])
@login_required
def all_tasks():
    tasks = Task.query.all()
    all_tasks = []
    for task in tasks:
        dict_task = task.to_dict()
        all_tasks.append(dict_task)
    return jsonify(all_tasks)

@tasks_bp.route("/api/tasks/<int:task_id>",methods=["GET"])
@login_required
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error":"task doenot exist"}),404
    return jsonify(task.to_dict())

@tasks_bp.route("/api/tasks",methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({"error":"task doesnot exist"}),404
    name = data.get("name")
    description = data.get("description")
    status = data.get("status")

    if not name or type(name)!=str  or name.strip()=="":
        return jsonify({"error":"name should be there for task"}),400
    
    if not description or len(description) < 9 or description.strip =="":
        return jsonify({"error":"description must be greater than 10 chars for task"}),400
    
    if status not in("pending","done"):
        return jsonify({"error":"if you enter status it must be pending or done"}),400
    
    new_task = Task(name = name, description = description, status = status)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"success":"task added ", "new task":new_task.to_dict()}),201

@tasks_bp.route("/api/tasks/<int:task_id>",methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error":"task not found"}),404
    
    data = request.get_json()
    if not data:
        return jsonify({"error":"no data entered"}),404
    
    name = data.get("name")
    description = data.get("description")
    status = data.get("status")
    
    if name:
        if type(name)!=str or name.strip() == "":
            return jsonify({"error":"enter proper name"}),400
        task.name = name

    if description:
        if description.strip() == "" or len(description)<10:
            return jsonify({"error":"description must be greater than 10 chars for task"}),400
        task.description = description
    if status:
        if status not in ("pending","done"):
            return jsonify({"error":"if you enter status it must be pending or done"}),400
        task.status = status
    
    db.session.commit()
    return jsonify({"success":"your task modified successfully","task":task.to_dict()}),201


@tasks_bp.route("/api/tasks/<int:task_id>",methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error":"task not found"}),404
    if task.author != current_user:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success":"task deleted","task":task.to_dict()}),201