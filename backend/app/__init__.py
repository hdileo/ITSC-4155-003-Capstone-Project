from flask import Flask

def create_app():
    app = Flask(
        __name__,
        static_folder="../../frontend",
        static_url_path=""
    )

    from .routes import api
    app.register_blueprint(api)

    return app