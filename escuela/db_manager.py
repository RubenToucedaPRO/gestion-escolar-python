import mysql.connector
from .registrar import Registrar
from .common import IntegridadDatos


class DBManager:
    _conexion = None

    @classmethod
    def obtener_conexion(cls):
        if cls._conexion is None or not cls._conexion.is_connected():
            try:
                # Crear conexion
                cls._conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="admin",
                    database="db_escuela",
                )
            except Exception as e:
                mensaje = f"Error al crear la conexion a la BD: {e}"
                print(mensaje)
                raise IntegridadDatos(mensaje)
        return cls._conexion

    def leer_alumnos(self):
        con = self.obtener_conexion()
        if con:
            cursor = con.cursor(dictionary=True)
            query = """
            SELECT p.* 
            FROM alumnos as a 
            JOIN personas as p 
            ON a.id_persona=p.id_persona
            """
            cursor.execute(query)
            return cursor.fetchall()
        return []

    def leer_profesores(self):
        con = self.obtener_conexion()
        if con:
            cursor = con.cursor(dictionary=True)
            query = """
            SELECT p.*,pr.especialidad, pr.salario 
            FROM profesores as pr 
            JOIN personas as p 
            ON pr.id_persona=p.id_persona
            """
            cursor.execute(query)
            return cursor.fetchall()
        return []

    def obtener_usuario_dni(self, dni):
        con = self.obtener_conexion()
        if con:
            cursor = con.cursor(dictionary=True)
            query = """
            SELECT a.id_persona AS es_alumno, pr.id_persona AS es_profesor, p.*, pr.especialidad, pr.salario
            FROM personas as p 
            LEFT JOIN alumnos as a ON  p.id_persona=a.id_persona 
            LEFT JOIN profesores as pr ON p.id_persona=pr.id_persona 
            where p.dni=%s
            """
            cursor.execute(query, (dni,))
            return cursor.fetchone()
        return None

    def obtener_asignaturas_alumno(self, id):
        con = self.obtener_conexion()
        if con:
            cursor = con.cursor(dictionary=True)
            query = """
            SELECT a.*,m.nota
            FROM asignaturas as a 
            JOIN matriculas as m ON a.id_asignatura=m.id_asignatura 
            where m.id_alumno=%s
            """
            cursor.execute(query, (id,))
            return cursor.fetchall()
        return None
