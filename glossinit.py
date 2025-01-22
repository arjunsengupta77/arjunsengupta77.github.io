from flask import Blueprint

glossary_bp = Blueprint("glossary", __name__, template_folder="../../templates")

from . import routes