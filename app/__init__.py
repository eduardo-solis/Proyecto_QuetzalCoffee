from flask import Flask
from .config import DevelopmentConfig
from .public import public

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    app.register_blueprint(public)
    
    return app