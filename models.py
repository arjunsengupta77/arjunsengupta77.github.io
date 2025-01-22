from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

class System(db.Model):
    __tablename__ = 'systems'

    system_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    system_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
        return f"<System {self.system_name}>"

class Attribute(db.Model):
    __tablename__ = 'attributes'

    attribute_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    owner = db.Column(db.String)
    origin_system = db.Column(db.String)
    value_data_type = db.Column(db.String)

    def __repr__(self):
        return f"<Attribute {self.attribute_name}>"

class AttributeSystemMapping(db.Model):
    __tablename__ = 'attribute_system_mapping'

    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.attribute_id'), primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.system_id'), primary_key=True)
    system_attribute_name = db.Column(db.String, nullable=False)

    # Define relationships for the foreign keys
    attribute = db.relationship('Attribute', backref=db.backref('system_mappings', lazy=True))
    system = db.relationship('System', backref=db.backref('attribute_mappings', lazy=True))

    def __repr__(self):
        return f"<AttributeSystemMapping {self.attribute_id} - {self.system_id} - {self.system_attribute_name}>"