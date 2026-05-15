from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g,
)
from functools import wraps
from app.extensions import sistema

auth_bp = Blueprint("auth", __name__)


# Decorador para proteger vistas
def login_required(role=None):
    def decorator(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            if "dni" not in session:
                return redirect(url_for("auth.login"))

            user_role = session.get("role")
            # Convertimos a lista los role si no es lista
            roles_permitidos = [role] if isinstance(role, str) else role

            if user_role not in roles_permitidos:
                flash("No tienes permiso para acceder aquí.", "danger")
                return redirect(url_for("main.home"))

            return view(**kwargs)

        return wrapped_view

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        dni = request.form["dni"]
        contrasena = request.form["contrasena"]

        usuario = sistema.validar_login(dni, contrasena)

        if usuario:
            session.clear()
            session["nombre"] = usuario.get_nombre()
            session["dni"] = usuario.get_dni()
            session["role"] = usuario.get_rol()
            return redirect(url_for("main.home"))

        flash("DNI o contraseña incorrectos.", "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
