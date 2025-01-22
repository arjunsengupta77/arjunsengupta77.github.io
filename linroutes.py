from flask import render_template
from .models import Attribute, AttributeSystemMapping
import graphviz

def generate_lineage_graph():
    graph = graphviz.Digraph(format="png")
    attributes = Attribute.query.all()
    for attr in attributes:
        graph.node(str(attr.id), attr.attribute_name)
    mappings = AttributeSystemMapping.query.all()
    for mapping in mappings:
        graph.edge(str(mapping.attribute_id), str(mapping.system_id))
    return graph

@lineage_bp.route("/")
def view_lineage():
    graph = generate_lineage_graph()
    graph_path = graph.render("static/lineage_graph")
    return render_template("lineage.html", graph_path=graph_path)

@lineage_bp.route("/attribute/<int:attribute_id>")
def attribute_lineage(attribute_id):
    attribute = Attribute.query.get(attribute_id)
    if not attribute:
        return "Attribute not found", 404
    graph = graphviz.Digraph(format="png")
    graph.node(str(attribute.id), attribute.attribute_name)
    mappings = AttributeSystemMapping.query.filter_by(attribute_id=attribute_id).all()
    for mapping in mappings:
        graph.node(str(mapping.system_id), mapping.system_attribute_name)
        graph.edge(str(attribute.id), str(mapping.system_id))
    graph_path = graph.render(f"static/attribute_{attribute_id}_lineage")
    return render_template("attribute_lineage.html", graph_path=graph_path, attribute=attribute)