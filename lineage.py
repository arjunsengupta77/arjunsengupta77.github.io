import graphviz

class Lineage:
    def __init__(self, systems, feeds, attributes):
        self.systems = systems
        self.feeds = feeds
        self.attributes = attributes

    def __repr__(self):
        return f"Lineage(systems={len(self.systems)}, feeds={len(self.feeds)}, attributes={len(self.attributes)})"

    def generate_full_lineage(self):
        dot = graphviz.Digraph(comment="Data Lineage")

        for system in self.systems:
            dot.node(system.name, system.name)

        for feed in self.feeds:
            for attribute in feed.attributes:
                dot.edge(feed.origin_system.name, feed.target_system.name, label=attribute.name)

        return dot

    def generate_attribute_lineage(self, attribute_name):
        dot = graphviz.Digraph(comment=f"Data Lineage for {attribute_name}")

        attribute = None
        for attr in self.attributes:
            if attr.name == attribute_name:
                attribute = attr
                break

        if not attribute:
            raise ValueError(f"Attribute '{attribute_name}' not found.")

        visited_systems = set()

        def add_lineage(feed, visited_systems):
            origin_system = feed.origin_system
            target_system = feed.target_system

            if origin_system not in visited_systems:
                visited_systems.add(origin_system)
                dot.node(origin_system.name, origin_system.name)

            if target_system not in visited_systems:
                visited_systems.add(target_system)
                dot.node(target_system.name, target_system.name)

            dot.edge(origin_system.name, target_system.name, label=attribute.name)

        for feed in attribute.feeds:
            add_lineage(feed, visited_systems)

        return dot