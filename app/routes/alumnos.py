from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.routes.auth import login_required
from app.extensions import sistema
from escuela import Registrar, ROL_ALUMNO

alumnos_bp = Blueprint("alumnos", __name__)


@alumnos_bp.route("/crear")
@login_required(role="admin")
def formulario():
    """Muestra el formulario vacío"""
    return render_template("nuevo_alumno.html")


@alumnos_bp.route("/crear", methods=["POST"])
@login_required(role="admin")
def crear():
    """Recibe los datos del formulario y los guarda en la BD"""
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    try:
        alumno = sistema.crear_alumno(dni, nombre, email)
        flash(f"Alumno con dni {dni} creado con éxito")
        Registrar.registrar_log(
            "Alta alumno", f"Operación exitosa dni: {alumno.get_dni()!r}"
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Alta alumno", f"{e}")
    return redirect(url_for("main.listar_usuarios"))


@alumnos_bp.route("/editar/<dni>")
@login_required(role="admin")
def editar(dni):

    usuario = sistema.obtener_usuario(dni)
    return render_template("editar_alumno.html", usuario=usuario)


@alumnos_bp.route("/actualizar", methods=["POST"])
@login_required(role="admin")
def actualizar():
    id = request.form.get("id")
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    try:
        usuario = sistema.obtener_usuario_por_id(id, ROL_ALUMNO)
        sistema.actualizar_persona(usuario, dni=dni, nombre=nombre, email=email)
        flash("Alumno actualizado con éxito", "success")
        Registrar.registrar_log(
            "Actualizar alumno", f"Operación exitosa dni: {usuario.get_dni()!r}"
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Actualizar alumno", f"{e}")
    return redirect(url_for("main.detalle_usuario", dni=dni))


@alumnos_bp.route("/matricular", methods=["POST"])
@login_required(role=["admin", "alumno"])
def matricular():
    dni = request.form.get("dni")
    nombre_asig = request.form.get("nombre_asignatura")

    try:
        alumno = sistema.obtener_usuario(dni)
        nombre_asig = sistema.matricular_alumno(alumno, nombre_asig)
        flash(f"Matriculado con éxito en {nombre_asig}", "success")
        Registrar.registrar_log(
            "Matricular alumno",
            f"Operación exitosa dni: {alumno.get_dni()!r}, asignatura:{nombre_asig!r}",
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Matricular alumno", f"{e}")
    return redirect(url_for("main.detalle_usuario", dni=dni))


@alumnos_bp.route("/calificar", methods=["POST"])
@login_required(role=["admin", "profesor"])
def calificar():
    dni = request.form.get("dni")
    nota = float(request.form.get("nota"))
    nombre_asig = request.form.get("nombre_asignatura")

    try:
        alumno = sistema.obtener_usuario(dni)
        asignatura = sistema.calificar_alumno(alumno, nombre_asig, nota)
        flash(
            f"Calficado con éxito en {asignatura.get_nombre()!r} - nota: {str(asignatura.get_nota())!r} - nota: {str(asignatura.get_nota())!r}",
            "success",
        )
        Registrar.registrar_log(
            "Calificar alumno",
            f"Operación exitosa dni: {alumno.get_dni()!r}, asignatura: {asignatura.get_nombre()!r} - nota: {str(asignatura.get_nota())!r}",
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Calificar alumno", f"{e}")
    return redirect(url_for("main.detalle_usuario", dni=dni))
