from flask import Flask, render_template, request, redirect, url_for, flash
from escuela.gestion import CentroEducativo

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = "clave_super_secreta_para_sesiones"
sistema = CentroEducativo()  # Tu orquestador de siempre


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/usuarios")
def listar_usuarios():
    # Usas tus métodos de siempre
    usuarios = sistema.get_usuarios()

    return render_template("usuarios.html", lista=usuarios)


@app.route("/alumno/nuevo_alumno")
def formulario_alumno():
    """Muestra el formulario vacío"""
    return render_template("nuevo_alumno.html")


@app.route("/alumno/guardar", methods=["POST"])
def guardar_nuevo_alumno():
    """Recibe los datos del formulario y los guarda en la BD"""
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    try:
        sistema.crear_alumno(dni, nombre, email)
        # flash(f"Alumno con dni {dni} creado")
        return redirect(url_for("listar_usuarios"))
    except Exception as e:
        return f"Error al guardar: {e}", 400


@app.route("/profesor/nuevo_profesor")
def formulario_profesor():
    """Muestra el formulario vacío"""
    return render_template("nuevo_profesor.html")


@app.route("/profesor/guardar", methods=["POST"])
def guardar_nuevo_profesor():
    """Recibe los datos del formulario y los guarda en la BD"""
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    especialidad = request.form.get("especialidad")
    salario = request.form.get("salario")

    try:
        sistema.crear_profesor(dni, nombre, email, especialidad, salario)
        return redirect(url_for("listar_usuarios"))
    except Exception as e:
        return f"Error al guardar: {e}", 400


@app.route("/usuario/<dni>")
def detalle_usuario(dni):
    # Usamos el método de tu clase CentroEducativo para buscar por DNI
    usuario = sistema.obtener_usuario(dni)

    if not usuario:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("listar_usuarios"))

    return render_template("detalle_usuario.html", usuario=usuario)


@app.route("/alumno/editar/<dni>")
def editar_alumno(dni):
    # Buscamos al usuario existente
    usuario = sistema.obtener_usuario(dni)
    if not usuario:
        flash("Alumno no encontrado", "danger")
        return redirect(url_for("listar_usuarios"))

    return render_template("editar_alumno.html", usuario=usuario)


@app.route("/alumno/actualizar", methods=["POST"])
def actualizar_alumno():
    id = request.form.get("id")
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    try:
        usuario = sistema.obtener_usuario_por_id(id)
        sistema.actualizar_persona(usuario, dni=dni, nombre=nombre, email=email)
        flash("Alumno actualizado con éxito", "success")
        return redirect(url_for("detalle_usuario", dni=dni))
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return render_template("detalle_usuario.html", usuario=usuario)


@app.route("/profesor/editar/<dni>")
def editar_profesor(dni):
    # Buscamos al usuario existente
    usuario = sistema.obtener_usuario(dni)
    if not usuario:
        flash("Profesor no encontrado", "danger")
        return redirect(url_for("listar_usuarios"))

    return render_template("editar_profesor.html", usuario=usuario)


@app.route("/profesor/actualizar", methods=["POST"])
def actualizar_profesor():
    id = request.form.get("id")
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    especialidad = request.form.get("especialidad")
    salario = request.form.get("salario")

    try:
        usuario = sistema.obtener_usuario_por_id(id)
        sistema.actualizar_persona(usuario, dni=dni, nombre=nombre, email=email)
        sistema.actualizar_profesor(usuario, especialidad=especialidad, salario=salario)
        flash("Profesor actualizado con éxito", "success")
        return redirect(url_for("detalle_usuario", dni=dni))
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return render_template("detalle_usuario.html", usuario=usuario)


if __name__ == "__main__":
    # Lanzamos el servidor en modo debug para ver errores en tiempo real
    app.run(debug=True, port=5000)
