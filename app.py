from flask import Flask, jsonify, request
from task_utils import (
    load_tasks, save_tasks, tambah_tugas, check_deadlines,
    sort_tasks, search_tasks, load_users, add_user, delete_task
)

app = Flask(__name__)

@app.get("/tasks")
def get_tasks():
    return jsonify(load_tasks())

@app.post("/tasks")
def post_task():
    data = request.json
    tasks = load_tasks()
    if not data.get("task") or not data.get("priority") or not data.get("deadline"):
        return jsonify({"error": "Missing required fields"}), 400
    tambah_tugas(tasks, data["task"], data["priority"], data["deadline"])
    return jsonify({"message": "Tugas ditambahkan"}), 201

@app.put("/tasks/<int:index>")
def update_task(index):
    data = request.json
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index].update({
            "task": data.get("task", tasks[index]["task"]),
            "priority": data.get("priority", tasks[index]["priority"]),
            "deadline": data.get("deadline", tasks[index]["deadline"]),
            "done": data.get("done", tasks[index]["done"])
        })
        save_tasks(tasks)
        return jsonify({"message": f"Tugas {index} berhasil diupdate."})
    return jsonify({"error": "Index tidak valid"}), 404

@app.put("/tasks/<int:index>/done")
def mark_done(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        return jsonify({"message": "Tugas ditandai selesai."})
    return jsonify({"error": "Index tidak valid"}), 404

@app.delete("/tasks/<int:index>")
def delete_task_route(index):
    tasks = load_tasks()
    return delete_task(tasks, index)

@app.get("/tasks/upcoming")
def get_upcoming_tasks():
    tasks = load_tasks()
    upcoming_tasks = check_deadlines(tasks)
    return jsonify(upcoming_tasks)

@app.get("/tasks/sorted")
def get_sorted_tasks():
    sort_by = request.args.get('by', 'priority')
    tasks = load_tasks()
    sorted_tasks = sort_tasks(tasks, by=sort_by)
    return jsonify(sorted_tasks)

@app.get("/tasks/search")
def search_task():
    query = request.args.get('query', '')
    tasks = load_tasks()
    found_tasks = search_tasks(tasks, query)
    return jsonify(found_tasks)

@app.post("/users")
def register_user():
    data = request.json
    users = load_users()
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400
    add_user(users, data["username"], data["password"])
    return jsonify({"message": "User added"}), 201

if __name__ == "__main__":
    app.run(debug=True)
