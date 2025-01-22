from flask import Blueprint, render_template
from .models import db, System, AttributeSystemMapping
import plotly.graph_objects as go

# Initialize the blueprint for routes
lineage_bp = Blueprint('lineage_bp', __name__)

@lineage_bp.route('/lineage')
def full_lineage():
    # Initialize a Plotly graph
    G = go.Figure()

    # Query all system-to-system mappings via AttributeSystemMapping
    attribute_system_mappings = db.session.query(AttributeSystemMapping, System) \
        .join(System, AttributeSystemMapping.system_id == System.system_id).all()

    # Prepare nodes and edges for visualization
    nodes = set()
    edges = []

    # Add edges (lineages between systems based on AttributeSystemMapping)
    for mapping, system in attribute_system_mappings:
        source_system = system.system_name  # Access the System's name
        target_system = mapping.system_attribute_name  # Access the system attribute name from the mapping

        # Add to nodes set to ensure unique nodes (only systems)
        nodes.add(source_system)
        nodes.add(target_system)

        # Add the edge between source and target systems
        edges.append((source_system, target_system))

    # Create the layout for the graph
    node_positions = {node: (i, 0) for i, node in enumerate(nodes)}  # Simple layout with nodes in a line

    # Create the scatter plot for nodes
    node_x = [node_positions[node][0] for node in nodes]
    node_y = [node_positions[node][1] for node in nodes]

    # Add nodes as Scatter objects (no attribute names, only system names)
    G.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=list(nodes), textposition='top center', marker=dict(size=10, color='blue')))

    # Add edges as lines between nodes
    for edge in edges:
        source, target = edge
        source_x, source_y = node_positions[source]
        target_x, target_y = node_positions[target]

        G.add_trace(go.Scatter(x=[source_x, target_x], y=[source_y, target_y], mode='lines', line=dict(width=1, color='black')))

    # Set layout for the plot
    layout = {
        'title': 'System Lineage',
        'xaxis': {'title': 'Systems'},
        'yaxis': {'title': 'Systems'},
    }

    G.update_layout(layout)
    return render_template('lineage.html', graph=G.to_html(full_html=False))