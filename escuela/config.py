import os
from dotenv import load_dotenv

load_dotenv()

# Configuración del Sistema de Usuarios
CONTRASENA_POR_DEFECTO = os.environ.get("CONTRASENA_POR_DEFECTO", "1234")
ROL_ALUMNO = "alumno"
ROL_PROFESOR = "profesor"
ROL_ADMIN = "admin"

# Configuración de la Base de Datos
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", 3306)
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "db_escuela")

# Clave secreta Flask firma cookies que el servidor envia al usuario
CLAVE_SECRETA = os.environ.get("CLAVE_SECRETA", "")
