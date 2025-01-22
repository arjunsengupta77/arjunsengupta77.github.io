from app import db

class System(db.Model):
    __tablename__ = 'system'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    system_name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<System {self.system_name}>"