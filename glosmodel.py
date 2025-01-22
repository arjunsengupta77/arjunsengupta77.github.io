from app import db

class Attribute(db.Model):
    __tablename__ = 'attribute'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Attribute {self.attribute_name}>"