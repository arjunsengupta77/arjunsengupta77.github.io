from flask import Blueprint

lineage_bp = Blueprint("lineage", __name__, template_folder="../../templates")

from . import routes