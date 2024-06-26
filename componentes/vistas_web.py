from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from app import app
from componentes.modelos import Curso
from componentes.modelos import Docente
from componentes.modelos import Tema
from componentes.modelos import Cuenta
from componentes.modelos import Estudiante



# ****** Inicio ******
@app.route('/')
def inicio():
    return render_template('inicio.html')

# ****** Modelos ******
@app.route('/cursos')
@app.route('/cursos/<mensaje>')
def cursos(mensaje=None):
    cursos = Curso.obtener()
    
    for curso in cursos:
        curso.tema_id = Tema.obtener('id', curso.tema_id).tema
        docente = Docente.obtener('id', curso.docente_id)
        d_nom = docente.nombre
        d_ape = docente.apellido
        curso.docente = f"{d_nom} {d_ape}"
    
    return render_template('./modelos/cursos.html', cursos=cursos, mensaje=mensaje)

@app.route('/docentes')
@app.route('/docentes/<mensaje>')
def docentes(mensaje=None):
    docentes = Docente.obtener()
    return render_template('./modelos/docentes.html', docentes=docentes, mensaje=mensaje)

@app.route('/estudiantes')
@app.route('/estudiantes/<mensaje>')
def estudiantes(mensaje=None):
    estudiantes = Estudiante.obtener()
    estudiantes = [estudiantes] if type(estudiantes) != list else estudiantes
    
    for estudiante in estudiantes:
        estudiante.correo = Cuenta.obtener('id', estudiante.id_cuenta).correo
        
    return render_template('./modelos/estudiantes.html', estudiantes=estudiantes, mensaje=mensaje)

# ****** Detalle de registros y CRUD ******
tablas = {
    "docente": Docente,
    "estudiante": Estudiante,
    "curso": Curso
}

@app.route('/<id>/<tipo>/detalle')
def ver_detalle(id, tipo):
    return render_template("./modelos/crud/detalle.html", 
                           datos=tablas[tipo].obtener('id', id), 
                           tipo=tipo)

@app.route('/<id>/<tipo>/eliminar')
def eliminar(id, tipo):
    respuesta = tablas[tipo].eliminar(id)
    return redirect(url_for(tipo + "s", mensaje=respuesta))

@app.route('/<id>/<tipo>/modificar', methods=['POST'])
def modificar(id, tipo):
    
    if request.method == 'POST':
        datos = dict(request.form)
        datos['id'] = id
        respuesta = tablas[tipo].modificar(datos)
        
    return redirect(url_for(tipo + "s", mensaje=respuesta))

@app.route('/<tipo>/crear', methods=['GET', 'POST'])
def crear(tipo):
    
    if request.method == 'POST':
        datos = dict(request.form).values()
        nvo_registro = tablas[tipo](*list(datos))
        respuesta = nvo_registro.guardar_db()
        return redirect(url_for(tipo + "s", mensaje=respuesta))        
    
    modelo = tablas[tipo].campos[1:]  
    return render_template('./modelos/crud/crear.html', tipo=tipo, modelo=modelo)
    

# ****** API EdTech ******
@app.route('/api-edtech')
def api_docu():
    return render_template('./api-edtech/docu.html')