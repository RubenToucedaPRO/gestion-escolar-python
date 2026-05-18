from flask import Flask, flash, redirect, url_for
from werkzeug.exceptions import HTTPException
from app.routes import alumnos_bp, profesores_bp, main_bp, auth_bp
import os
from escuela import Registrar

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "app", "templates"),
    static_folder=os.path.join(base_dir, "app", "static"),
)
app.secret_key = "clave_super_secreta_para_sesiones"

# Registras los Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(profesores_bp, url_prefix="/profesores")
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.errorhandler(Exception)
def manejador_global_errores(error):
    Registrar.registrar_log("Error no controlado", error)

    flash(f"{error}", "danger")

    return redirect(url_for("main.home"))


if __name__ == "__main__":
    # Lanzamos el servidor en modo debug para ver errores en tiempo real
    app.run(debug=True, port=5000)
