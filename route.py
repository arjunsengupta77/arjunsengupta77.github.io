from flask import render_template
from . import db
from .models import System, Attribute, AttributeSystemMapping

# Route to display glossary of attributes with their definitions and origin systems
@bp.route('/glossary')
def glossary():
    attributes = Attribute.query.all()  # Fetch all attributes from the database
    return render_template('glossary.html', attributes=attributes)

# Route to display full lineage of all systems (no attributes shown)
@bp.route('/full_lineage')
def full_lineage():
    systems = System.query.all()  # Fetch all systems from the database
    return render_template('full_lineage.html', systems=systems)

# Route to display the lineage of a given attribute
@bp.route('/attribute_lineage/<int:attribute_id>')
def attribute_lineage(attribute_id):
    attribute = Attribute.query.get(attribute_id)  # Get the specific attribute
    if not attribute:
        return "Attribute not found", 404
    
    systems = db.session.query(System).join(AttributeSystemMapping).filter(
        AttributeSystemMapping.attribute_id == attribute_id
    ).all()  # Get all systems for the specific attribute

    return render_template('attribute_lineage.html', attribute=attribute, systems=systems)