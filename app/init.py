from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
import logging

db = SQLAlchemy()
jwt = JWTManager()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    with app.app_context():
        from .routes import routes

        # Register blueprints
        app.register_blueprint(routes)
        print(app.url_map)

        # Create database tables
        db.create_all()

    return app
