from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask_security import roles_required, login_required
from werkzeug.security import generate_password_hash

import mysql.connector
from . import public
from ..models import db, User, Producto, Venta, DetalleVenta
from ..forms import CarritoVenta, PagoVenta, HistorialVenta, RegistroClienteForm, CatalogoCliente

@public.route('/')
def principal():
    return render_template('inicio.html')

@public.route('/perfil', methods=['GET','POST'])
@login_required
@roles_required('cliente')
def perfil():
    
    usuario = User.query.get(current_user.id)
    
    if request.method == 'POST':
        usuario.calle = request.form['calle']
        usuario.numero = request.form['numero']
        usuario.colonia = request.form['colonia']
        usuario.codigoPostal = request.form['codigoPostal']
        usuario.telefono = request.form['telefono']
        usuario.email = request.form['correo']
        
        if request.form['password'] != '':
            usuario.password = generate_password_hash(request.form['password'], method='sha256')
        
        db.session.commit()
        
        return redirect(url_for('public.principal'))
    
    context = {
        'form' : RegistroClienteForm()
    }
    
    return render_template('Perfil.html', **context)

@public.route('/catalogo', methods=['GET'])
@login_required
@roles_required('cliente')
def catalogo():
    print('idVentaActual = ',current_user.idVentaActual)
    productos = Producto.query.all()
    catalogo_form = CatalogoCliente()
    
    context = {
        'lista' : productos,
        'form' : catalogo_form
    }
    
    return render_template('CatalogoProducto.html', **context)


@public.route('/catalogo/agregar/<idProducto>')
@login_required
@roles_required('cliente')
def cat_agregar(idProducto):
    
    conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'cliente',
        password= 'cliente123',
        db='db_quetzal_coffee'
    )
    
    usuario = User.query.get(current_user.id)
    
    if usuario.idVentaActual == 0 :
        print('El usuario no tiene una venta en curso')
        
        cursor = conexion.cursor()
        
        sql = 'SELECT idVenta FROM venta ORDER BY idVenta DESC LIMIT 1'
        
        cursor.execute(sql)
        row1 = cursor.fetchone()
        id = 0
        
        # No hay nada en la tabla venta
        if str(row1) == "None":
            #print('No hay nada en venta')
            id = 1
            
            v = Venta(id, current_user.id, current_user.id)
            
            sql2 = 'UPDATE user SET idVentaActual = {} where id = {}'.format(id, current_user.id)
            
            db.session.add(v)
            db.session.commit()
            
            p = Producto.query.get(idProducto)
            
            total = p.precioVenta * 1
            
            dv = DetalleVenta(current_user.idVentaActual, total, 1, idProducto)
            
            db.session.add(dv)
            db.session.commit()
            
            cursor.execute(sql2)
            conexion.commit()
            
            cursor.close()
            conexion.close()
        
        else:
            for item in row1:
                id = item
            id += 1
            
            p = Producto.query.get(idProducto)
            
            v = Venta(id, current_user.id, current_user.id)
            
            db.session.add(v)
            db.session.commit()
            
            total = p.precioVenta * 1
            
            dv = DetalleVenta(current_user.idVentaActual, total, 1, idProducto)
            
            db.session.add(dv)
            db.session.commit()

            cursor.close()
            conexion.close()
        return redirect(url_for('public.catalogo'))
    
    if current_user.idVentaActual != 0:
        
        print('Ya hay una venta')
        
        cursor = conexion.cursor()
        
        sql = 'select if (idProducto = {}, "Si", "No" ) from detalleventa where idVenta = {} and idProducto = {}'.format(idProducto, current_user.idVentaActual, idProducto)
        
        cursor.execute(sql)
        row = cursor.fetchone()
        
        respuesta = ''
        
        
        if str(row) == 'None':
            respuesta = 'No'
        else :
            for item in row:
                respuesta = item
        
        if respuesta == 'Si':
            p = Producto.query.get(idProducto)
            
            sql2 = 'select cantidad from detalleventa where idVenta = {} and idProducto = {}'.format(current_user.idVentaActual, idProducto)
            
            cantidad_producto = 0
            
            cursor.execute(sql2)
            row2 = cursor.fetchone()
            
            for item in row2:
                cantidad_producto = item
            
            cantidad_producto += 1
            new_total = cantidad_producto * p.precioVenta
            
            sql3 = 'update detalleventa set cantidad = {}, total = {} where idVenta = {} and idProducto = {}'.format(cantidad_producto, new_total, current_user.idVentaActual, idProducto)
            cursor.execute(sql3)
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('public.catalogo'))
        
        else:
            p = Producto.query.get(idProducto)
            
            total = p.precioVenta * 1
            
            dv = DetalleVenta(current_user.idVentaActual, total, 1, idProducto)
            
            db.session.add(dv)
            db.session.commit()
            return redirect(url_for('public.catalogo'))


@public.route('/carrito')
@login_required
@roles_required('cliente')
def carrito():
    
    conexion = mysql.connector.connect(
        host= 'localhost',
        port=3306,
        user= 'cliente',
        password= 'cliente123',
        db='db_quetzal_coffee'
    )
    
    sql = 'select sum(total) from detalleventa where idVenta = {}'.format(current_user.idVentaActual)
    
    cursor = conexion.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    
    if str(row) == 'None':
        cursor.close()
        conexion.close()
        return redirect(url_for('public.catalogo'))
    else :
        total = 0
        for item in row:
            total = item
        
        sql = 'update venta set totalVenta = {} where idVenta = {}'.format(total, current_user.idVentaActual)
        cursor.execute(sql)
        conexion.commit()
        
        lista_detalle = []
        
        sql2 = 'SELECT dv.idDetalleVenta, dv.idVenta, dv.total, dv.cantidad, dv.idProducto, p.Nombre, p.precioVenta FROM detalleventa as dv join producto as p on p.idProducto = dv.idProducto where idVenta = {}'.format(current_user.idVentaActual)
        cursor.execute(sql2)
        
        rows = cursor.fetchall()
        detalle = {}
        
        for row in rows:
            detalle['idDetalleVenta'] = row[0]
            detalle['idVenta'] = row[1]
            detalle['total'] = row[2]
            detalle['cantidad'] = row[3]
            detalle['idProducto'] = row[4]
            detalle['nombre'] = row[5]
            detalle['precioVenta'] = row[6]
            lista_detalle.append(detalle)
            detalle = {}
        
        v = Venta.query.get(current_user.idVentaActual)
        
        context = {
            'lista_detalle' : lista_detalle,
            'venta' : v
        }
        
        return render_template('CarritoCompraCliente.html', **context)

@public.route('/historial')
@login_required
@roles_required('cliente')
def historial():
    historial_venta_form = HistorialVenta()
    
    context = {
        'form' : historial_venta_form
    }
    return render_template('HistorialCompraCliente.html', **context)

@public.route('/pagoCompraCliente')
@login_required
@roles_required('cliente')
def pagoVenta():
    pago_compra = PagoVenta()
    
    context = {
        'form' : pago_compra
    }
    return render_template('PagoCompraCliente.html', **context)