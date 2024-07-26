# src/routes/asociado.py
from flask import Blueprint, request, jsonify
from src.models import db, Asociado
from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest

asociado_bp = Blueprint('asociado', __name__)

@asociado_bp.route('/asociado', methods=['POST'])
def crear_asociado():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # Lista de campos obligatorios
    campos_obligatorios = [
        'nuip_asociado', 'tipo_nuip', 'nombre', 'apellidos', 
        'fecha_nacimiento', 'estado_civil', 'sexo', 'id_asociacion'
    ]

    # Verificar que todos los campos obligatorios están presentes
    for campo in campos_obligatorios:
        if campo not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {campo}"}), 400

    try:
        nuevo_asociado = Asociado(
            nuip_asociado=data['nuip_asociado'],
            tipo_nuip=data['tipo_nuip'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date(),
            estado_civil=data['estado_civil'],
            sexo=data['sexo'],
            poblacion_especial=data.get('poblacion_especial'),
            direccion=data.get('direccion'),
            discapacidad_fisica=data.get('discapacidad_fisica'),
            celular=data.get('celular'),
            email=data.get('email'),
            id_asociacion=data['id_asociacion'],
            cargo=data.get('cargo'),
        )
        db.session.add(nuevo_asociado)
        db.session.commit()
        return jsonify({"mensaje": "Asociado creado exitosamente"}), 201

    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Log the exception if needed
        # current_app.logger.error(f'Error creating asociado: {str(e)}')
        return jsonify({"error": "Error al crear el asociado", "detalle": str(e)}), 500


@asociado_bp.route('/asociado', methods=['GET'])
def obtener_asociados():
    try:
        asociados = Asociado.query.all()
        resultado = [{
            'nuip_asociado': asociado.nuip_asociado,
            'tipo_nuip': asociado.tipo_nuip,
            'nombre': asociado.nombre,
            'apellidos': asociado.apellidos,
            'fecha_nacimiento': asociado.fecha_nacimiento.strftime('%Y-%m-%d'),
            'estado_civil': asociado.estado_civil,
            'sexo': asociado.sexo,
            'poblacion_especial': asociado.poblacion_especial,
            'direccion': asociado.direccion,
            'discapacidad_fisica': asociado.discapacidad_fisica,
            'celular': asociado.celular,
            'email': asociado.email,
            'id_asociacion': asociado.id_asociacion,
            'cargo': asociado.cargo,
            'fecha_digitacion': asociado.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        } for asociado in asociados]
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": "Error al obtener los asociados", "detalle": str(e)}), 500


@asociado_bp.route('/asociado/<int:nuip_asociado>', methods=['GET'])
def obtener_asociado(nuip_asociado):
    try:
        asociado = Asociado.query.get_or_404(nuip_asociado)
        resultado = {
            'nuip_asociado': asociado.nuip_asociado,
            'tipo_nuip': asociado.tipo_nuip,
            'nombre': asociado.nombre,
            'apellidos': asociado.apellidos,
            'fecha_nacimiento': asociado.fecha_nacimiento.strftime('%Y-%m-%d'),
            'estado_civil': asociado.estado_civil,
            'sexo': asociado.sexo,
            'poblacion_especial': asociado.poblacion_especial,
            'direccion': asociado.direccion,
            'discapacidad_fisica': asociado.discapacidad_fisica,
            'celular': asociado.celular,
            'email': asociado.email,
            'id_asociacion': asociado.id_asociacion,
            'cargo': asociado.cargo,
            'fecha_digitacion': asociado.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(resultado)
    except NotFound:
        return jsonify({"error": "Asociado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener el asociado", "detalle": str(e)}), 500
    

@asociado_bp.route('/asociado/<int:id>/nombre', methods=['GET'])
def obtener_asociado_nom(id):
    try:
        asociado = Asociado.query.get_or_404(id)
        resultado = {
            'nombre': asociado.nombre,
        }
        return jsonify(resultado), 200
    except NotFound:
        return jsonify({"error": "Asociado no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener el asociado", "detalle": str(e)}), 500


@asociado_bp.route('/asociado/<int:nuip_asociado>', methods=['PUT'])
def actualizar_asociado(nuip_asociado):
    try:
        data = request.json
        asociado = Asociado.query.get_or_404(nuip_asociado)
        
        asociado.tipo_nuip = data.get('tipo_nuip', asociado.tipo_nuip)
        asociado.nombre = data.get('nombre', asociado.nombre)
        asociado.apellidos = data.get('apellidos', asociado.apellidos)
        asociado.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
        asociado.estado_civil = data.get('estado_civil', asociado.estado_civil)
        asociado.sexo = data.get('sexo', asociado.sexo)
        asociado.poblacion_especial = data.get('poblacion_especial', asociado.poblacion_especial)
        asociado.direccion = data.get('direccion', asociado.direccion)
        asociado.discapacidad_fisica = data.get('discapacidad_fisica', asociado.discapacidad_fisica)
        asociado.celular = data.get('celular', asociado.celular)
        asociado.email = data.get('email', asociado.email)
        asociado.id_asociacion = data.get('id_asociacion', asociado.id_asociacion)
        asociado.cargo = data.get('cargo', asociado.cargo)
        
        db.session.commit()
        return jsonify({"mensaje": "Asociado actualizado exitosamente"})
    except NotFound:
        return jsonify({"error": "Asociado no encontrado"}), 404
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al actualizar el asociado", "detalle": str(e)}), 500


@asociado_bp.route('/asociado/<int:nuip_asociado>', methods=['DELETE'])
def eliminar_asociado(nuip_asociado):
    try:
        asociado = Asociado.query.get_or_404(nuip_asociado)
        db.session.delete(asociado)
        db.session.commit()
        return jsonify({"mensaje": "Asociado eliminado exitosamente"})
    except NotFound:
        return jsonify({"error": "Asociado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al eliminar el asociado", "detalle": str(e)}), 500
