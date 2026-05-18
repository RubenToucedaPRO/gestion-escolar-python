from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.routes.auth import login_required
from app.extensions import sistema
from escuela import Registrar

asignaturas_bp = Blueprint("asignaturas", __name__)


@asignaturas_bp.route("/asignaturas")
@login_required(role="admin")
def listar_asignaturas():

    asignaturas = sistema.obtener_todas_las_asignaturas()

    return render_template("asignaturas.html", asignaturas=asignaturas)


@asignaturas_bp.route("/crear", methods=["POST"])
@login_required(role="admin")
def crear():
    """Recibe los datos del formulario y los guarda en la BD"""
    nombre = request.form.get("nombre")

    try:
        asignatura = sistema.crear_asignatura(nombre)
        flash(f"Asignatura {asignatura} creada con éxito")
        Registrar.registrar_log(
            "Alta asignatura", f"Operación exitosa asignatura: {asignatura!r}"
        )
    except Exception as e:
        flash(f"{e}", "danger")
        Registrar.registrar_log("Alta asignatura", f"{e}")
    return redirect(url_for("asignaturas.listar_asignaturas"))


@asignaturas_bp.route("/eliminar_asignatura/<nombre>", methods=["POST"])
@login_required(role="admin")
def eliminar_asignatura(nombre):

    sistema.eliminar_asignatura(nombre)

    flash(f"Asignatura {nombre!r} elimnada con éxito", "success")
    Registrar.registrar_log(
        "Eliminar asignatura", f"Operación exitosa asignatura: {nombre!r}"
    )
    return redirect(url_for("asignaturas.listar_asignaturas"))
