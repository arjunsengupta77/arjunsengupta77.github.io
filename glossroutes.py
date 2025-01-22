from flask import render_template
from .models import Attribute

def get_all_attributes():
    return Attribute.query.all()

@glossary_bp.route("/")
def glossary():
    attributes = get_all_attributes()
    return render_template("glossary.html", attributes=attributes)