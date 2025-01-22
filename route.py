from flask import Blueprint, render_template
from .models import db, System, Attribute, AttributeSystemMapping
import networkx as nx
import plotly.graph_objects as go

lineage_bp = Blueprint('lineage', __name__)

# Helper function to generate the Plotly graph
def generate_lineage_graph(nodes, edges):
    # Create a Plotly figure
    fig = go.Figure()

    # Add nodes to the figure
    node_x = [node['label'] for node in nodes]
    node_y = [i for i in range(len(nodes))]
    
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_x,
        marker=dict(size=12, color='blue'),
        textposition="top center"
    ))

    # Add edges (connections between nodes) to the figure
    for edge in edges:
        source = edge['source']
        target = edge['target']
        fig.add_trace(go.Scatter(
            x=[source, target],
            y=[node_y[node_x.index(source)], node_y[node_x.index(target)]],
            mode='lines',
            line=dict(width=2, color='gray')
        ))

    fig.update_layout(showlegend=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    
    return fig

# Glossary route: lists attributes with their definitions and origin systems
@lineage_bp.route('/glossary')
def glossary():
    attributes = Attribute.query.all()

    glossary_data = []
    for attribute in attributes:
        glossary_data.append({
            'name': attribute.attribute_name,
            'description': attribute.description,
            'origin_system': attribute.origin_system
        })

    return render_template('glossary.html', glossary_data=glossary_data)

# Full Lineage route: Displays all systems in the lineage
@lineage_bp.route('/full_lineage')
def full_lineage():
    # Query all systems
    systems = System.query.all()

    # Create a directed graph with NetworkX
    G = nx.DiGraph()

    # Add nodes (systems)
    for system in systems:
        G.add_node(system.system_name, label=system.system_name)

    # Query all attribute-system mappings, joining with systems and attributes
    attribute_system_mappings = db.session.query(AttributeSystemMapping, System).join(System).all()

    # Add edges (lineages between systems based on AttributeSystemMapping)
    for mapping, system in attribute_system_mappings:
        source_system = system.system_name  # System where the attribute originates
        target_system = mapping.attribute.origin_system  # Origin system of the attribute
        
        # Add edge if source and target systems are different
        if source_system != target_system:
            G.add_edge(source_system, target_system)

    # Generate Plotly graph
    nodes = [{'label': system['label']} for system in G.nodes(data=True)]
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]

    fig = generate_lineage_graph(nodes, edges)

    # Return the rendered template with Plotly graph
    graph_html = fig.to_html(full_html=False)
    return render_template('lineage_full.html', graph_html=graph_html)

# Attribute-specific Lineage route: Displays lineage of a given attribute
@lineage_bp.route('/attribute_lineage/<int:attribute_id>')
def attribute_lineage(attribute_id):
    attribute = Attribute.query.get_or_404(attribute_id)

    # Query systems associated with the given attribute
    attribute_system_mappings = AttributeSystemMapping.query.filter_by(attribute_id=attribute_id).all()
    
    # Create a directed graph with NetworkX
    G = nx.DiGraph()

    # Add nodes (systems)
    systems = set()
    for mapping in attribute_system_mappings:
        systems.add(mapping.system.system_name)
        G.add_node(mapping.system.system_name)

    # Add edges (lineages between systems based on AttributeSystemMapping)
    for mapping in attribute_system_mappings:
        source_system = mapping.system.system_name
        target_system = mapping.attribute.origin_system
        
        # Add edge if source and target systems are different
        if source_system != target_system:
            G.add_edge(source_system, target_system)

    # Generate Plotly graph
    nodes = [{'label': system['label']} for system in G.nodes(data=True)]
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]

    fig = generate_lineage_graph(nodes, edges)

    # Return the rendered template with Plotly graph
    graph_html = fig.to_html(full_html=False)
    return render_template('attribute_lineage.html', attribute=attribute, graph_html=graph_html)