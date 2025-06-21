from flask import Flask
from mavis_reporting.config import config

import os


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from mavis_reporting.views import main

    app.register_blueprint(main)

    return app
