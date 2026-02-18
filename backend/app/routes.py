from flask import Blueprint, jsonify, request, send_from_directory
from .storage import create_task, get_all_tasks

api = Blueprint("api", __name__)

# Serve frontend index
@api.route("/", methods=["GET"])
def index():
    return send_from_directory("../../frontend", "index.html")

# Optional health check (handy for Sprint 0 demo)
@api.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# GET tasks (supports sorting)
@api.route("/api/tasks", methods=["GET"])
def list_tasks():
    sort_by = request.args.get("sort")  # "date" or "priority" or None
    tasks = get_all_tasks(sort_by=sort_by)

    # Return exactly what frontend expects
    response = [
        {
            "title": t["title"],
            "status": t["status"],
            "due_date": t["due_date"],
            "priority": t["priority"]
        }
        for t in tasks
    ]
    return jsonify(response), 200

# POST create task
@api.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    due_date = (data.get("due_date") or "").strip()
    priority = (data.get("priority") or "").strip()

    if not title:
        return jsonify({"error": "Title is required."}), 400
    if not due_date:
        return jsonify({"error": "Due date is required."}), 400
    if priority not in {"Low", "Medium", "High"}:
        return jsonify({"error": "Priority must be Low, Medium, or High."}), 400

    task = create_task(title, due_date, priority)

    # Return the created task (frontend doesn’t need it, but helpful)
    return jsonify({
        "title": task["title"],
        "status": task["status"],
        "due_date": task["due_date"],
        "priority": task["priority"]
    }), 201