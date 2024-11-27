class System:
    def __init__(self, name, system_type, feeds_in, feeds_out, owner, description):
        self.name = name
        self.system_type = system_type
        self.feeds_in = feeds_in if feeds_in else []
        self.feeds_out = feeds_out if feeds_out else []
        self.owner = owner
        self.description = description

    def __repr__(self):
        return f"System(name={self.name}, system_type={self.system_type}, owner={self.owner})"


class Feed:
    def __init__(self, origin_system, target_system, attributes, granularity, description, owner, technology, format):
        self.origin_system = origin_system
        self.target_system = target_system
        self.attributes = attributes if attributes else []
        self.granularity = granularity
        self.description = description
        self.owner = owner
        self.technology = technology
        self.format = format

    def __repr__(self):
        return f"Feed(origin_system={self.origin_system.name}, target_system={self.target_system.name}, granularity={self.granularity}, technology={self.technology})"


class Attribute:
    def __init__(self, name, description, owner, origin_system, feeds, mapping, value_data_type):
        self.name = name
        self.description = description
        self.owner = owner
        self.origin_system = origin_system
        self.feeds = feeds if feeds else []
        self.mapping = mapping if mapping else {}
        self.value_data_type = value_data_type

    def __repr__(self):
        return f"Attribute(name={self.name}, owner={self.owner}, value_data_type={self.value_data_type})"