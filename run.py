import json
from lineage.parser import Parser
from lineage.lineage import Lineage

# Load JSON data
with open('data/data.json', 'r') as f:
    json_data = json.load(f)

# Parse the JSON data into Python objects
systems, feeds, attributes = Parser.parse_json(json_data)

# Create the lineage object
lineage = Lineage(systems, feeds, attributes)

# Generate and save the full data lineage diagram
dot = lineage.generate_full_lineage()
dot.render("output/full_lineage", format="png", cleanup=True)

# Generate and save the attribute-specific lineage diagram for "TransactionID"
dot_attribute = lineage.generate_attribute_lineage("TransactionID")
dot_attribute.render("output/attribute_lineage", format="png", cleanup=True)