from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.extensions import sistema

alumnos_bp = Blueprint("alumnos", __name__)


@alumnos_bp.route("/crear")
def formulario():
    """Muestra el formulario vacío"""
    return render_template("nuevo_alumno.html")


@alumnos_bp.route("/crear", methods=["POST"])
def crear():
    """Recibe los datos del formulario y los guarda en la BD"""
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    try:
        sistema.crear_alumno(dni, nombre, email)
        flash(f"Alumno con dni {dni} creado con éxito")
        return redirect(url_for("main.listar_usuarios"))
    except Exception as e:
        flash(f"Error al guardar: {e}", "danger")
        return redirect(url_for("main.listar_usuarios"))


@alumnos_bp.route("/editar/<dni>")
def editar(dni):
    # Buscamos al usuario existente
    usuario = sistema.obtener_usuario(dni)
    if not usuario:
        flash("Alumno no encontrado", "danger")
        return redirect(url_for("listar_usuarios"))

    return render_template("editar_alumno.html", usuario=usuario)


@alumnos_bp.route("/actualizar", methods=["POST"])
def actualizar():
    id = request.form.get("id")
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    try:
        usuario = sistema.obtener_usuario_por_id(id)
        sistema.actualizar_persona(usuario, dni=dni, nombre=nombre, email=email)
        flash("Alumno actualizado con éxito", "success")
        return redirect(url_for("main.detalle_usuario", dni=dni))
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return render_template("detalle_usuario.html", usuario=usuario)


@alumnos_bp.route("/matricular", methods=["POST"])
def matricular():
    dni = request.form.get("dni")
    nombre_asig = request.form.get("nombre_asignatura")

    # 1. Recuperamos el objeto alumno completo
    alumno = sistema.obtener_usuario(dni)

    if not alumno:
        flash("Error: Alumno no encontrado", "danger")
        return redirect(url_for("main.listar_usuarios"))

    try:
        sistema.matricular_alumno(alumno, nombre_asig)
        flash(f"Matriculado con éxito en {nombre_asig}", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")

    return redirect(url_for("main.detalle_usuario", dni=dni))
