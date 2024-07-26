# en routes/dashboard.py

from flask import Blueprint, jsonify
from src.models import db, Asociacion, Asociado

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/estadisticas', methods=['GET'])
def obtener_estadisticas():
    try:
        num_asociaciones = db.session.query(Asociacion).count()
        num_asociados = db.session.query(Asociado).count()
        # Agrega más estadísticas si es necesario

        estadisticas = {
            'num_asociaciones': num_asociaciones,
            'num_asociados': num_asociados,
            # Agrega más estadísticas si es necesario
        }

        return jsonify(estadisticas), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener estadísticas", "detalle": str(e)}), 500
