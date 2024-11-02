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

    from app.controller.usuario_controller import usuario
    from app.controller.cliente_controller import cliente
    from app.controller.produto_controller import produto
    from app.controller.categoria_controller import categoria
    from app.controller.pedido_controller import pedido
    from app.controller.detalhe_pedido_controller import detalhe_pedido

    app.register_blueprint(usuario)
    app.register_blueprint(cliente)
    app.register_blueprint(produto)
    app.register_blueprint(categoria)
    app.register_blueprint(pedido)
    app.register_blueprint(detalhe_pedido)

    return app
