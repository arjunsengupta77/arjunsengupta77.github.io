from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blueprints.glossary import glossary_bp
from blueprints.lineage import lineage_bp

app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)

# Register blueprints
app.register_blueprint(glossary_bp, url_prefix="/glossary")
app.register_blueprint(lineage_bp, url_prefix="/lineage")

if __name__ == "__main__":
    app.run(debug=True)