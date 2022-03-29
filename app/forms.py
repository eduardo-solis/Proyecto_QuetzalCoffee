from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, DateField, SelectField

class LoginForm(FlaskForm):
    
    correo = EmailField('Correo')
    password = PasswordField('Contraseña')
    iniciar = SubmitField('Iniciar sesión')
    
class RegistroClienteForm(FlaskForm):
    nombre = StringField('Nombre')
    primerApellido = StringField('Primer apellido')
    segundoApellido = StringField('Segundo apellido')
    calle = StringField('Calle')
    numero = StringField('Número')
    colonia = StringField('Colonia')
    codigoPostal = StringField('CP')
    ciudad = SelectField('Ciudad', choices=[('1','León')])
    estado = SelectField('Estado', choices=[('1','Guanajuato')])
    
    telefono = StringField('Telefono')
    correo = EmailField('Correo')
    password = PasswordField('Contraseña')
    fechaNac = DateField('Fecha de nacimiento')
    guardar = SubmitField('Guardar')

class RegistroEmpleadoForm(FlaskForm):
    nombre = StringField()

class RegistroProveedorForm(FlaskForm):
    nombre = StringField()

class RegistroMateriaForm():
    nombre = StringField()

class RegistroProductoForm():
    nombre = StringField()