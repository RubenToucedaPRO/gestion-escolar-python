import unittest
import sys
import os

# Inyecta de forma automática la raíz del proyecto (gestion-escolar-python) en el buscador de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from server import app


class TestAuthBlueprint(unittest.TestCase):
    def setUp(self):
        # Configuramos la app en modo testing
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  # Desactiva CSRF para facilitar el test
        self.client = app.test_client()

    def test_login_page_loads(self):
        # Simula una petición GET a la ruta de login
        respuesta = self.client.get("/login", follow_redirects=True)
        # Verifica que la página carga con éxito (Código 200)
        self.assertEqual(respuesta.status_code, 200)

    def test_login_exitoso_redirige(self):
        # Simula el envío del formulario de login por POST
        respuesta = self.client.post(
            "/login",
            data={"dni": "16083440T", "contrasena": "admin"},
            follow_redirects=True,
        )

        # Verifica que tras loguearse con éxito te lleve al panel (index)
        self.assertEqual(respuesta.status_code, 200)
        # Verifica si un texto específico sale en el dashboard
        self.assertIn(b"Bienvenido a CentroEdu", respuesta.data)
