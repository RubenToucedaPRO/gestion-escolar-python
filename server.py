from flask import Flask
from app.routes import alumnos_bp, profesores_bp, main_bp

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = "clave_super_secreta_para_sesiones"

# Registras los Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(profesores_bp, url_prefix="/profesores")

if __name__ == "__main__":
    # Lanzamos el servidor en modo debug para ver errores en tiempo real
    app.run(debug=True, port=5000)
