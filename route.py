from flask import render_template, request, Response
from . import db
from .models import System, Attribute, AttributeSystemMapping
from graphviz import Digraph
import io
from flask import send_file

# Route to display glossary of attributes with their definitions and origin systems
@bp.route('/glossary')
def glossary():
    attributes = Attribute.query.all()  # Fetch all attributes from the database
    return render_template('glossary.html', attributes=attributes)

# Route to display full lineage of all systems (no attributes shown)
@bp.route('/full_lineage')
def full_lineage():
    systems = System.query.all()  # Fetch all systems from the database
    graph = Digraph('full_lineage')
    
    for system in systems:
        graph.node(system.name)  # Add node for each system
    
    # Generate the graph and convert it to PNG for rendering
    img_data = io.BytesIO(graph.pipe(format='png'))
    return send_file(img_data, mimetype='image/png')

# Route to display the lineage of a given attribute
@bp.route('/attribute_lineage/<int:attribute_id>')
def attribute_lineage(attribute_id):
    attribute = Attribute.query.get(attribute_id)  # Get the specific attribute
    if not attribute:
        return "Attribute not found", 404

    systems = db.session.query(System).join(AttributeSystemMapping).filter(
        AttributeSystemMapping.attribute_id == attribute_id
    ).all()  # Get all systems for the specific attribute

    graph = Digraph(f'attribute_lineage_{attribute_id}')
    graph.node(attribute.name, label=f"{attribute.name}: {attribute.definition}")  # Add node for the attribute
    
    for system in systems:
        graph.node(system.name)  # Add node for each system
        graph.edge(attribute.name, system.name)  # Connect the attribute to the system
    
    # Generate the graph and convert it to PNG for rendering
    img_data = io.BytesIO(graph.pipe(format='png'))
    return send_file(img_data, mimetype='image/png')