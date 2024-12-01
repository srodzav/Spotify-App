import os
from flask import Flask
from instance.config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.secret_key = os.getenv('SECRET_KEY') or 'some_random_secret'
    # Registrar rutas
    from .routes import main
    app.register_blueprint(main)

    return app
