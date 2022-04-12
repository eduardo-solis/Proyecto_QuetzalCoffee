#import os
from flask import Flask, render_template
from .config import DevelopmentConfig
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
# Manejo de logs
import logging
import datetime

from .public import public
from .private import private
from .auth import auth

from .models import db, userDataStore
from .config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    
    @app.errorhandler(code_or_exception=404)
    def page_not_found(e):
        return render_template('404.html'),404
    
    LOG_FILENAME = 'events.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    date = datetime.datetime.now()
    
    mensaje='''
            Arranque de la aplicacion el dia {} a las {}
    '''.format(date.date(), date.strftime('%X'))
    
    app.logger.info(mensaje)
    app.config.from_object(DevelopmentConfig)
    
    # Conectamos los modelos a flask-security
    security = Security(app, userDataStore)
    
    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
    
    # Registramos el blueprint para las rutas de auth
    app.register_blueprint(auth)
    
    # Registramos el blueprint para las rutas publicas
    app.register_blueprint(public)
    
    # Registramos el blueprint para las rutas privadas
    app.register_blueprint(private)
    
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    return app