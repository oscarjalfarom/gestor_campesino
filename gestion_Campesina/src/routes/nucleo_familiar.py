# src/routes/nucleo_familiar.py
from flask import Blueprint, request, jsonify
from src.models import db, NucleoFamiliar
from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest

nucleo_familiar_bp = Blueprint('nucleo_familiar', __name__)

@nucleo_familiar_bp.route('/nucleo_familiar', methods=['POST'])
def crear_miembro():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # Lista de campos obligatorios
    campos_obligatorios = [
        'nuip_miembro', 'tipo_nuip', 'nombre', 'apellidos', 
        'fecha_nacimiento', 'estado_civil', 'sexo', 'parentesco', 'nuip_asociado'
    ]

    # Verificar que todos los campos obligatorios están presentes
    for campo in campos_obligatorios:
        if campo not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {campo}"}), 400

    try:
        nuevo_miembro = NucleoFamiliar(
            nuip_miembro=data['nuip_miembro'],
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
            parentesco=data['parentesco'],
            nuip_asociado=data['nuip_asociado'],
        )
        db.session.add(nuevo_miembro)
        db.session.commit()
        return jsonify({"mensaje": "Miembro creado exitosamente"}), 201

    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Log the exception if needed
        # current_app.logger.error(f'Error creating miembro: {str(e)}')
        return jsonify({"error": "Error al crear el miembro", "detalle": str(e)}), 500


@nucleo_familiar_bp.route('/nucleo_familiar', methods=['GET'])
def obtener_miembros():
    try:
        miembros = NucleoFamiliar.query.all()
        resultado = [{
            'nuip_miembro': miembro.nuip_miembro,
            'tipo_nuip': miembro.tipo_nuip,
            'nombre': miembro.nombre,
            'apellidos': miembro.apellidos,
            'fecha_nacimiento': miembro.fecha_nacimiento.strftime('%Y-%m-%d'),
            'estado_civil': miembro.estado_civil,
            'sexo': miembro.sexo,
            'poblacion_especial': miembro.poblacion_especial,
            'direccion': miembro.direccion,
            'discapacidad_fisica': miembro.discapacidad_fisica,
            'celular': miembro.celular,
            'email': miembro.email,
            'parentesco': miembro.parentesco,
            'nuip_asociado': miembro.nuip_asociado,
            'fecha_digitacion': miembro.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        } for miembro in miembros]
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": "Error al obtener los miembros", "detalle": str(e)}), 500


@nucleo_familiar_bp.route('/nucleo_familiar/<int:nuip_miembro>', methods=['GET'])
def obtener_miembro(nuip_miembro):
    try:
        miembro = NucleoFamiliar.query.get_or_404(nuip_miembro)
        resultado = {
            'nuip_miembro': miembro.nuip_miembro,
            'tipo_nuip': miembro.tipo_nuip,
            'nombre': miembro.nombre,
            'apellidos': miembro.apellidos,
            'fecha_nacimiento': miembro.fecha_nacimiento.strftime('%Y-%m-%d'),
            'estado_civil': miembro.estado_civil,
            'sexo': miembro.sexo,
            'poblacion_especial': miembro.poblacion_especial,
            'direccion': miembro.direccion,
            'discapacidad_fisica': miembro.discapacidad_fisica,
            'celular': miembro.celular,
            'email': miembro.email,
            'parentesco': miembro.parentesco,
            'nuip_asociado': miembro.nuip_asociado,
            'fecha_digitacion': miembro.fecha_digitacion.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(resultado)
    except NotFound:
        return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener el miembro", "detalle": str(e)}), 500


@nucleo_familiar_bp.route('/nucleo_familiar/<int:nuip_miembro>', methods=['PUT'])
def actualizar_miembro(nuip_miembro):
    try:
        data = request.json
        miembro = NucleoFamiliar.query.get_or_404(nuip_miembro)
        
        miembro.tipo_nuip = data.get('tipo_nuip', miembro.tipo_nuip)
        miembro.nombre = data.get('nombre', miembro.nombre)
        miembro.apellidos = data.get('apellidos', miembro.apellidos)
        miembro.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
        miembro.estado_civil = data.get('estado_civil', miembro.estado_civil)
        miembro.sexo = data.get('sexo', miembro.sexo)
        miembro.poblacion_especial = data.get('poblacion_especial', miembro.poblacion_especial)
        miembro.direccion = data.get('direccion', miembro.direccion)
        miembro.discapacidad_fisica = data.get('discapacidad_fisica', miembro.discapacidad_fisica)
        miembro.celular = data.get('celular', miembro.celular)
        miembro.email = data.get('email', miembro.email)
        miembro.parentesco = data.get('parentesco', miembro.parentesco)
        miembro.nuip_asociado = data.get('nuip_asociado', miembro.nuip_asociado)
        
        db.session.commit()
        return jsonify({"mensaje": "Miembro actualizado exitosamente"})
    except NotFound:
        return jsonify({"error": "Miembro no encontrado"}), 404
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al actualizar el miembro", "detalle": str(e)}), 500


@nucleo_familiar_bp.route('/nucleo_familiar/<int:nuip_miembro>', methods=['DELETE'])
def eliminar_miembro(nuip_miembro):
    try:
        miembro = NucleoFamiliar.query.get_or_404(nuip_miembro)
        db.session.delete(miembro)
        db.session.commit()
        return jsonify({"mensaje": "Miembro eliminado exitosamente"})
    except NotFound:
        return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al eliminar el miembro", "detalle": str(e)}), 500
