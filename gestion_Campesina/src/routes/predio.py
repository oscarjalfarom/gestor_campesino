from flask import Blueprint, request, jsonify
from src.models import db, Predio
from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest

predio_bp = Blueprint('predio', __name__)

@predio_bp.route('/predio', methods=['POST'])
def crear_predio():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    campos_obligatorios = ['nombre_predio', 'ubicacion', 'hectareas', 'nuip_asociado', 'fecha_ingreso']

    for campo in campos_obligatorios:
        if campo not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {campo}"}), 400

    try:
        nuevo_predio = Predio(
            nombre_predio=data['nombre_predio'],
            ubicacion=data['ubicacion'],
            hectareas=data['hectareas'],
            nuip_asociado=data['nuip_asociado'],
            fecha_ingreso=datetime.strptime(data['fecha_ingreso'], '%Y-%m-%d').date()
        )
        db.session.add(nuevo_predio)
        db.session.commit()
        return jsonify({"mensaje": "Predio creado exitosamente"}), 201

    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear el predio", "detalle": str(e)}), 500


@predio_bp.route('/predio', methods=['GET'])
def obtener_predios():
    try:
        predios = Predio.query.all()
        resultado = [{
            'id_predio': predio.id_predio,
            'nombre_predio': predio.nombre_predio,
            'ubicacion': predio.ubicacion,
            'hectareas': predio.hectareas,
            'nuip_asociado': predio.nuip_asociado,
            'fecha_ingreso': predio.fecha_ingreso.strftime('%Y-%m-%d'),
            'fecha_digitacion': predio.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        } for predio in predios]
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": "Error al obtener los predios", "detalle": str(e)}), 500


@predio_bp.route('/predio/<int:id_predio>', methods=['GET'])
def obtener_predio(id_predio):
    try:
        predio = Predio.query.get_or_404(id_predio)
        resultado = {
            'id_predio': predio.id_predio,
            'nombre_predio': predio.nombre_predio,
            'ubicacion': predio.ubicacion,
            'hectareas': predio.hectareas,
            'nuip_asociado': predio.nuip_asociado,
            'fecha_ingreso': predio.fecha_ingreso.strftime('%Y-%m-%d'),
            'fecha_digitacion': predio.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(resultado)
    except NotFound:
        return jsonify({"error": "Predio no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener el predio", "detalle": str(e)}), 500


@predio_bp.route('/predio/<int:id_predio>', methods=['PUT'])
def actualizar_predio(id_predio):
    try:
        data = request.json
        predio = Predio.query.get_or_404(id_predio)

        predio.nombre_predio = data.get('nombre_predio', predio.nombre_predio)
        predio.ubicacion = data.get('ubicacion', predio.ubicacion)
        predio.hectareas = data.get('hectareas', predio.hectareas)
        predio.nuip_asociado = data.get('nuip_asociado', predio.nuip_asociado)
        predio.fecha_ingreso = datetime.strptime(data['fecha_ingreso'], '%Y-%m-%d').date()

        db.session.commit()
        return jsonify({"mensaje": "Predio actualizado exitosamente"})
    except NotFound:
        return jsonify({"error": "Predio no encontrado"}), 404
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al actualizar el predio", "detalle": str(e)}), 500


@predio_bp.route('/predio/<int:id_predio>', methods=['DELETE'])
def eliminar_predio(id_predio):
    try:
        predio = Predio.query.get_or_404(id_predio)
        db.session.delete(predio)
        db.session.commit()
        return jsonify({"mensaje": "Predio eliminado exitosamente"})
    except NotFound:
        return jsonify({"error": "Predio no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al eliminar el predio", "detalle": str(e)}), 500
