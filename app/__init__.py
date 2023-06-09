# Import third-party
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    migrate = Migrate(app, db)
    # init logging
    logging.basicConfig(level=logging.DEBUG)
    from app import models
    from app import cmd
    from app import pub
    from app import wk
    from app import reporter
    from . import endpoint
    # apply the blueprints to the app
    app.register_blueprint(endpoint.api)
    app.register_blueprint(cmd.bd)
    app.register_blueprint(pub.pub)
    app.register_blueprint(wk.wk)
    app.register_blueprint(reporter.bd)
    return app
