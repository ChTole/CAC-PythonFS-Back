from base_db.conexion_db import conexion
from base_db.tabla_db import Tabla
from auxiliares.cifrado import encriptar

        
class Curso(Tabla):
    
    tabla = 'curso'
    conexion = conexion
    campos = ('id', 'tema_id', 'fecha_inicio', 'fecha_cierre', 'docente_id', 'cupo')
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
class Docente(Tabla):
    
    tabla = 'docente'
    conexion = conexion
    campos = ('id', 'nombre', 'apellido', 'cuit')
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
class Tema(Tabla):
    
    tabla = 'tema'
    conexion = conexion
    campos = ('id', 'tema', 'nivel_id', 'descripcion')
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
class Nivel(Tabla):
    
    tabla = 'nivel'
    conexion = conexion
    campos = ('id', 'nivel')
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)

class Imagen(Tabla):
    
    tabla = 'imagen'
    conexion = conexion
    campos = ('id', 'tema_id', 'url_img', 'texto_alt')
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
class Estudiante(Tabla):
    
    tabla = 'estudiante'
    conexion = conexion
    campos = ('id', 'id_cuenta','nombre', 'apellido', 'doc_identidad', 'educacion')
    
    def __init__(self, *args, de_bbdd=False):
        super().crear(args, de_bbdd)
        
class Cuenta(Tabla):
    
    tabla = 'cuenta'
    conexion = conexion
    campos = ('id', 'correo', 'clave')
    
    def __init__(self, *args, de_bbdd=False):
        
        if not de_bbdd:
            cuenta = []
            cuenta.append(args[0])
            cuenta.append(encriptar(args[1]))
            super().crear(tuple(cuenta), de_bbdd)
        else:
            super().crear(args, de_bbdd)