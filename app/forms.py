from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, DateField, SelectField, DecimalField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms import FileField

class CarritoInsumos(FlaskForm):
    agua = StringField('Agua')  
    cafe = StringField('Café')   
    vasos = SelectField('Vasos',choices=[('1', 'Vaso 250ml'), ('2', 'Vaso 500ml')]) 
    tapas = SelectField('Tapas',choices=[('1', 'Tapa 250ml'), ('2', 'Tapa 500ml')]) 
    popotes = StringField('Popotes')
    azucar = StringField('Azucar')   
    leche = StringField('Leche')
    canela = StringField('Canela')
    cacao = StringField('Cacao')
    manzanilla = StringField('Manzanilla')
    hNaranja = StringField('Hoja de Naranja')
    cNaranja = StringField('Cascara de Naranja')
    menta = StringField('Menta')
    hLimon = StringField('Hoja de Limon')
    limon = StringField('Limon')
    naranjas = StringField('Naranjas')
    zanahorias = StringField('Zanahorias')
    pina = StringField('Piña')
    mango = StringField('Mango')
    guardar = SubmitField('Agregar')


class LoginForm(FlaskForm):
    
    correo = EmailField('Correo', validators=[InputRequired('Se necesita llenar este campo')])
    password = PasswordField('Contraseña', validators=[InputRequired('Se necesita llenar este campo')])
    iniciar = SubmitField('Iniciar sesión')
    
class RegistroClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired('Se necesita llenar este campo')])
    primerApellido = StringField('Primer apellido', validators=[InputRequired('Se necesita llenar este campo')])
    segundoApellido = StringField('Segundo apellido')
    calle = StringField('Calle', validators=[InputRequired('Se necesita llenar este campo')])
    numero = StringField('Número', validators=[InputRequired('Se necesita llenar este campo')])
    colonia = StringField('Colonia', validators=[InputRequired('Se necesita llenar este campo')])
    codigoPostal = StringField('Código Postal', validators=[InputRequired('Se necesita llenar este campo'), Length(min=5, max=5, message='Este campo requiere ser llenado con 5 caracteres')])
    
    telefono = StringField('Telefono', validators=[InputRequired('Se necesita llenar este campo'), Length(min=10, max=10, message='Este campo requiere ser llenado con 10 caracteres')])
    correo = EmailField('Correo', validators=[InputRequired('Se necesita llenar este campo')])
    password = PasswordField('Contraseña', validators=[InputRequired('Se necesita llenar este campo')])
    fechaNac = DateField('Fecha de nacimiento', validators=[InputRequired('Se necesita llenar este campo')])
    guardar = SubmitField('Registrarse')

class RegistroEmpleadoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired('Se necesita llenar este campo')])
    primerApellido = StringField('Primer apellido', validators=[InputRequired('Se necesita llenar este campo')])
    segundoApellido = StringField('Segundo apellido')
    calle = StringField('Calle', validators=[InputRequired('Se necesita llenar este campo')])
    numero = StringField('Número', validators=[InputRequired('Se necesita llenar este campo')])
    colonia = StringField('Colonia', validators=[InputRequired('Se necesita llenar este campo')])
    codigoPostal = StringField('Código Postal', validators=[InputRequired('Se necesita llenar este campo'), Length(min=5, max=5, message='Este campo requiere ser llenado con 5 caracteres')])
    
    sueldo = DecimalField('Sueldo', validators=[InputRequired('Se necesita llenar este campo')])
    hrsTrabajo = DecimalField('Horas de trabajo', validators=[InputRequired('Se necesita llenar este campo')])
    
    telefono = StringField('Telefono', validators=[InputRequired('Se necesita llenar este campo'), Length(min=10, max=10, message='Este campo requiere ser llenado con 10 caracteres')])
    correo = EmailField('Correo', validators=[InputRequired('Se necesita llenar este campo')])
    password = PasswordField('Contraseña', validators=[InputRequired('Se necesita llenar este campo')])
    fechaNac = DateField('Fecha de nacimiento', validators=[InputRequired('Se necesita llenar este campo')])
    
    tipoEmpleado = SelectField('Tipo de empleado', choices=[('2', 'Empleado'), ('3', 'Gerente')])
    
    guardar = SubmitField('Registrarse')

class RegistroProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired('Se necesita llenar este campo')])
    rfc = StringField('RFC', validators=[InputRequired('Se necesita llenar este campo')])
    razonSocial = StringField('Razón Social', validators=[InputRequired('Se necesita llenar este campo')])
    
    calle = StringField('Calle', validators=[InputRequired('Se necesita llenar este campo')])
    numero = StringField('Número', validators=[InputRequired('Se necesita llenar este campo')])
    colonia = StringField('Colonia', validators=[InputRequired('Se necesita llenar este campo')])
    codigoPostal = StringField('Código Postal' , validators=[InputRequired('Se necesita llenar este campo'), Length(min=5,max=5,message='Se requiere llenar el campo con 5 caracteres')])
    
    telefono = StringField('Telefono', validators=[InputRequired('Se necesita llenar este campo'), Length(min=10,max=10,message='Se requiere llenar el campo con 10 caracteres')])
    correo = EmailField('Correo', validators=[InputRequired('Se necesita llenar este campo')])
    
    guardar = SubmitField('Guardar')

class RegistroMateriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired('Se necesita llenar este campo')])
    descripcion = StringField('Descripcion', validators=[InputRequired('Se necesita llenar este campo')])
    cantidad = StringField('Cantidad', validators=[InputRequired('Se necesita llenar este campo')])
    unidadMedida = SelectField('Unidad de medida',choices=[('Kg', 'Kg'), ('Litro', 'Litro'),('Pza','Pza')]) 
    precioCompra = DecimalField('Precio de compra', validators=[InputRequired('Se necesita llenar este campo')])
    foto = FileField('Foto', validators=[InputRequired('Se necesita llenar este campo')])
    guardar = SubmitField('Guardar')

class RegistroProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired('Se necesita llenar este campo')])
    descripcion = StringField('Descripción', validators=[InputRequired('Se necesita llenar este campo')])   
    cantidad = DecimalField('Cantidad', validators=[InputRequired('Se necesita llenar este campo')])
    precioVenta = DecimalField('Precio', validators=[InputRequired('Se necesita llenar este campo')])
    tipoProducto = SelectField('Tipo producto', choices=[(1, 'Café'), (2, 'Jugo'),(3,'Té')])
    foto = FileField("Foto", validators=[InputRequired('Se necesita llenar este campo')])
    guardar = SubmitField('Guardar')
    
class RegistroRecetaForm(FlaskForm):
    producto = StringField('Producto')
    materiaPrima = StringField('Insumo')
    cantidad = DecimalField('Cantidad')
    guardar = SubmitField('Guardar')

class RegistroRolForm(FlaskForm):
    nombre = StringField('Nombre')
    descripcion = TextAreaField('Descripción')
    guardar = SubmitField('Guardar')

class CatalogoCliente(FlaskForm):
    cantidad = IntegerField('Cantidad', validators=[InputRequired('Se necesita llenar este campo'), NumberRange(min=1,message='Se requiere pedir por lo menos un producto para agregar al carrito')])
    agregar = SubmitField('Agregar')

class CarritoCompra(FlaskForm):
    cantidad = DecimalField('Cantidad')
    precio = DecimalField('Precio')
    subtotal = DecimalField('Subtotal')
    total = DecimalField('Total')
    comprar = SubmitField('Realizar compra')

class CarritoVenta(FlaskForm):
    cantidad = DecimalField('Cantidad')
    precio = DecimalField('Precio')
    subtotal = DecimalField('Subtotal')
    total = DecimalField('Total')
    comprar = SubmitField('Realizar compra')

class HistorialCompra(FlaskForm):
    nombre = StringField('Nombre')

class HistorialVenta(FlaskForm):
    nombre = StringField('Nombre')

class PagoCompra(FlaskForm):
    noTarjeta = StringField('Número de tarjeta')
    vencimiento = StringField('Vencimiento')
    cvv = StringField('CVV')
    total = DecimalField('Total')
    comprar = SubmitField('Pagar')

class PagoVenta(FlaskForm):
    noTarjeta = StringField('Número de tarjeta')
    vencimiento = StringField('Vencimiento')
    cvv = StringField('CVV')
    total = DecimalField('Total')
    comprar = SubmitField('Pagar')


