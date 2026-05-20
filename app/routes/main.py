from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.routes.auth import login_required
from app.extensions import sistema
from escuela import Registrar

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/estadisticas")
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
        Registrar.registrar_log("Ejecutar SQL libre", f"{e}")
        return redirect(url_for("main.sql_libre"))

    Registrar.registrar_log("Eejcutar SQL libre", f"Operación exitosa: {query!r}")
    return render_template("sql_libre.html", lista=resultado, query=query)
