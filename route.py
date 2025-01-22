import plotly.graph_objects as go
import networkx as nx
from flask import Blueprint, render_template
from app import db  # Assuming you're using SQLAlchemy for your models
from app.models import Attribute, System, AttributeSystemMapping  # Your actual models

# Create the blueprint for lineage routes
lineage_bp = Blueprint('lineage', __name__)

# Helper function to generate the Plotly graph
def generate_lineage_graph(nodes, edges):
    """
    Generate a Plotly graph from the nodes and edges of a lineage.

    :param nodes: List of nodes (systems)
    :param edges: List of edges (relationships between systems)
    :return: Plotly figure object
    """
    edge_x = []
    edge_y = []
    for edge in edges:
        x0, y0 = edge[0]['pos']
        x1, y1 = edge[1]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_y.append(y0)
        edge_y.append(y1)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_text = []
    for node in nodes:
        x, y = node['pos']
        node_x.append(x)
        node_y.append(y)
        node_text.append(node['label'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10
        ),
        text=node_text
    )

    layout = go.Layout(
        title='Lineage Visualization',
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig

# Route for glossary
@lineage_bp.route('/glossary')
def glossary():
    attributes = Attribute.query.all()
    return render_template('glossary.html', attributes=attributes)

# Route for full lineage (systems only)
@lineage_bp.route('/full_lineage')
def full_lineage():
    systems = System.query.all()

    # Create a directed graph with NetworkX
    G = nx.DiGraph()

    # Add nodes (systems)
    for system in systems:
        G.add_node(system.system_name, pos=(system.system_id, system.system_id), label=system.system_name)

    # Add edges (lineages between systems)
    attribute_system_mappings = AttributeSystemMapping.query.all()  # This represents the relationship between systems and attributes
    for attribute_system_mapping in attribute_system_mappings:
        source_system = attribute_system_mapping.system.system_name
        target_system = attribute_system_mapping.attribute.origin_system
        if source_system != target_system:
            G.add_edge(source_system, target_system)

    # Generate Plotly graph
    nodes = [{'label': system['label'], 'pos': system['pos']} for system in G.nodes(data=True)]
    edges = [{'source': G.nodes[edge[0]], 'target': G.nodes[edge[1]]} for edge in G.edges()]
    
    fig = generate_lineage_graph(nodes, edges)

    # Return the rendered template with Plotly graph
    graph_html = fig.to_html(full_html=False)
    return render_template('lineage_full.html', graph_html=graph_html)

# Route for specific attribute lineage
@lineage_bp.route('/attribute_lineage/<attribute_id>')
def attribute_lineage(attribute_id):
    attribute = Attribute.query.get_or_404(attribute_id)

    # Create a directed graph with NetworkX
    G = nx.DiGraph()

    # Add nodes (systems related to the attribute)
    attribute_system_mappings = AttributeSystemMapping.query.filter_by(attribute_id=attribute_id).all()
    for attribute_system_mapping in attribute_system_mappings:
        system = attribute_system_mapping.system
        G.add_node(system.system_name, pos=(system.system_id, system.system_id), label=system.system_name)

    # Add edges (lineages between systems)
    for attribute_system_mapping in attribute_system_mappings:
        source_system = attribute_system_mapping.system.system_name
        target_system = attribute_system_mapping.attribute.origin_system
        if source_system != target_system:
            G.add_edge(source_system, target_system)

    # Generate Plotly graph
    nodes = [{'label': system['label'], 'pos': system['pos']} for system in G.nodes(data=True)]
    edges = [{'source': G.nodes[edge[0]], 'target': G.nodes[edge[1]]} for edge in G.edges()]

    fig = generate_lineage_graph(nodes, edges)

    # Return the rendered template with Plotly graph
    graph_html = fig.to_html(full_html=False)
    return render_template('lineage_attribute.html', attribute=attribute, graph_html=graph_html)