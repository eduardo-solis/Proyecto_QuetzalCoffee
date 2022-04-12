from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security.utils import login_user, logout_user

from flask import current_app
import datetime

from . import auth
from ..forms import LoginForm, RegistroClienteForm
from ..models import db, userDataStore
from ..models import User, users_roles

import mysql.connector



@auth.route('/login', methods=['GET', 'POST'])
def login_get():
    
    login_form = LoginForm()
    
    context = {
        'form' : login_form
    }
    
    if login_form.validate_on_submit():
        
        email = login_form.correo.data
        password = login_form.password.data
        # Se consulta si existe un usuario ya registrado con el correo
        user = User.query.filter_by(email=email).first()
        date = datetime.datetime.now()
        
        # Se verifica si el usuario existe
        # Se toma el password proporcionado por el usuario, lo hasheamos
        # y lo comparamos con el password en la base de datos
        if not user or not check_password_hash(user.password, password):
            flash('El usuario y/o contraseña son incorrectos')
            
            mensaje = '''
            Se intento acceder a la aplicación con el 
            correo: {} y contraseña: {}
            el dia {} a las {}
            '''.format(email,password,date.date(), date.strftime('%X'))
            
            current_app.logger.warning(mensaje)
            
            # Si el usuario no existe o el password no coincide
            return redirect(url_for('auth.login_get'))
        
        # En caso contrario, si existe un usuario y la contraseña esta correcta
        # Entonces creamos la sesion y logeamos al usuario
        login_user(user)
        
        mensaje = '''
        Se ingreso a la aplicacion el usuario con id: {} ,
        el dia {} a las {}
        '''.format(user.id,date.date(), date.strftime('%X'))
        current_app.logger.info(mensaje)
        
        return redirect(url_for('public.principal'))
    
    return render_template('Login.html', **context)


@auth.route('/register', methods=['GET', 'POST'])
def register_get():
    
    date = datetime.datetime.now()
    
    register_form = RegistroClienteForm()
    
    context = {
        'form' : register_form
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
            
            return redirect(url_for('auth.register_get'))
        
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
        
        return redirect(url_for('auth.login_get'))
    
    return render_template('Registro.html', **context)


@auth.route('logout')
@login_required
def logout():
    id = current_user.id
    # Cerrar la sesión
    logout_user()
    date = datetime.datetime.now()
    mensaje = '''
    El usuario con id {} salio de la aplicacion
    el dia {} a las {}
    '''.format(id,date.date(), date.strftime('%X'))
    current_app.logger.info(mensaje)
    return redirect(url_for('public.principal'))
