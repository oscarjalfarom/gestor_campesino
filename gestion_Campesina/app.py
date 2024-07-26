# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from src.models import db
from src.routes.dashboards import dashboard_bp
from src.routes.asociaciones import asociaciones_bp
from src.routes.asociado import asociado_bp
from src.routes.nucleo_familiar import nucleo_familiar_bp
from src.routes.predio import predio_bp
from src.routes.cultivos import cultivo_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
# Registrar blueprints
app.register_blueprint(asociaciones_bp)
app.register_blueprint(asociado_bp)
app.register_blueprint(nucleo_familiar_bp)
app.register_blueprint(predio_bp)
app.register_blueprint(cultivo_bp)
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)
