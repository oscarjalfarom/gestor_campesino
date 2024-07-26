# src/routes/asociaciones.py
from flask import Blueprint, request, jsonify
from src.models import db, Asociacion
from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest

asociaciones_bp = Blueprint('asociaciones', __name__)

@asociaciones_bp.route('/asociaciones', methods=['POST'])
def crear_asociacion():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    try:
        nueva_asociacion = Asociacion(
            id_asociacion=data['id_asociacion'],
            nombre_asociacion=data['nombre_asociacion'],
            siglas=data['siglas'],
            fecha_constitucion=datetime.strptime(data['fecha_constitucion'], '%Y-%m-%d').date(),
            objetivo=data.get('objetivo'),
            direccion=data.get('direccion'),
            representante_legal=data.get('representante_legal'),
            celular=data['celular'],
            email=data['email']
        )
        db.session.add(nueva_asociacion)
        db.session.commit()
        return jsonify({"mensaje": "Asociación creada exitosamente"}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear la asociación"}), 500


@asociaciones_bp.route('/asociaciones', methods=['GET'])
def obtener_asociaciones():
    try:
        asociaciones = Asociacion.query.all()
        resultado = [{
            'id_asociacion': asociacion.id_asociacion,
            'nombre_asociacion': asociacion.nombre_asociacion,
            'siglas': asociacion.siglas,
            'fecha_constitucion': asociacion.fecha_constitucion.strftime('%Y-%m-%d'),
            'objetivo': asociacion.objetivo,
            'direccion': asociacion.direccion,
            'representante_legal': asociacion.representante_legal,
            'celular': asociacion.celular,
            'email': asociacion.email,
            'fecha_digitacion': asociacion.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        } for asociacion in asociaciones]
        return jsonify(resultado), 200
    except Exception as e:
        # Log the exception if needed
        # current_app.logger.error(f'Error retrieving associations: {str(e)}')
        return jsonify({"error": "Error al obtener las asociaciones", "detalle": str(e)}), 500


@asociaciones_bp.route('/asociaciones/<int:id>/nombre', methods=['GET'])
def obtener_asociacion_nom(id):
    try:
        asociacion = Asociacion.query.get_or_404(id)
        resultado = {
            'siglas': asociacion.siglas,
        }
        return jsonify(resultado), 200
    except NotFound:
        return jsonify({"error": "Asociación no encontrada"}), 404
    except Exception as e:
        # Log the exception if needed
        # current_app.logger.error(f'Error retrieving association: {str(e)}')
        return jsonify({"error": "Error al obtener la asociación", "detalle": str(e)}), 500

@asociaciones_bp.route('/asociaciones/<int:id>', methods=['GET'])
def obtener_asociacion(id):
    try:
        asociacion = Asociacion.query.get_or_404(id)
        resultado = {
            'id_asociacion': asociacion.id_asociacion,
            'nombre_asociacion': asociacion.nombre_asociacion,
            'siglas': asociacion.siglas,
            'fecha_constitucion': asociacion.fecha_constitucion.strftime('%Y-%m-%d'),
            'objetivo': asociacion.objetivo,
            'direccion': asociacion.direccion,
            'representante_legal': asociacion.representante_legal,
            'celular': asociacion.celular,
            'email': asociacion.email,
            'fecha_digitacion': asociacion.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(resultado), 200
    except NotFound:
        return jsonify({"error": "Asociación no encontrada"}), 404
    except Exception as e:
        # Log the exception if needed
        # current_app.logger.error(f'Error retrieving association: {str(e)}')
        return jsonify({"error": "Error al obtener la asociación", "detalle": str(e)}), 500

@asociaciones_bp.route('/asociaciones/<int:id>', methods=['PUT'])
def actualizar_asociacion(id):
    try:
        data = request.json
        if not data:
            raise BadRequest("No se proporcionaron datos para la actualización")
        
        asociacion = Asociacion.query.get_or_404(id)

        if 'fecha_constitucion' in data:
            asociacion.fecha_constitucion = datetime.strptime(data['fecha_constitucion'], '%Y-%m-%d').date()

        asociacion.nombre_asociacion = data.get('nombre_asociacion', asociacion.nombre_asociacion)
        asociacion.siglas = data.get('siglas', asociacion.siglas)
        asociacion.objetivo = data.get('objetivo', asociacion.objetivo)
        asociacion.direccion = data.get('direccion', asociacion.direccion)
        asociacion.representante_legal = data.get('representante_legal', asociacion.representante_legal)
        asociacion.celular = data.get('celular', asociacion.celular)
        asociacion.email = data.get('email', asociacion.email)

        db.session.commit()
        return jsonify({"mensaje": "Asociación actualizada exitosamente"}), 200

    except NotFound:
        return jsonify({"error": "Asociación no encontrada"}), 404
    except BadRequest as e:
        return jsonify({"error": "Datos inválidos o faltantes", "detalle": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Formato de fecha inválido", "detalle": str(e)}), 400
    except Exception as e:
        # Log the exception if needed
        # current_app.logger.error(f'Error updating association: {str(e)}')
        return jsonify({"error": "Error al actualizar la asociación", "detalle": str(e)}), 500
    
@asociaciones_bp.route('/asociaciones/<int:id>', methods=['DELETE'])
def eliminar_asociacion(id):
    try:
        asociacion = Asociacion.query.get_or_404(id)
        db.session.delete(asociacion)
        db.session.commit()
        return jsonify({"mensaje": "Asociación eliminada exitosamente"}), 200

    except NotFound:
        return jsonify({"error": "Asociación no encontrada"}), 404
    except Exception as e:
        # Log the exception if needed
        # current_app.logger.error(f'Error deleting association: {str(e)}')
        return jsonify({"error": "Error al eliminar la asociación", "detalle": str(e)}), 500