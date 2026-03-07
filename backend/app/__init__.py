from flask import Flask
from .database import init_db

def create_app():
    app = Flask(
        __name__,
        static_folder="../../frontend",
        static_url_path=""
    )

    app.config["DB_NAME"] = "tasks.db"

    from .routes import api
    app.register_blueprint(api)

    with app.app_context():
        init_db()

    return app