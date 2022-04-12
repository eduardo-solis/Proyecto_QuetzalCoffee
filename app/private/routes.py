from flask import render_template, flash, current_app, redirect, request, url_for

from flask_security import current_user, roles_accepted, login_required, roles_required

# Modulo para el cifrado del passwords
from werkzeug.security import generate_password_hash

import datetime
import mysql.connector

from ..forms import CarritoInsumos, RegistroEmpleadoForm, RegistroMateriaForm, RegistroProductoForm, RegistroRecetaForm, RegistroRolForm, RegistroClienteForm, RegistroProveedorForm, CarritoCompra, HistorialCompra, PagoCompra
from ..models import MateriaPrima, Producto, User, db, userDataStore, Proveedor

from . import private

@private.route('/c_insumos')
@login_required
@roles_accepted('admin','gerente','empleado')
def c_insumos():
    carritoInsumos_form = CarritoInsumos()
    
    context = {
        'form' : carritoInsumos_form
    }
    
    return render_template('CatalogoInsumos.html', **context)

@private.route('/roles')
@login_required
@roles_required('admin')
def roles():

    rol_form = RegistroRolForm()
    context = {
        'form': rol_form
    }

    return render_template('GestionRoles.html', **context)

@private.route('/clientes', methods = ['GET','POST'])
@login_required
@roles_accepted('admin','gerente')
def clientes():
    date = datetime.datetime.now()
    register_form = RegistroClienteForm()
    lista_clientes = []
    conexion = mysql.connector

    if current_user.tipoUsuario == 4:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )
    elif current_user.tipoUsuario == 3:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )

    cursor = conexion.cursor()
    sql = 'SELECT * FROM user WHERE tipoUsuario = 1  AND estatus = 1'
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conexion.close()
    cliente = {}
    for row in rows:
        cliente['id'] = row[0]
        cliente['name'] = row[1]
        cliente['correo'] = row[2]
        cliente['password'] = row[3]
        cliente['estatus'] = row[4]
        cliente['primerApellido'] = row[5]
        cliente['segundoApellido'] = row[6]
        cliente['fechaNac'] = row[7]
        cliente['calle'] = row[8]
        cliente['numero'] = row[9]
        cliente['colonia'] = row[10]
        cliente['codigoPostal'] = row[11]
        cliente['telefono'] = row[12]
        cliente['sueldo'] = row[13]
        cliente['hrsTrabajo'] = row[14]
        cliente['tipoUsuario'] = row[15]
        cliente['creadoPor'] = row[16]
        cliente['fechaCreacion'] = row[17]
        cliente['modificadoPor'] = row[18]
        cliente['fechaModificacion'] = row[19]
        cliente['active'] = row[20]
        cliente['confirmed_at'] = row[21]

        lista_clientes.append(cliente)

        cliente = {}

    #lista_empleados = rows

    context = {
        'form': register_form,
        'lista': lista_clientes
    }
    
    if register_form.validate_on_submit():
        
        nombre = register_form.nombre.data
        primerApellido = register_form.primerApellido.data
        segundoApellido = register_form.segundoApellido.data
        fechaNac = register_form.fechaNac.data
        
        calle = register_form.calle.data
        numero = register_form.numero.data
        colonia = register_form.colonia.data
        cp = register_form.codigoPostal.data
        
        telefono = register_form.telefono.data
        email = register_form.correo.data
        password = register_form.password.data
        
        # Consultamos si existe un usuario ya registrado con ese email.
        user = User.query.filter_by(email = email).first()
        
        # Si se encontró un usuario, redireccionamos de regreso al registro
        if user:
            flash('El correo electronico ya existe')
            
            mensaje = '''
            Registro denegado el dia {} a las {}, 
            debido a que ya existe el usuario para el correo : {}
            '''.format(date.date(), date.strftime('%X'),email)
            
            current_app.logger.warning(mensaje)
            
            return redirect(url_for('private.clientes'))
        
        # Creamos un nuevo usuario con los datos del formulario
        # Hacemos un hash a la contraseña para que no se guarde la version en texto plano
        
        userDataStore.create_user(
            name = nombre,
            primerApellido = primerApellido,
            segundoApellido = segundoApellido,
            fechaNac = fechaNac,
            
            calle = calle,
            numero = numero,
            colonia = colonia,
            codigoPostal = cp,
            telefono = telefono,
            email = email,
            password = generate_password_hash(password, method = 'sha256'),
            tipoUsuario = 1,
            creadoPor = 1
        )
        
        # Añadimos el usuario a la BD
        db.session.commit()
        
        conexion = mysql.connector.connect(
            host = 'localhost',
            port=3306,
            user = 'gerente',
            password = 'gerente123',
            db='db_quetzal_coffee'
        )
        
        cursor = conexion.cursor()
        select = 'SELECT id FROM user ORDER BY id DESC LIMIT 1'
        select2 = 'SELECT tipoUsuario FROM user ORDER BY id DESC LIMIT 1'
        
        cursor.execute(select)
        row1 = cursor.fetchone()
        id = 0
        for item in row1:
            id = item
        
        cursor.execute(select2)
        row2 = cursor.fetchone()
        tipo = 0
        for item in row2:
            tipo = item
        
        sql = 'INSERT INTO users_roles (userId, roleId) values ({},{})'.format(id,tipo)
        cursor.execute(sql)
        conexion.commit()
        cursor.close()
        conexion.close()
        
        
        mensaje = '''
        Se ha creado el registro del usuario para el correo: {}
        el dia {} a las {}
        '''.format(email,date.date(), date.strftime('%X'))
        current_app.logger.info(mensaje)
        
        return redirect(url_for('private.clientes'))
    return render_template('GestionClientes.html', **context)

@private.route('/cliente/delete/<id>')
@login_required
@roles_accepted('admin', 'gerente')
def delete_cliente(id):

    user = ''
    password = ''

    if current_user.tipoUsuario == 4:
        user = 'gerente'
        password = 'gerente123'
    elif current_user.tipoUsuario == 3:
        user = 'gerente',
        password = 'gerente123'

    conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= user,
        password= password,
        db='db_quetzal_coffee'
    )

    cursor = conexion.cursor()
    
    sql = ''' UPDATE user SET estatus = 2 WHERE id = {} '''.format(id)
    
    cursor.execute(sql)
    conexion.commit()
    
    cursor.close()
    conexion.close()
    
    return redirect(url_for('private.clientes'))

# GET - EMPLEADO
@private.route('/empleados', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente')
def empleados():

    empleados_form = RegistroEmpleadoForm()
    lista_empleados = []
    user = ''
    password = ''

    if current_user.tipoUsuario == 4:
        user = 'gerente'
        password = 'gerente123'
    elif current_user.tipoUsuario == 3:
        user = 'gerente',
        password = 'gerente123'

    conexion = mysql.connector.connect(
        host='localhost',
        port=3306,
        user=user,
        password=password,
        db='db_quetzal_coffee'
    )

    cursor = conexion.cursor()
    sql = 'SELECT * FROM user WHERE tipoUsuario != 1  AND tipoUsuario != 4 AND estatus = 1'
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conexion.close()
    empleado = {}
    for row in rows:
        empleado['id'] = row[0]
        empleado['name'] = row[1]
        empleado['correo'] = row[2]
        empleado['password'] = row[3]
        empleado['estatus'] = row[4]
        empleado['primerApellido'] = row[5]
        empleado['segundoApellido'] = row[6]
        empleado['fechaNac'] = row[7]
        empleado['calle'] = row[8]
        empleado['numero'] = row[9]
        empleado['colonia'] = row[10]
        empleado['codigoPostal'] = row[11]
        empleado['telefono'] = row[12]
        empleado['sueldo'] = row[13]
        empleado['hrsTrabajo'] = row[14]
        empleado['tipoUsuario'] = row[15]
        empleado['creadoPor'] = row[16]
        empleado['fechaCreacion'] = row[17]
        empleado['modificadoPor'] = row[18]
        empleado['fechaModificacion'] = row[19]
        empleado['active'] = row[20]
        empleado['confirmed_at'] = row[21]

        lista_empleados.append(empleado)

        empleado = {}

    #lista_empleados = rows

    context = {
        'form': empleados_form,
        'lista': lista_empleados
    }

    if empleados_form.validate_on_submit():
        date = datetime.datetime.now()
        nombre = empleados_form.nombre.data
        primerApellido = empleados_form.primerApellido.data
        segundoApellido = empleados_form.segundoApellido.data
        calle = empleados_form.calle.data
        numero = empleados_form.numero.data
        colonia = empleados_form.colonia.data
        cp = empleados_form.codigoPostal.data

        sueldo = abs(empleados_form.sueldo.data)
        hrsTrabajo = abs(empleados_form.hrsTrabajo.data)
        telefono = empleados_form.telefono.data
        email = empleados_form.correo.data
        password = empleados_form.password.data
        fechaNac = empleados_form.fechaNac.data

        tipoEmpleado = empleados_form.tipoEmpleado.data
        creadoPor = current_user.id

        # Consultamos si existe un empleado ya registrado con el correo.
        user = User.query.filter_by(email=email).first()

        if user:  # Si se encontró un usuario, quiere decir que ya esta registrado

            flash('Ya existe un Empleado/Gerente con este mismo correo')

            mensaje = '''
            No se ha realizado el registro de un empleado con el correo {},  el dia {} a las {},
            por el usuario {}, debido a que ya existe un registro con el mismo correo
            '''.format(email, date.date(), date.strftime('%X'), current_user.id)

            current_app.logger.info(mensaje)
            return redirect(url_for('private.empleados'))

        # Creamos un nuevo empleado con los datos del formulario

        userDataStore.create_user(
            name=nombre,
            primerApellido=primerApellido,
            segundoApellido=segundoApellido,
            fechaNac=fechaNac,

            calle=calle,
            numero=numero,
            colonia=colonia,
            codigoPostal=cp,
            telefono=telefono,
            email=email,
            password=generate_password_hash(password, method='sha256'),
            sueldo=sueldo,
            hrsTrabajo=hrsTrabajo,
            tipoUsuario=tipoEmpleado,
            creadoPor=creadoPor
        )
        db.session.commit()

        user = ''
        password = ''

        if current_user.tipoUsuario == 4:
            user = 'gerente'
            password = 'gerente123'
        elif current_user.tipoUsuario == 3:
            user = 'gerente',
            password = 'gerente123'

        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user=user,
            password=password,
            db='db_quetzal_coffee'
        )

        cursor = conexion.cursor()
        select = 'SELECT id FROM user ORDER BY id DESC LIMIT 1'
        select2 = 'SELECT tipoUsuario FROM user ORDER BY id DESC LIMIT 1'

        cursor.execute(select)
        row1 = cursor.fetchone()
        id = 0
        for item in row1:
            id = item

        cursor.execute(select2)
        row2 = cursor.fetchone()
        tipo = 0
        for item in row2:
            tipo = item

        sql = 'INSERT INTO users_roles (userId, roleId) values ({},{})'.format(
            id, tipo)
        cursor.execute(sql)
        conexion.commit()
        cursor.close()
        conexion.close()

        mensaje = '''
        El usuario con id {} ha creado el registro de un empleado
        el dia {} a las {}
        '''.format(current_user.id, date.date(), date.strftime('%X'))
        current_app.logger.info(mensaje)
        return redirect(url_for('private.empleados'))
    return render_template('GestionEmpleado.html', **context)

@private.route('/empleado/update/<id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','gerente')
def update_empleado(id):
    usuario = User.query.get(id)
    if request.method == 'POST':
        usuario.calle = request.form['calle']
        usuario.numero = request.form['numero']
        usuario.colonia = request.form['colonia']
        usuario.codigoPostal = request.form['codigoPostal']
        usuario.sueldo = abs(request.form['sueldo'])
        usuario.hrsTrabajo = abs(request.form['hrsTrabajo'])
        usuario.telefono = request.form['telefono']
        usuario.email = request.form['correo']
        usuario.tipoUsuario = request.form.get('algo')
        
        db.session.commit()
        
        return redirect(url_for('private.empleados'))
    
    context = {
        'u' : usuario,
        'form' : RegistroEmpleadoForm()
    }
    
    return render_template('updateEmpleado.html', **context)

@private.route('/empleado/delete/<id>')
@login_required
@roles_accepted('admin', 'gerente')
def delete_empleado(id):

    user = ''
    password = ''

    if current_user.tipoUsuario == 4:
        user = 'gerente'
        password = 'gerente123'
    elif current_user.tipoUsuario == 3:
        user = 'gerente',
        password = 'gerente123'

    conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= user,
        password= password,
        db='db_quetzal_coffee'
    )

    cursor = conexion.cursor()
    
    sql = ''' UPDATE user SET estatus = 2 WHERE id = {} '''.format(id)
    
    cursor.execute(sql)
    conexion.commit()
    
    cursor.close()
    conexion.close()
    
    return redirect(url_for('private.empleados'))

@private.route('/ventas')
@login_required
@roles_accepted('admin', 'gerente', 'empleado')
def ventas():
    return render_template('HistorialCompraCliente1.html')

@private.route('/productos', methods=['GET','POST'])
@login_required
@roles_accepted('admin', 'gerente', 'empleado')
def productos():
    productos_form = RegistroProductoForm()
    
    lista_productos = []
    user = ''
    password = ''

    conexion = mysql.connector

    if current_user.tipoUsuario == 4:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )
    elif current_user.tipoUsuario == 3:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )
    elif current_user.tipoUsuario == 2:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )

    cursor = conexion.cursor()
    sql = 'SELECT * FROM producto WHERE isActive = 1'
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conexion.close()
    producto = {}
    for row in rows:
        producto['idProducto'] = row[0]
        producto['nombre'] = row[1]
        producto['descripcion'] = row[2]
        producto['cantidad'] = row[3]
        producto['UnidadMedida'] = row[4]
        producto['precioVenta'] = row[5]
        producto['tipoProducto'] = row[6]
        producto['foto'] = row[7]
        producto['isActive'] = row[8]
        producto['estatus'] = row[9]
        producto['creadoPor'] = row[10]
        producto['fechaCreacion'] = row[11]
        producto['modificadoPor'] = row[12]
        producto['fechaModificacion'] = row[13]

        lista_productos.append(producto)

        producto = {}
    
    context = {
        'form': productos_form,
        'productos':lista_productos
    }
    
    if productos_form.validate_on_submit():
        nombre = productos_form.nombre.data
        descripcion = productos_form.descripcion.data
        cantidad = abs(productos_form.cantidad.data)
        precio = abs(productos_form.precioVenta.data)
        tipoProducto = productos_form.tipoProducto.data
        foto = productos_form.foto.data
        
        nuevo_producto = Producto(nombre=nombre,
                                    descripcion=descripcion,
                                    precioVenta=precio,
                                    tipoProducto=tipoProducto,
                                    cantidad=cantidad,
                                    creadoPor=current_user.id,
                                    foto= foto,
                                    unidadMedida='ml'
                                )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        context = {
            'form': productos_form
        }
        return redirect(url_for('private.productos'))
    
    return render_template ('GestionProducto.html',**context)

@private.route('/productos/delete/<id>')
@login_required
@roles_accepted('admin', 'gerente')
def delete_producto(id):
    user = ''
    password = ''

    if current_user.tipoUsuario == 4:
        user = 'gerente'
        password = 'gerente123'
    elif current_user.tipoUsuario == 3:
        user = 'gerente',
        password = 'gerente123'

    conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= user,
        password= password,
        db='db_quetzal_coffee'
    )

    cursor = conexion.cursor()
    
    sql = ''' UPDATE producto SET isActive = 0 WHERE idProducto = {} '''.format(id)
    
    cursor.execute(sql)
    conexion.commit()
    
    cursor.close()
    conexion.close()
    
    return redirect(url_for('private.productos'))

@private.route('/productos/update/<id>', methods=['POST','GET'])
@login_required
@roles_accepted('admin','gerente')
def update_producto(id):
    
    producto = Producto.query.get(id)
    
    productos_form = RegistroProductoForm()
    if request.method == 'POST':
        producto.precioVenta = abs(request.form['precioVenta'])
        
        if request.form['foto'] != '' and request.form['foto'] != ' ' and request.form['foto'] != '   ':
            producto.foto = request.form['foto']
        
        db.session.commit()        
        return redirect(url_for('private.productos'))
    context = {
            'form': productos_form,
            'producto':producto
        }
    return render_template('UpdateProducto.html',**context)

@private.route('/recetas/update/<id>',methods = ['POST','GET'])
@login_required
@roles_accepted('admin', 'gerente')
def recetas_post(id):
    recetas_form = RegistroRecetaForm()
    
    productoVal = Producto.query.get(id)
    productos_form = RegistroProductoForm()
    if request.method == 'POST':
        productoVal.nombre = request.form['nombre']
        productoVal.descripcion = request.form['descripcion']
        productoVal.foto = request.form['foto']
        productoVal.precioVenta = request.form['precioVenta']
        
        db.session.commit()        
        return redirect(url_for('private.recetas'))
    
    lista_productos = []
    user = ''
    password = ''

    if current_user.tipoUsuario == 4:
        user = 'gerente'
        password = 'gerente123'
    elif current_user.tipoUsuario == 3:
        user = 'gerente',
        password = 'gerente123'

    conexion = mysql.connector.connect(
        host='localhost',
        port=3306,
        user=user,
        password=password,
        db='db_quetzal_coffee'
    )

    cursor = conexion.cursor()
    sql = 'SELECT * FROM materiaprima WHERE isActive = 1'
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conexion.close()
    producto = {}
    for row in rows:
        producto['idMateriaPrima'] = row[0]
        producto['nombre'] = row[1]
        producto['descripcion'] = row[2]
        producto['cantidad'] = row[3]
        producto['unidadMedida'] = row[4]
        producto['precioCompra'] = row[5]
        producto['idProveedor'] = row[6]
        producto['foto'] = row[7]
        producto['isActive'] = row[8]
        producto['estatus'] = row[9]
        producto['creadoPor'] = row[10]
        producto['fechaCreacion'] = row[11]
        producto['modificadoPor'] = row[12]
        producto['fechaModificacion'] = row[13]
       

        lista_productos.append(producto)

        producto = {}
    
    
    
    context = {
            'form': productos_form,
            'productoVal':productoVal,
            'lista_productos': lista_productos
        }
    return render_template('UpdateRecetas.html',**context)

@private.route('/proveedores', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente','empleado')
def proveedores():
    proveedores_form = RegistroProveedorForm()

    lista = Proveedor.query.filter_by(estatus = 1).all()

    context = {
        'form': proveedores_form,
        'lista' : lista
    }
    
    if proveedores_form.validate_on_submit():
        
        nombre = proveedores_form.nombre.data
        rfc = proveedores_form.rfc.data
        rS = proveedores_form.razonSocial.data
        calle = proveedores_form.calle.data
        numero = proveedores_form.numero.data
        colonia = proveedores_form.colonia.data
        cp = proveedores_form.codigoPostal.data
        telefono = proveedores_form.telefono.data
        correo = proveedores_form.correo.data
        
        p = Proveedor(nombre, rfc, rS, calle, numero, colonia,cp,telefono, correo, current_user.id)
        
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('private.proveedores'))
    return render_template ('GestionProveedor.html', **context)

@private.route('/proveedores/update/<id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','gerente')
def update_proveedor(id):
    p = Proveedor.query.get(id)
    if request.method == 'POST':
        p.calle = request.form['calle']
        p.numero = request.form['numero']
        p.colonia = request.form['colonia']
        p.codigoPostal = request.form['codigoPostal']
        p.telefono = request.form['telefono']
        p.email = request.form['correo']
        
        db.session.commit()
        
        return redirect(url_for('private.proveedores'))
    
    context = {
        'u' : p,
        'form' : RegistroProveedorForm()
    }
    
    return render_template('updateProveedor.html', **context)

@private.route('proveedores/delete/<id>')
@login_required
@roles_accepted('admin', 'gerente')
def deleteProveedor(id):
    
    user = ''
    password = ''
    
    conexion = mysql.connector

    if current_user.tipoUsuario == 4:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )
    elif current_user.tipoUsuario == 3:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )

    cursor = conexion.cursor()
    
    sql = ''' UPDATE proveedor SET estatus = 2 WHERE idProveedor = {} '''.format(id)
    
    cursor.execute(sql)
    conexion.commit()
    
    cursor.close()
    conexion.close()
    
    return redirect(url_for('private.proveedores'))

@private.route('/insumos', methods=['GET','POST'])
@login_required
@roles_accepted('admin','gerente', 'empleado')
def insumos():
    insumos_form = RegistroMateriaForm()
    
    lista_insumos = []
    
    lista_proveedores = Proveedor.query.filter_by(estatus = 1).all()

    conexion = mysql.connector

    if current_user.tipoUsuario == 4:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )
    elif current_user.tipoUsuario == 3:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )
    elif current_user.tipoUsuario == 2:
        conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'gerente',
        password= 'gerente123',
        db='db_quetzal_coffee'
        )

    cursor = conexion.cursor()
    sql = 'SELECT * FROM materiaprima WHERE isActive = 1'
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conexion.close()
    materiaprima = {}
    for row in rows:
        materiaprima['idMateriaPrima'] = row[0]
        materiaprima['nombre'] = row[1]
        materiaprima['descripcion'] = row[2]
        materiaprima['cantidad'] = row[3]
        materiaprima['foto'] = row[4]
        materiaprima['UnidadMedida'] = row[5]
        materiaprima['precioCompra'] = row[6]
        materiaprima['idProducto'] = row[7]
        materiaprima['isActive'] = row[8]
        materiaprima['estatus'] = row[9]
        materiaprima['creadoPor'] = row[10]
        materiaprima['fechaCreacion'] = row[11]
        materiaprima['modificadoPor'] = row[12]
        materiaprima['fechaModificacion'] = row[13]

        lista_insumos.append(materiaprima)

        materiaprima = {}
    
    context = {
        'form': insumos_form,
        'lista':lista_insumos,
        'proveedores' : lista_proveedores
    }
    
    if insumos_form.validate_on_submit():
        nombre = insumos_form.nombre.data
        descripcion = insumos_form.descripcion.data
        cantidad = abs(float(insumos_form.cantidad.data))
        unidadMedida = insumos_form.unidadMedida.data
        precioCompra = abs(insumos_form.precioCompra.data)
        foto = insumos_form.foto.data
        proveedor = request.form.get('proveedor')
        
        nuevo_insumo = MateriaPrima( nombre,
                                    descripcion=descripcion,
                                    cantidad=cantidad,
                                    foto= foto, 
                                    unidadMedida=unidadMedida,
                                    PrecioCompra=precioCompra,
                                    creadoPor=current_user.id,
                                    idProveedor=proveedor
                                )
        
        print(nuevo_insumo)
        
        db.session.add(nuevo_insumo)
        db.session.commit()
        
        return redirect(url_for('private.insumos'))
    
    return render_template ('GestionMateriaPrima.html',**context)


@private.route('/insumos/delete/<id>')
@login_required
@roles_accepted('admin', 'gerente')
def delete_insumos(id):
    user = ''
    password = ''

    if current_user.tipoUsuario == 4:
        user = 'gerente'
        password = 'gerente123'
    elif current_user.tipoUsuario == 3:
        user = 'gerente',
        password = 'gerente123'

    conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= user,
        password= password,
        db='db_quetzal_coffee'
    )

    cursor = conexion.cursor()
    
    sql = ''' UPDATE materiaprima SET isActive = 0 WHERE idMateriaPrima = {} '''.format(id)
    
    cursor.execute(sql)
    conexion.commit()
    
    cursor.close()
    conexion.close()
    
    return redirect(url_for('private.insumos'))

@private.route('/insumos/update/<id>', methods=['POST','GET'])
@login_required
@roles_accepted('admin', 'gerente')
def update_insumos(id):
    
    insumos = MateriaPrima.query.get(id)
    
    insumos_form = RegistroMateriaForm()
    if request.method == 'POST':
        
        insumos.precioCompra = abs(request.form['precioCompra'])
        
        if request.form['foto'] != '' and request.form['foto'] != ' ' and request.form['foto'] != '   ':
            insumos.foto = request.form['foto']
            
        db.session.commit()        
        return redirect(url_for('private.insumos'))
    
    context = {
            'form': insumos_form,
            'insumos': insumos
        }
    return render_template('updateMateriaPrima.html',**context)

@private.route('/carrito')
@login_required
@roles_accepted('admin', 'gerente', 'empleado')
def carrito():
    carrito_form = CarritoCompra()

    context = {
        'form': carrito_form
    }

    return render_template('CarritoCompra.html', **context)

@private.route('/historial')
@login_required
@roles_accepted('admin', 'gerente', 'empleado')
def historial():
    historial_compra_form = HistorialCompra()

    context = {
        'form': historial_compra_form
    }
    return render_template('HistorialCompra.html', **context)

@private.route('/pagoCompra')
@login_required
@roles_accepted('admin', 'gerente', 'empleado')
def pagoCompra():
    pago_compra = PagoCompra()

    context = {
        'form': pago_compra
    }
    return render_template('PagoCompra.html', **context)
