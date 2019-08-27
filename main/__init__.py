from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .config import Config

db = SQLAlchemy()
def create_app():
    db = SQLAlchemy()
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    db.init_app(app)
    return app