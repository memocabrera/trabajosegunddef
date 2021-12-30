from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://xufocjsutnficn:eed110c81c39d231cb8200d7643f62f3881de75c918ca0ffe45b3572cbede900@ec2-52-70-205-234.compute-1.amazonaws.com:5432/d9smkia9q8gvat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))
    def __int__(self, email, password):
        self.email=email
        self.password=password


class Editorial(db.Model):
    __tablename__="editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))
    def __init__(self, nombre_editorial):
        self.nombre_editorial = nombre_editorial

class Autor(db.Model):
    __tablename__ = "autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor = db.Column(db.String(80))
    fecha_nac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(50))

    def __init__(self, nombre_autor, fecha_nac, nacionalidad):
        self.nombre_autor = nombre_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad = nacionalidad

class Genero(db.Model):
    __tablename__ = "genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre_genero = db.Column(db.String(80))

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero

class Libro(db.Model):
    __tablename__ = "libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(80))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))
    volumen = db.Column(db.Integer)
    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, volumen, id_editorial, id_autor, id_genero):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.volumen = volumen
        self.id_editorial = id_editorial
        self.id_autor = id_autor
        self.id_genero = id_genero


class Misfavoritos(db.Model):
    __tablename__ = "misfavoritos"
    id_favoritos = db.Column(db.Integer, primary_key=True)
    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    def __init__(self, id_libro, id_usuario):
        self.id_libro = id_libro
        self.id_usuario = id_usuario


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    consulta_usuario = Usuarios.query.filter_by(email=email).first()
    print(consulta_usuario.email)
    bcrypt.check_password_hash(consulta_usuario.password,password)
    return render_template("login.html")

@app.route("/registrar")
def registrar():
    return render_template("registro.html")

@app.route("/registrar_usuario", methods=['POST'])
def registrar_usuario():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)
    password_cifrado = bcrypt.generate_password_hash(password).decode('utf-8')
    print(password_cifrado)
    usuario = Usuarios(email = email, password=password_cifrado)
    db.session.add(usuario)
    db.session.commit()
    return "Resgistro usuario"

@app.route("/iniciar_sesion")
def iniciar_sesion():
    redirect("")

@app.route("/libro")
def libro():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("libro.html", consulta_editorial = consulta_editorial, consulta_genero = consulta_genero, consulta_autor = consulta_autor)

@app.route("/registrarLibro", methods=["POST"])
def registrarLibro():
    titulo_libro = request.form["titulo_libro"]
    fecha_publicacion = request.form["fecha_publicacion"]
    numero_paginas = request.form["numero_paginas"]
    formato = request.form["formato"]
    volumen = request.form["volumen"]
    id_editorial = request.form["editorial"]
    id_genero = request.form["genero"]
    id_autor = request.form["autor"]
    numero_paginas_int = int(numero_paginas)
    libro_nuevo = Libro(titulo_libro = titulo_libro, fecha_publicacion = fecha_publicacion,numero_paginas = numero_paginas_int,formato = formato,volumen=volumen, id_editorial = id_editorial, id_genero = id_genero, id_autor = id_autor)
    db.session.add(libro_nuevo)
    db.session.commit()
    return redirect("/libro")

@app.route("/autor")
def autor():
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("autor.html",consulta_autor = consulta_autor)

@app.route("/registrarautor", methods=["POST"])
def registrarautor():
    nombre_autor = request.form["nombre_autor"]
    fecha_nac = request.form["fecha_nac"]
    nacionalidad = request.form["nacionalidad"]
    autor_nuevo = Autor(nombre_autor = nombre_autor, fecha_nac = fecha_nac,nacionalidad = nacionalidad)
    db.session.add(autor_nuevo)
    db.session.commit()
    return redirect("/autor")

@app.route("/genero")
def genero():
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    return render_template("genero.html",consulta_genero = consulta_genero)

@app.route("/registrargenero", methods=["POST"])
def registreditorial():
    nombre_genero = request.form["nombre_genero"]
    genero_nuevo = Genero(nombre_genero = nombre_genero)
    db.session.add(genero_nuevo)
    db.session.commit()
    return redirect("/genero")

@app.route("/editorial")
def editorial():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    return render_template("editorial.html",consulta_editorial = consulta_editorial)

@app.route("/registrareditorial", methods=["POST"])
def registrgenero():
    nombre_editorial = request.form["nombre_editorial"]
    editorial_nuevo = Editorial(nombre_editorial = nombre_editorial)
    db.session.add(editorial_nuevo)
    db.session.commit()
    return redirect("/editorial")

@app.route("/leerlibro")
def leerlibro():
    conulta_libro= Libro.query.all()
    print(conulta_libro)
    for libros in conulta_libro:
        print(libros.titulo_libro)
        print(libros.fecha_publicacion)
        print(libros.numero_paginas)
        print(libros.formato)
        print(libros.volumen)
        print(libros.id_editorial)
        print(libros.id_genero)
        print(libros.id_autor)
    return render_template("LeerLibro.html", constlta = conulta_libro)

@app.route("/leerAutor")
def leerAutor():
    conulta_autor= Autor.query.all()
    print(conulta_autor)
    for autores in conulta_autor:
        print(autores.nombre_autor)
        print(autores.fecha_nac)
        print(autores.nacionalidad)
    return render_template("LeerAutor.html", constlta = conulta_autor)

@app.route("/leerGenero")
def leerGenero():
    conulta_genero= Genero.query.all()
    print(conulta_genero)
    for generos in conulta_genero:
        print(generos.nombre_genero)
    return render_template("LeerGenero.html", constlta = conulta_genero)

@app.route("/leerEditorial")
def leerEditorial():
    conulta_editorial= Editorial.query.all()
    print(conulta_editorial)
    for editoriales in conulta_editorial:
        print(editoriales.nombre_editorial)
    return render_template("LeerEditorial.html", constlta = conulta_editorial)

@app.route("/eliminarLibro/<id>")
def eliminar(id):
    libros = Libro.query.filter_by(id_libro=int(id)).delete()
    print(libros)
    db.session.commit()
    return render_template("LeerLibro.html")

@app.route("/eliminarautor/<id>")
def eliminarautor(id):
    autores = Autor.query.filter_by(id_autor=int(id)).delete()
    print(autores)
    db.session.commit()
    return render_template("LeerAutor.html")

@app.route("/eliminareditorial/<id>")
def eliminareditorial(id):
    editoriales = Editorial.query.filter_by(id_editorial=int(id)).delete()
    print(editoriales)
    db.session.commit()
    return render_template("LeerEditorial.html")

@app.route("/eliminargenero/<id>")
def eliminargenero(id):
    generos = Genero.query.filter_by(id_genero=int(id)).delete()
    print(generos)
    db.session.commit()
    return render_template("LeerGenero.html")

@app.route("/editarLibro/<id>")
def editarlibro(id):
    libros = Libro.query.filter_by(id_libro=int(id)).first()
    print(libros)
    print(libros.titulo_libro)
    print(libros.fecha_publicacion)
    print(libros.numero_paginas)
    print(libros.formato)
    print(libros.volumen)
    print(libros.id_editorial)
    print(libros.id_genero)
    print(libros.id_autor)
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    
    return render_template("modificarlibro.html", libros = libros, consulta_editorial = consulta_editorial, consulta_genero = consulta_genero, consulta_autor = consulta_autor)

@app.route("/modificarlibro/", methods=['POST'])
def modificarlibro():
    id_libro = request.form["id_libro"]
    nuevo_titulo_libro = request.form["titulo_libro"]
    nuevo_fecha_publicacion = request.form["fecha_publicacion"]
    nuevo_numero_paginas = request.form["numero_paginas"]
    nuevo_formato = request.form["formato"]
    nuevo_volumen = request.form["volumen"]
    nuevo_id_editorial = request.form["editorial"]
    nuevo_id_genero = request.form["genero"]
    nuevo_id_autor = request.form["autor"]

    libros = Libro.query.filter_by(id_libro=int(id_libro)).first()
    libros.titulo_libro= nuevo_titulo_libro
    libros.fecha_publicacion = nuevo_fecha_publicacion
    libros.numero_paginas= nuevo_numero_paginas
    libros.formato = nuevo_formato
    libros.volumen = nuevo_volumen
    libros.id_editorial = nuevo_id_editorial
    libros.nuevo_id_genero = nuevo_id_genero
    libros.id_autor = nuevo_id_autor
    db.session.commit()
    return render_template("LeerLibro.html")   


@app.route("/editarautor/<id>")
def editarautor(id):
    autores = Autor.query.filter_by(id_autor=int(id)).first()
    print(autores)
    print(autores.nombre_autor )
    print(autores.fecha_nac)
    print(autores.nacionalidad)
    return render_template("modificarautor.html", autores = autores)

@app.route("/modificarautor/", methods=['POST'])
def modificarautor():
    id_autor = request.form["id_autor"]
    nuevo_nombre_autor = request.form["nombre_autor"]
    nuevo_fecha_nac = request.form["fecha_nac"]
    nuevo_nacionalidad = request.form["nacionalidad"]

    autores = Autor.query.filter_by(id_autor=int(id_autor)).first()
    autores.nombre_autor = nuevo_nombre_autor 
    autores.fecha_nac = nuevo_fecha_nac
    autores.nacionalidad = nuevo_nacionalidad
    db.session.commit()
    return render_template("LeerAutor.html")   

@app.route("/editareditorial/<id>")
def editareditorial(id):
    editoriales = Editorial.query.filter_by(id_editorial=int(id)).first()
    print(editoriales)
    print(editoriales.nombre_editorial)
    return render_template("modificareditorial.html", editoriales = editoriales)

@app.route("/modificareditorial/", methods=['POST'])
def modificareditorial():
    id_editorial = request.form["id_editorial"]
    nuevo_nombre_editorial= request.form["nombre_editorial"]

    editoriales = Editorial.query.filter_by(id_editorial=int(id_editorial)).first()
    editoriales.nombre_editorial = nuevo_nombre_editorial
    db.session.commit()
    return render_template("LeerEditorial.html") 

@app.route("/editargenero/<id>")
def editargenero(id):
    generos = Genero.query.filter_by(id_genero=int(id)).first()
    print(generos)
    print(generos.nombre_genero)
    return render_template("modificargenero.html", generos = generos)

@app.route("/modificargenero/", methods=['POST'])
def modificargenero():
    id_genero = request.form["id_genero"]
    nuevo_nombre_genero = request.form["nombre_genero"]

    generos = Genero.query.filter_by(id_genero=int(id_genero)).first()
    generos.nombre_genero  = nuevo_nombre_genero 
    db.session.commit()
    return render_template("LeerGenero.html") 

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)