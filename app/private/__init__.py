from flask import Blueprint

private = Blueprint('private', __name__, template_folder='./templates', url_prefix='/private')

from . import routes