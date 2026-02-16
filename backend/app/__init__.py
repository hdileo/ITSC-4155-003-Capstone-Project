from flask import Flask
from .routes import main

def create_app():
    app = Flask(
        __name__,
        static_folder="../../frontend",   # serves your frontend files
        static_url_path=""               # makes / go to frontend
    )

    app.register_blueprint(main)

    return app