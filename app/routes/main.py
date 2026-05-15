from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.routes.auth import login_required
from app.extensions import sistema

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/usuarios")
@login_required(role="admin")
def listar_usuarios():

    usuarios = sistema.get_usuarios()

    return render_template("usuarios.html", lista=usuarios)


@main_bp.route("/usuario/<dni>")
@login_required(role="admin")
def detalle_usuario(dni):

    usuario = sistema.obtener_usuario(dni)

    if not usuario:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("main.listar_usuarios"))
    todas_las_asignaturas = sistema.obtener_todas_las_asignaturas()

    return render_template(
        "detalle_usuario.html",
        usuario=usuario,
        asignaturas_sistema=todas_las_asignaturas,
    )


@main_bp.route("/usuario", methods=["POST"])
@login_required(role="admin")
def buscar_usuario():
    dni = request.form.get("dni")

    try:
        usuario = sistema.obtener_usuario(dni)
        if not usuario:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for("main.listar_usuarios"))
    except Exception as e:
        flash(f"{e}", "danger")
        return redirect(url_for("main.listar_usuarios"))

    return render_template("detalle_usuario.html", usuario=usuario)


@main_bp.route("/eliminar_usuario/<dni>", methods=["POST"])
@login_required(role="admin")
def eliminar_usuario(dni):

    sistema.eliminar_usuario(dni)

    flash(f"Usuario con dni {dni!r} elimnado con éxito", "success")
    return redirect(url_for("main.listar_usuarios"))


@main_bp.route("/estadisticas")
@login_required(role=["admin", "profesor", "alumno"])
def listar_estadisticas():

    estadisticas = sistema.obtener_estadisticas()

    return render_template("estadisticas.html", lista=estadisticas)


@main_bp.route("/sql")
@login_required(role="admin")
def sql_libre():
    lista = []
    return render_template("sql_libre.html", lista=lista)


@main_bp.route("/sql", methods=["POST"])
@login_required(role="admin")
def ejecutar_sql_libre():
    query = request.form.get("query")

    try:
        resultado = sistema.ejecutar_sql_libre(query)

    except Exception as e:
        flash(f"{e}", "danger")
        return redirect(url_for("main.sql_libre"))

    return render_template("sql_libre.html", lista=resultado)
