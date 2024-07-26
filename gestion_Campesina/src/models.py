# src/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Asociacion(db.Model):
    __tablename__ = 'asociacion'
    id_asociacion = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre_asociacion = db.Column(db.String(255), nullable=False)
    siglas = db.Column(db.String(20), nullable=False)
    fecha_constitucion = db.Column(db.Date, nullable=False)
    fecha_digitacion = db.Column(db.DateTime, default=datetime.now)
    objetivo = db.Column(db.Text)
    direccion = db.Column(db.String(255))
    representante_legal = db.Column(db.String(100))
    celular = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Asociacion {self.nombre_asociacion}>'

class Asociado(db.Model):
    __tablename__ = 'asociado'
    nuip_asociado = db.Column(db.Integer, primary_key=True, autoincrement=False)
    tipo_nuip = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(70), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    estado_civil = db.Column(db.String(70), nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    poblacion_especial = db.Column(db.String(70))
    direccion = db.Column(db.String(255))
    discapacidad_fisica = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(100))
    id_asociacion = db.Column(db.Integer, db.ForeignKey('asociacion.id_asociacion'), nullable=False)
    cargo = db.Column(db.Integer)
    fecha_digitacion = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f'<Asociado {self.nombre}>'

class NucleoFamiliar(db.Model):
    __tablename__ = 'nucleo_familiar'
    nuip_miembro = db.Column(db.Integer, primary_key=True, autoincrement=False)
    tipo_nuip = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(70), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    estado_civil = db.Column(db.String(70), nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    poblacion_especial = db.Column(db.String(70))
    direccion = db.Column(db.String(255))
    discapacidad_fisica = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(100))
    parentesco = db.Column(db.String(20), nullable=False)
    nuip_asociado = db.Column(db.Integer, db.ForeignKey('asociado.nuip_asociado'), nullable=False)
    fecha_digitacion = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f'<Miembro {self.nombre}>'

class Predio(db.Model):
    __tablename__ = 'predio'
    id_predio = db.Column(db.Integer, primary_key=True)
    nombre_predio = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    hectareas = db.Column(db.Integer, nullable=False)
    nuip_asociado = db.Column(db.Integer, db.ForeignKey('asociado.nuip_asociado'), nullable=False, unique=True)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_digitacion = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f'<Predio {self.nombre_predio}>'

class Cultivo(db.Model):
    __tablename__ = 'cultivo'
    id_cultivo = db.Column(db.Integer, primary_key=True)
    tipo_cultivo = db.Column(db.String(100), nullable=False)
    area_cultivada = db.Column(db.Integer, nullable=False)
    fecha_siembra = db.Column(db.Date, nullable=False)
    fecha_cosecha = db.Column(db.Date, nullable=False)
    observacion = db.Column(db.Text)
    nuip_asociado = db.Column(db.Integer, db.ForeignKey('asociado.nuip_asociado'), nullable=False)
    id_predio = db.Column(db.Integer, db.ForeignKey('predio.id_predio'), nullable=False)
    fecha_digitacion = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f'<Cultivo {self.tipo_cultivo}>'
