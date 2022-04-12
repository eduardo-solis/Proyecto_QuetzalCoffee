
from telnetlib import RCP
from flask_sqlalchemy import SQLAlchemy

from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
import datetime

from pyparsing import col

db = SQLAlchemy()

dia = datetime.datetime.now()
fecha = '' + dia.strftime('%Y') + '/' + dia.strftime('%m') + '/' + dia.strftime('%d')


# Definimos la tabla relacional
users_roles = db.Table('users_roles',
                        db.Column('userId', db.Integer, db.ForeignKey('user.id')),
                        db.Column('roleId', db.Integer, db.ForeignKey('role.id'))
                        )

# DEFINICION DE LA CLASE TIPOUSUARIO
class TipoUsuario(db.Model):
    '''Modelo del tipo de usuario'''
    __tablename__ = 'tipoUsuario'
    
    idTipoUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable = False)
    
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date)
    
    def __init__(self, idTipoUsuario, nombre, creadoPor):
        self. idTipoUsuario = idTipoUsuario
        self.nombre = nombre
        self.creadoPor = creadoPor
        self.fechaCreacion = fecha
    

# Definimos la clase del usuario
class User(UserMixin, db.Model):
    ''' User account model '''
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100), nullable = False)
    
    estatus = db.Column(db.Integer, default = 1)
    
    primerApellido = db.Column(db.String(100), nullable = False)
    segundoApellido = db.Column(db.String(100))
    fechaNac = db.Column(db.Date, nullable = False)
    # Domicilio
    calle = db.Column(db.String(100), nullable = False)
    numero = db.Column(db.String(50), nullable = False)
    colonia = db.Column(db.String(100), nullable = False)
    codigoPostal = db.Column(db.String(5), nullable = False)
    
    # Contacto
    telefono = db.Column(db.String(10), nullable = False)
    sueldo = db.Column(db.Numeric(15,2))
    hrsTrabajo = db.Column(db.Numeric)
    
    tipoUsuario = db.Column(db.Integer, db.ForeignKey('tipoUsuario.idTipoUsuario'), nullable = False)
    idVentaActual = db.Column(db.Integer)
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date, default = fecha)
    
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    
    roles = db.relationship('Role', 
                            secondary = users_roles, 
                            backref = db.backref('users', lazy = 'dynamic'))
    

class Role(RoleMixin, db.Model):
    '''Role model'''
    
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(255))
    
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date, default = fecha)

userDataStore = SQLAlchemyUserDatastore(db, User, Role)

class Proveedor (db.Model):
    
    __tablename__ = 'proveedor'
    
    idProveedor = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(90))
    rfc = db.Column(db.String(30))
    razonSocial = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    # Domicilio
    calle = db.Column(db.String(100), nullable = False)
    numero = db.Column(db.String(50), nullable = False)
    colonia = db.Column(db.String(100), nullable = False)
    codigoPostal = db.Column(db.String(5), nullable = False)
    
    estatus = db.Column(db.Integer, default = 1)
    
    telefono = db.Column(db.String(10), nullable = False)
    
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date, default = fecha)
    
    def __init__(self, nombre, rfc, rS, calle, numero, colonia, codigoPostal, telefono, correo, creadoPor):
        self.nombre = nombre
        self.rfc = rfc
        self.calle = calle
        self.numero = numero
        self.colonia = colonia
        self.codigoPostal = codigoPostal
        self.telefono = telefono
        self.email = correo
        self.razonSocial = rS
        self.creadoPor = creadoPor

class MateriaPrima (db.Model):
    
    __tablename__ = 'materiaprima'
    
    idMateriaPrima = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(90))
    descripcion = db.Column(db.Text, nullable = False)  
    cantidad = db.Column(db.Float, nullable = False)
    foto = db.Column(db.Text, nullable = False)  
    unidadMedida = db.Column(db.String(10))     
    precioCompra = db.Column(db.Float)
    idProveedor = db.Column(db.Integer, db.ForeignKey('proveedor.idProveedor'), nullable=False)
    #estatus del registro
    isActive = db.Column(db.Integer, default = 1)
    #estatus de materia prima
    estatus = db.Column(db.Integer, default = 1)
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date, default = fecha)

    def __init__(self, nombre, descripcion,cantidad,foto,unidadMedida,
                PrecioCompra,creadoPor, idProveedor):
        #self.idMateriaPrima = idMateriaPrima
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad=cantidad
        self.foto=foto
        self.unidadMedida=unidadMedida
        self.precioCompra=PrecioCompra
        self.idProveedor=idProveedor
        self.creadoPor = creadoPor
        #self.modificadoPor=modificadoPor

class TipoProducto(db.Model):
    __tablename__ = 'tipoProducto'
    
    idTipoProducto = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(90))
    
    estatus = db.Column(db.Integer, default = 1)
    
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date)
    

class Producto (db.Model):
    
    __tablename__ = 'producto'
    
    idProducto = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    descripcion = db.Column(db.Text, nullable = False)
    cantidad = db.Column(db.Float)
    unidadMedida = db.Column(db.String(10))
    precioVenta = db.Column(db.Float)    
    tipoProducto = db.Column(db.Integer, db.ForeignKey('tipoProducto.idTipoProducto'), nullable=False)    
    foto = db.Column(db.Text, nullable = False)    
    isActive = db.Column(db.Integer, nullable = False, default=1)    
    estatus = db.Column(db.Integer, default = 1)
    
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date, default = fecha)
    
    def __init__(self,  nombre, descripcion, cantidad,unidadMedida,precioVenta,tipoProducto,foto,creadoPor):
    
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.unidadMedida = unidadMedida
        self.precioVenta = precioVenta
        self.tipoProducto = tipoProducto
        self.foto = foto
        self.creadoPor = creadoPor

class Compra (db.Model):
    
    __tablename__ = 'compra'
    
    idCompra = db.Column(db.Integer, primary_key = True)
    folio = db.Column(db.Integer)
    fechaCompra = db.Column(db.Date, nullable = False, default = fecha)
    totalCompra = db.Column(db.Float)
    idEmpleado = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #estatus de compra
    estatus = db.Column(db.Integer, default = 1)
    
        
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date,  default = fecha)

class DetalleCompra (db.Model):
    
    __tablename__ = 'detalleCompra'
    
    idDetalleCompra = db.Column(db.Integer, primary_key = True)
    total = db.Column(db.Float)
    cantidad = db.Column(db.Float, nullable = False)
    idMateriaPrima = db.Column(db.Integer, db.ForeignKey('materiaprima.idMateriaPrima'), nullable=False)
    idCompra = db.Column(db.Integer, db.ForeignKey('compra.idCompra'), nullable=False)

    #estatus de detalle venta
    estatus = db.Column(db.Integer, default = 1)

class Venta (db.Model):
    
    __tablename__ = 'venta'
    
    
    idVenta = db.Column(db.Integer, primary_key = True)
    folio = db.Column(db.Integer)
    fechaVenta = db.Column(db.Date, nullable = False, default = fecha)
    totalVenta = db.Column(db.Float)
    idEmpleado = db.Column(db.Integer, default = 0)
    #------------------------------------------------------------
    idCliente = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #estatus venta
    estatus = db.Column(db.Integer, default = 1)
    
    # Datos de trasabilidad
    creadoPor = db.Column(db.Integer, nullable = False)
    fechaCreacion = db.Column(db.Date, nullable = False, default = fecha)
    modificadoPor = db.Column(db.Integer)
    fechaModificacion = db.Column(db.Date,  default = fecha)
    
    def __init__(self, folio, idCliente, creadoPor):
        self.folio = folio
        self.idCliente = idCliente
        self.creadoPor = creadoPor


class DetalleVenta (db.Model):
    
    __tablename__ = 'detalleVenta'
    
    
    idDetalleVenta = db.Column(db.Integer, primary_key = True)
    idVenta = db.Column(db.Integer, db.ForeignKey('venta.idVenta'), nullable = False)
    total = db.Column(db.Float)
    cantidad = db.Column(db.Float, nullable = False)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False)
    
    #estatus de detalle venta
    estatus = db.Column(db.Integer, default = 1)
    
    def __init__(self, idVenta, total, cantidad, idProducto):
        self.idVenta = idVenta
        self.total = total
        self.cantidad = cantidad
        self.idProducto = idProducto

class MateriaProducto (db.Model):
    __tablename__ = 'materiaProducto'
    
    idMateriaProducto = db.Column(db.Integer, primary_key = True)
    idProducto = db.Column(db.Integer,  db.ForeignKey('producto.idProducto'), nullable=False)
    idMateriaPrima = db.Column(db.Integer,   db.ForeignKey('materiaprima.idMateriaPrima'), nullable=False)
    cantidad = db.Column(db.Float, nullable = False)
    
    #estatus de detalle venta
    estatus = db.Column(db.Integer, default = 1)
    
