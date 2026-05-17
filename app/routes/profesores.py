from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.routes.auth import login_required
from app.extensions import sistema
from escuela import Registrar

profesores_bp = Blueprint("profesores", __name__)


@profesores_bp.route("/crear")
@login_required(role="admin")
def formulario():
    """Muestra el formulario vacío"""
    asignaturas = sistema.obtener_todas_las_asignaturas()
    return render_template("nuevo_profesor.html", asignaturas_sistema=asignaturas)


@profesores_bp.route("/crear", methods=["POST"])
@login_required(role="admin")
def crear():
    """Recibe los datos del formulario y los guarda en la BD"""
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    especialidad = request.form.get("especialidad")
    salario = request.form.get("salario")

    try:
        sistema.crear_profesor(dni, nombre, email, especialidad, salario)
        flash(f"Profesor con dni {dni} creado con éxito")
        Registrar.registrar_log("Alta profesor", f"Operación exitosa dni: {dni!r}")
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Alta profesor", f"{e}")
    return redirect(url_for("main.listar_usuarios"))


@profesores_bp.route("/editar/<dni>")
@login_required(role="admin")
def editar(dni):

    usuario = sistema.obtener_usuario(dni)
    asignaturas = sistema.obtener_todas_las_asignaturas()
    return render_template(
        "editar_profesor.html", usuario=usuario, asignaturas_sistema=asignaturas
    )


@profesores_bp.route("/actualizar", methods=["POST"])
@login_required(role="admin")
def actualizar():
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
        Registrar.registrar_log(
            "Actualizar profesor", f"Operación exitosa dni: {usuario.get_dni()!r}"
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Actualizar profesor", f"{e}")
    return redirect(url_for("main.detalle_usuario", dni=dni))
