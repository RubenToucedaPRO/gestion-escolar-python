from flask import (
    session,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Blueprint,
)
from app.routes.auth import login_required
from app.extensions import sistema
from escuela import Registrar, ROL_ALUMNO

alumnos_bp = Blueprint("alumnos", __name__)


@alumnos_bp.route("/alumnos")
@login_required(role=["admin", "profesor"])
def listar():

    alumnos = sistema.get_alumnos()

    return render_template(
        "alumnos.html",
        alumnos=alumnos,
    )


@alumnos_bp.route("/crear")
@login_required(role="admin")
def formulario():
    """Muestra el formulario vacío"""
    return render_template("nuevo_alumno.html")


@alumnos_bp.route("/usuario/<dni>/<rol>")
@login_required(role=["admin", "profesor", "alumno"])
def detalle(dni, rol):
    if session.get("role") == "alumno" and session.get("dni") != dni:
        abort(403)
    usuario = sistema.obtener_usuario(dni, rol)

    if not usuario:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("alumnos.listar"))
    todas_las_asignaturas = sistema.obtener_todas_las_asignaturas()

    return render_template(
        "alumno_detalle.html",
        usuario=usuario,
        asignaturas_sistema=todas_las_asignaturas,
    )


@alumnos_bp.route("/usuario", methods=["POST"])
@login_required(role=["admin", "profesor"])
def buscar():
    dni = request.form.get("dni")

    try:
        usuario = sistema.obtener_usuario(dni, "alumno")
        if not usuario:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for("alumnos.listar"))
        todas_las_asignaturas = sistema.obtener_todas_las_asignaturas()
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Buscar usuario", f"{e}")
        return redirect(url_for("alumnos.listar"))

    Registrar.registrar_log(
        "Buscar usuario", f"Operación exitosa dni: {usuario.get_dni()!r}"
    )
    return render_template("alumno_detalle.html", usuario=usuario,asignaturas_sistema=todas_las_asignaturas)


@alumnos_bp.route("/crear", methods=["POST"])
@login_required(role="admin")
def crear():
    """Recibe los datos del formulario y los guarda en la BD"""
    dni = request.form.get("dni")
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    try:
        alumno = sistema.crear_alumno(dni, nombre, email)
        flash(f"Alumno con dni {dni} creado con éxito","success")
        Registrar.registrar_log(
            "Alta alumno", f"Operación exitosa dni: {alumno.get_dni()!r}"
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Alta alumno", f"{e}")
    return redirect(url_for("alumnos.listar"))


@alumnos_bp.route("/editar/<dni>")
@login_required(role="admin")
def editar(dni):
    usuario = sistema.obtener_usuario(dni, ROL_ALUMNO)
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
    return redirect(url_for("alumnos.detalle", dni=dni, rol=ROL_ALUMNO))


@alumnos_bp.route("/matricular", methods=["POST"])
@login_required(role=["admin", "alumno"])
def matricular():
    dni = request.form.get("dni")
    nombre_asig = request.form.get("nombre_asignatura")

    try:
        alumno = sistema.obtener_usuario(dni, ROL_ALUMNO)
        nombre_asig = sistema.matricular_alumno(alumno, nombre_asig)
        flash(f"Matriculado con éxito en {nombre_asig}", "success")
        Registrar.registrar_log(
            "Matricular alumno",
            f"Operación exitosa dni: {alumno.get_dni()!r}, asignatura:{nombre_asig!r}",
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Matricular alumno", f"{e}")
    return redirect(url_for("alumnos.detalle", dni=dni, rol=ROL_ALUMNO))


@alumnos_bp.route("/calificar", methods=["POST"])
@login_required(role=["admin", "profesor"])
def calificar():
    dni = request.form.get("dni")
    nota = float(request.form.get("nota"))
    nombre_asig = request.form.get("nombre_asignatura")

    try:
        alumno = sistema.obtener_usuario(dni, ROL_ALUMNO)
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
    return redirect(url_for("alumnos.detalle", dni=dni, rol=ROL_ALUMNO))


@alumnos_bp.route("/eliminar/<dni>", methods=["POST"])
@login_required(role="admin")
def eliminar(dni):

    dni = sistema.eliminar_usuario(dni)

    flash(f"Usuario con dni {dni!r} elimnado con éxito", "success")
    Registrar.registrar_log("Eliminar usuario", f"Operación exitosa dni: {dni!r}")
    return redirect(url_for("alumnos.listar"))


@alumnos_bp.route(
    "/eliminar_asignatura/<dni>/<id_alumno>/<id_asignatura>", methods=["POST"]
)
@login_required(role="admin")
def eliminar_asignatura(dni, id_alumno, id_asignatura):

    sistema.eliminar_asignatura_usuario(id_alumno, id_asignatura)

    flash(f"Asignatura elimnada con éxito", "success")
    Registrar.registrar_log("Eliminar asignatura usuario", f"Operación exitosa")
    return redirect(url_for("alumnos.detalle", dni=dni, rol=ROL_ALUMNO))
