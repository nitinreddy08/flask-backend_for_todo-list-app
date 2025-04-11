# app/models/task_model.py

tasks = {
    1: {
        "name": "Sample Task",
        "description": "Do something useful",
        "status": "pending"
    }
}
task_id_counter = 2  # simulate auto-increment


def get_all_tasks():
    return tasks


def get_task(task_id):
    return tasks.get(task_id)


def create_task(data):
    global task_id_counter
    tasks[task_id_counter] = data
    task_id_counter += 1
    return tasks[task_id_counter - 1]


def update_task(task_id, data):
    if task_id in tasks:
        tasks[task_id].update(data)
        return tasks[task_id]
    return None
