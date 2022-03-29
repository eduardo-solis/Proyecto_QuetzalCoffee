from . import public

@public.route('/')
def inicio():
    return '<h1>Inicio</h1>'
    # Editado desde la web