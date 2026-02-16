from flask import Blueprint, jsonify, request, send_from_directory
from .storage import create_task, list_tasks

main = Blueprint("main", __name__)

# Frontend entry point
@main.route("/")
def index():
    return send_from_directory("../../frontend", "index.html")

# Simple API health check
@main.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Smart Task Planner API is running."})

# Create a task
@main.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    due_date = (data.get("due_date") or "").strip()
    priority = (data.get("priority") or "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400
    if not due_date:
        return jsonify({"error": "Due date is required"}), 400
    if priority not in {"Low", "Medium", "High"}:
        return jsonify({"error": "Priority must be Low, Medium, or High"}), 400

    task = create_task(title, due_date, priority)
    return jsonify(task), 201

# List tasks (+ optional sorting)
@main.route("/api/tasks", methods=["GET"])
def get_tasks():
    sort_by = request.args.get("sort")  # "date" or "priority"
    tasks = list_tasks(sort_by=sort_by)
    return jsonify(tasks)