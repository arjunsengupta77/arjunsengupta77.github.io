from app import db
from blueprints.glossary.models import Attribute
from blueprints.system.models import System

class AttributeSystemMapping(db.Model):
    __tablename__ = 'attribute_system_mapping'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attribute.id'), nullable=False)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
    system_attribute_name = db.Column(db.String(255), nullable=False)

    attribute = db.relationship('Attribute', backref='mappings', lazy=True)
    system = db.relationship('System', backref='mappings', lazy=True)

    def __repr__(self):
        return f"<Mapping Attribute ID {self.attribute_id} -> System ID {self.system_id}>"