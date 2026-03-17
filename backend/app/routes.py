from flask import Blueprint, jsonify, request, send_from_directory
from .storage import create_task, generate_schedule, get_all_tasks

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
            "priority": t["priority"],
            "duration_minutes": t["duration_minutes"]
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
    duration_minutes = data.get("duration_minutes")

    if not title:
        return jsonify({"error": "Title is required."}), 400
    if not due_date:
        return jsonify({"error": "Due date is required."}), 400
    if priority not in {"Low", "Medium", "High"}:
        return jsonify({"error": "Priority must be Low, Medium, or High."}), 400
    if not isinstance(duration_minutes, int) or duration_minutes <= 0:
        return jsonify({"error": "Duration must be a positive number of minutes."}), 400

    task = create_task(title, due_date, priority, duration_minutes)

    # Return the created task (frontend doesn’t need it, but helpful)
    return jsonify({
        "title": task["title"],
        "status": task["status"],
        "due_date": task["due_date"],
        "priority": task["priority"],
        "duration_minutes": task["duration_minutes"]
    }), 201

@api.route("/api/schedule/generate", methods=["POST"])
def build_schedule():
    scheduled_tasks = generate_schedule()
    response = [
        {
            "title": task["title"],
            "status": task["status"],
            "due_date": task["due_date"],
            "priority": task["priority"],
            "duration_minutes": task["duration_minutes"],
            "scheduled_start": task["scheduled_start"],
            "scheduled_end": task["scheduled_end"],
            "display_time_range": task["display_time_range"],
            "scheduled_date": task["scheduled_date"],
            "is_scheduled": task["is_scheduled"]
        }
        for task in scheduled_tasks
    ]
    return jsonify(response), 200
