from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.routes.auth import login_required
from app.extensions import sistema
from escuela import Registrar, ROL_PROFESOR

profesores_bp = Blueprint("profesores", __name__)


@profesores_bp.route("/profesores")
@login_required(role="admin")
def listar():

    profesores = sistema.get_profesores()

    return render_template(
        "profesores.html",
        profesores=profesores,
    )


@profesores_bp.route("/crear")
@login_required(role="admin")
def formulario():
    """Muestra el formulario vacío"""
    asignaturas = sistema.obtener_todas_las_asignaturas()
    return render_template("nuevo_profesor.html", asignaturas_sistema=asignaturas)


@profesores_bp.route("/usuario/<dni>/<rol>")
@login_required(role="admin")
def detalle(dni, rol):
    usuario = sistema.obtener_usuario(dni, rol)

    if not usuario:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("profesores.listar"))
    todas_las_asignaturas = sistema.obtener_todas_las_asignaturas()

    return render_template(
        "profesor_detalle.html",
        usuario=usuario,
        asignaturas_sistema=todas_las_asignaturas,
    )


@profesores_bp.route("/usuario", methods=["POST"])
@login_required(role="admin")
def buscar():
    dni = request.form.get("dni")

    try:
        usuario = sistema.obtener_usuario(dni, "profesor")
        if not usuario:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for("profesores.listar"))
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Buscar usuario", f"{e}")
        return redirect(url_for("profesores.listar"))

    Registrar.registrar_log(
        "Buscar usuario", f"Operación exitosa dni: {usuario.get_dni()!r}"
    )
    return render_template("profesor_detalle.html", usuario=usuario)


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
        flash(f"Profesor con dni {dni} creado con éxito", "success")
        Registrar.registrar_log("Alta profesor", f"Operación exitosa dni: {dni!r}")
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Alta profesor", f"{e}")
    return redirect(url_for("profesores.listar"))


@profesores_bp.route("/editar/<dni>")
@login_required(role="admin")
def editar(dni):

    usuario = sistema.obtener_usuario(dni, ROL_PROFESOR)
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
        usuario = sistema.obtener_usuario_por_id(id, ROL_PROFESOR)
        sistema.actualizar_persona(usuario, dni=dni, nombre=nombre, email=email)
        sistema.actualizar_profesor(usuario, especialidad=especialidad, salario=salario)
        flash("Profesor actualizado con éxito", "success")
        Registrar.registrar_log(
            "Actualizar profesor", f"Operación exitosa dni: {usuario.get_dni()!r}"
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Actualizar profesor", f"{e}")
    return redirect(url_for("profesores.detalle", dni=dni, rol=ROL_PROFESOR))


@profesores_bp.route("/eliminar/<dni>", methods=["POST"])
@login_required(role="admin")
def eliminar(dni):

    dni = sistema.eliminar_usuario(dni)

    flash(f"Usuario con dni {dni!r} elimnado con éxito", "success")
    Registrar.registrar_log("Eliminar usuario", f"Operación exitosa dni: {dni!r}")
    return redirect(url_for("profesores.listar"))
