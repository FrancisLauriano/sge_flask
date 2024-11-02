from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config.config import Config
from app.middlewares.cors_middleware import init_cors

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    init_cors(app)

    # from app.routes.usuario_routes import usuario_routes
    # app.register_blueprint(usuario_routes)


    return app


    

