from flask import jsonify
from flask import render_template
from flask import request

from app import app
from componentes.modelos import Tema
from componentes.modelos import Imagen
from componentes.modelos import Nivel
from componentes.modelos import Curso
from componentes.modelos import Docente
from componentes.modelos import Estudiante
from componentes.modelos import Cuenta


@app.route("/api-edtech/cursos", methods=['GET'])
def api_cursos():
    cursos = Curso.obtener()
    datos = [curso.__dict__ for curso in cursos]
    
    for dato in datos:
        t_id = dato['tema_id']
        dato["tema"] = Tema.obtener('id', t_id).__dict__["tema"]
        dato['docente'] = Docente.obtener('id', dato['docente_id']).__dict__
        
        del dato["tema_id"]
        del dato['docente_id']
    
    return jsonify(datos)

@app.route("/api-edtech/temas", methods=['GET'])
def api_temas():
    temas = Tema.obtener()
    datos = [tema.__dict__ for tema in temas]
    
    for dato in datos:
        dato["nivel"] = Nivel.obtener('id', dato["nivel_id"]).__dict__["nivel"]
        imagenes = Imagen.obtener('tema_id', dato["id"])
        dato["imagenes"] = []

        if type(imagenes) == list:
            for img in imagenes:
                i = img.__dict__
                dato["imagenes"].append(i)
        else:
            dato["imagenes"].append(imagenes.__dict__)
            
        del dato["nivel_id"]
    
    return jsonify(datos)

@app.route("/api-edtech/docentes", methods=['GET'])
def api_docentes():
    docentes = Docente.obtener()
    datos = [docente.__dict__ for docente in docentes]
    return jsonify(datos)

@app.route("/api-edtech/curso/<id>/detalle", methods=['GET'])
def api_detalle_curso(id):
    curso = Curso.obtener('id', id)
    return jsonify(curso.__dict__)

@app.route("/api-edtech/perfil", methods=['POST'])
def crear_estudiante():
    
    if request.method == 'POST':
        datos = request.json["datos"]
        cuenta = Cuenta.obtener('correo', datos['correo'])
        perfil = Estudiante.obtener('id_cuenta', cuenta.id)
    
        if not perfil:
            estud_nuevo = Estudiante(
                cuenta.id,
                datos['nombre'],
                datos['apellido'],
                datos['doc_identidad'],
                datos['educacion']
            )
            estud_nuevo = estud_nuevo.guardar_db()
            respuesta = {'mensaje': estud_nuevo}
        else:
            del datos['lenguajes']
            del datos['correo']
            datos['id'] = cuenta.id
            estud_modif = Estudiante.modificar(datos)
            respuesta = {'mensaje': estud_modif}
    else:
        respuesta = {'mensaje': 'no se recibieron datos.'}

    return jsonify(respuesta)

@app.route("/api-edtech/cuenta", methods=['POST'])
def crear_cuenta():
    
    if request.method == 'POST':
        datos = request.json["datos"]
        cta_nueva = Cuenta(
            datos['correo'],
            datos['contrasenia'],
        )
        
        respuesta = {}
        
        try:
            cta_nueva.guardar_db()
            respuesta['mensaje'] = 'Cuenta creada con éxito!'
            respuesta['status'] = 200
        except Exception as e:
            respuesta['mensaje'] = 'No se puedo crear la cuenta!'
            respuesta['status'] = 409
            
    else:
        respuesta['mensaje'] = 'No se recibieron datos.'
        respuesta['status'] = 204    

    return jsonify(respuesta)

@app.route('/api-edtech/validar', methods=['POST'])
def validar_cuenta():
    respuesta = {}    
    
    if request.method == 'POST':
        datos = request.json["datos"]
        ingreso = Cuenta(datos['correo'], datos['contrasenia'])
        cuenta = Cuenta.obtener('correo', datos['correo'])
        
        
        if cuenta and ingreso.clave == cuenta.clave:
            estudiante = Estudiante.obtener('id_cuenta', cuenta.id)

            if not estudiante:
                respuesta['perfil'] = 0
            else:
                respuesta['perfil'] = 1
            
            respuesta['mensaje'] = 'Ingreso exitoso!'
            respuesta['status'] = 200
        else:
            respuesta['mensaje'] = 'Verifique los datos enviados.'
            respuesta['status'] = 409
    
    return jsonify(respuesta)

@app.route('/api-edtech/obt-perfil', methods=['POST'])
def obtener_perfil():
    
    if request.method == 'POST':
        correo = request.json['datos']
        cuenta = Cuenta.obtener('correo', correo)
        perfil = Estudiante.obtener('id_cuenta', cuenta.id)
        perfil = perfil.__dict__
        perfil['correo'] = cuenta.correo
        del perfil['id']
        del perfil['id_cuenta']
    
    return jsonify(perfil)    

@app.route('/api-edtech/eliminar', methods=['DELETE'])
def eliminar_cta_perfil():
    
    if request.method == 'DELETE':
        datos = request.json["datos"]
        cuenta = Cuenta.obtener('correo', datos)
        
        eliminar_perfil = Estudiante.eliminar(cuenta.id)
        eliminar_cuenta = Cuenta.eliminar(cuenta.id)
        
        if eliminar_cuenta == eliminar_perfil:
            respuesta = {'mensaje': eliminar_perfil}
        else:
            respuesta = {'mensaje': 'Algo salió mal!'}
    
    else:
        respuesta = {'mensaje': 'no se recibieron datos.'}
        
    return jsonify(respuesta)