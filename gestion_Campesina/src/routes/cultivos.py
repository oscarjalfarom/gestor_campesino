from flask import Blueprint, request, jsonify
from src.models import db, Cultivo
from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest

cultivo_bp = Blueprint('cultivo', __name__)

@cultivo_bp.route('/cultivo', methods=['POST'])
def crear_cultivo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    campos_obligatorios = [
        'tipo_cultivo', 'area_cultivada', 'fecha_siembra', 
        'fecha_cosecha', 'nuip_asociado', 'id_predio'
    ]

    for campo in campos_obligatorios:
        if campo not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {campo}"}), 400

    try:
        nuevo_cultivo = Cultivo(
            tipo_cultivo=data['tipo_cultivo'],
            area_cultivada=data['area_cultivada'],
            fecha_siembra=datetime.strptime(data['fecha_siembra'], '%Y-%m-%d').date(),
            fecha_cosecha=datetime.strptime(data['fecha_cosecha'], '%Y-%m-%d').date(),
            observacion=data.get('observacion'),
            nuip_asociado=data['nuip_asociado'],
            id_predio=data['id_predio']
        )
        db.session.add(nuevo_cultivo)
        db.session.commit()
        return jsonify({"mensaje": "Cultivo creado exitosamente"}), 201

    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear el cultivo", "detalle": str(e)}), 500


@cultivo_bp.route('/cultivo', methods=['GET'])
def obtener_cultivos():
    try:
        cultivos = Cultivo.query.all()
        resultado = [{
            'id_cultivo': cultivo.id_cultivo,
            'tipo_cultivo': cultivo.tipo_cultivo,
            'area_cultivada': cultivo.area_cultivada,
            'fecha_siembra': cultivo.fecha_siembra.strftime('%Y-%m-%d'),
            'fecha_cosecha': cultivo.fecha_cosecha.strftime('%Y-%m-%d'),
            'observacion': cultivo.observacion,
            'nuip_asociado': cultivo.nuip_asociado,
            'id_predio': cultivo.id_predio,
            'fecha_digitacion': cultivo.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        } for cultivo in cultivos]
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": "Error al obtener los cultivos", "detalle": str(e)}), 500


@cultivo_bp.route('/cultivo/<int:id_cultivo>', methods=['GET'])
def obtener_cultivo(id_cultivo):
    try:
        cultivo = Cultivo.query.get_or_404(id_cultivo)
        resultado = {
            'id_cultivo': cultivo.id_cultivo,
            'tipo_cultivo': cultivo.tipo_cultivo,
            'area_cultivada': cultivo.area_cultivada,
            'fecha_siembra': cultivo.fecha_siembra.strftime('%Y-%m-%d'),
            'fecha_cosecha': cultivo.fecha_cosecha.strftime('%Y-%m-%d'),
            'observacion': cultivo.observacion,
            'nuip_asociado': cultivo.nuip_asociado,
            'id_predio': cultivo.id_predio,
            'fecha_digitacion': cultivo.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(resultado)
    except NotFound:
        return jsonify({"error": "Cultivo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener el cultivo", "detalle": str(e)}), 500


@cultivo_bp.route('/cultivo/<int:id_cultivo>', methods=['PUT'])
def actualizar_cultivo(id_cultivo):
    try:
        data = request.json
        cultivo = Cultivo.query.get_or_404(id_cultivo)

        cultivo.tipo_cultivo = data.get('tipo_cultivo', cultivo.tipo_cultivo)
        cultivo.area_cultivada = data.get('area_cultivada', cultivo.area_cultivada)
        cultivo.fecha_siembra = datetime.strptime(data['fecha_siembra'], '%Y-%m-%d').date()
        cultivo.fecha_cosecha = datetime.strptime(data['fecha_cosecha'], '%Y-%m-%d').date()
        cultivo.observacion = data.get('observacion', cultivo.observacion)
        cultivo.nuip_asociado = data.get('nuip_asociado', cultivo.nuip_asociado)
        cultivo.id_predio = data.get('id_predio', cultivo.id_predio)

        db.session.commit()
        return jsonify({"mensaje": "Cultivo actualizado exitosamente"})
    except NotFound:
        return jsonify({"error": "Cultivo no encontrado"}), 404
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al actualizar el cultivo", "detalle": str(e)}), 500


@cultivo_bp.route('/cultivo/<int:id_cultivo>', methods=['DELETE'])
def eliminar_cultivo(id_cultivo):
    try:
        cultivo = Cultivo.query.get_or_404(id_cultivo)
        db.session.delete(cultivo)
        db.session.commit()
        return jsonify({"mensaje": "Cultivo eliminado exitosamente"})
    except NotFound:
        return jsonify({"error": "Cultivo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al eliminar el cultivo", "detalle": str(e)}), 500
