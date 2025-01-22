from flask import Blueprint, render_template
from .models import db, System, Attribute, AttributeSystemMapping
import plotly.graph_objects as go

# Initialize the blueprint for routes
lineage_bp = Blueprint('lineage_bp', __name__)

@lineage_bp.route('/glossary')
def glossary():
    # Query all attributes with their definitions and origin systems
    attributes = db.session.query(Attribute).all()
    return render_template('glossary.html', attributes=attributes)

@lineage_bp.route('/lineage')
def full_lineage():
    # Initialize a Plotly graph
    G = go.Figure()

    # Query all system-to-system mappings via AttributeSystemMapping
    attribute_system_mappings = db.session.query(AttributeSystemMapping, System) \
        .join(System, AttributeSystemMapping.system_id == System.system_id).all()

    # Add edges (lineages between systems based on AttributeSystemMapping)
    for mapping, system in attribute_system_mappings:
        source_system = system.system_name  # Access the System's name
        target_system = mapping.system_attribute_name  # Access the system attribute name from the mapping
        
        # Add edge if source and target systems are different
        if source_system != target_system:
            G.add_edge(source_system, target_system)

    # Generate the layout for the plot
    layout = {
        'title': 'System Lineage',
        'xaxis': {'title': 'Systems'},
        'yaxis': {'title': 'Systems'},
    }
    
    # Set the layout and return the graph
    G.update_layout(layout)
    return render_template('lineage.html', graph=G.to_html(full_html=False))

@lineage_bp.route('/lineage/<int:attribute_id>')
def attribute_lineage(attribute_id):
    # Get the attribute
    attribute = db.session.query(Attribute).filter(Attribute.attribute_id == attribute_id).first()

    if not attribute:
        return f"Attribute with ID {attribute_id} not found", 404

    # Initialize a Plotly graph for the attribute lineage
    G = go.Figure()

    # Query all attribute-system mappings for the given attribute
    attribute_system_mappings = db.session.query(AttributeSystemMapping, System) \
        .join(System, AttributeSystemMapping.system_id == System.system_id) \
        .filter(AttributeSystemMapping.attribute_id == attribute_id).all()

    # Add edges (lineages between systems based on AttributeSystemMapping)
    for mapping, system in attribute_system_mappings:
        source_system = system.system_name  # Access the System's name
        target_system = mapping.system_attribute_name  # Access the system attribute name from the mapping
        
        # Add edge if source and target systems are different
        if source_system != target_system:
            G.add_edge(source_system, target_system)

    # Generate the layout for the plot
    layout = {
        'title': f'Lineage of {attribute.attribute_name}',
        'xaxis': {'title': 'Systems'},
        'yaxis': {'title': 'Systems'},
    }

    # Set the layout and return the graph
    G.update_layout(layout)
    return render_template('lineage_attribute.html', graph=G.to_html(full_html=False), attribute=attribute)