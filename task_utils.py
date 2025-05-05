import json
import csv
from datetime import datetime, timedelta
import bcrypt
from flask import jsonify  

TASK_FILE = "tasks.json"
USER_FILE = "users.json"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def tambah_tugas(tasks, nama, prioritas, deadline):
    tugas = {
        "task": nama,
        "done": False,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "priority": prioritas,
        "deadline": deadline
    }
    tasks.append(tugas)
    save_tasks(tasks)

def delete_task(tasks, index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
        return jsonify({"message": f"Tugas dengan ID {index} berhasil dihapus."}), 200
    return jsonify({"error": "Tugas tidak ditemukan."}), 404

def export_to_csv(tasks, filename="tasks.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Task", "Status", "Time", "Priority", "Deadline"])
        for t in tasks:
            writer.writerow([
                t["task"],
                "Selesai" if t["done"] else "Belum",
                t["time"],
                t["priority"],
                t["deadline"]
            ])

def login(users, username, password):
    for user in users:
        if user["username"] == username and bcrypt.checkpw(password.encode(), user["password"].encode()):
            return True
    return False

def add_user(users, username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users.append({"username": username, "password": hashed_password})
    save_users(users)

def check_deadlines(tasks):
    upcoming_tasks = []
    now = datetime.now()
    for task in tasks:
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
        if deadline <= now + timedelta(days=1) and not task["done"]:
            upcoming_tasks.append(task)
    return upcoming_tasks

def sort_tasks(tasks, by="priority"):
    return sorted(tasks, key=lambda x: x.get(by, ''))

def search_tasks(tasks, query):
    return [task for task in tasks if query.lower() in task["task"].lower()]
