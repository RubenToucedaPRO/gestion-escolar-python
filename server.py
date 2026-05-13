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


@app.route("/usuarios/nuevo_alumno")
def formulario_alumno():
    """Muestra el formulario vacío"""
    return render_template("nuevo_alumno.html")


@app.route("/usuarios/guardar", methods=["POST"])
def guardar_alumno():
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


@app.route("/usuarios/nuevo_profesor")
def formulario_profesor():
    """Muestra el formulario vacío"""
    return render_template("nuevo_profesor.html")


@app.route("/usuarios/guardar", methods=["POST"])
def guardar_profesor():
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


if __name__ == "__main__":
    # Lanzamos el servidor en modo debug para ver errores en tiempo real
    app.run(debug=True, port=5000)
