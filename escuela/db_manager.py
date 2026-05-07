import mysql.connector
from .common import IntegridadDatos


class DBManager:
    _conexion = None

    @classmethod
    def __obtener_conexion(cls):
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
                mensaje = f"Error al crear la conexion a la BD-> {e}"
                raise IntegridadDatos(mensaje)
        return cls._conexion

    def leer_alumnos(self):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor(dictionary=True)
            query = """
            SELECT p.* 
            FROM alumnos as a 
            JOIN personas as p 
            ON a.id_persona=p.id_persona
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            raise IntegridadDatos(f"Error al solicitar alumnos en BD: {e}")
        finally:
            if cursor:
                cursor.close()

    def leer_profesores(self):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor(dictionary=True)
            query = """
            SELECT p.*,pr.especialidad, pr.salario 
            FROM profesores as pr 
            JOIN personas as p 
            ON pr.id_persona=p.id_persona
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            raise IntegridadDatos(f"Error al solicitar profesores en BD: {e}")
        finally:
            if cursor:
                cursor.close()

    def obtener_usuario_dni(self, dni):
        con = self.__obtener_conexion()
        try:
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
        except Exception as e:
            raise IntegridadDatos(f"Error al consultar usuario por DNI en BD: {e}")
        finally:
            if cursor:
                cursor.close()

    def obtener_asignaturas_alumno(self, id):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor(dictionary=True)
            query = """
            SELECT a.*,m.nota
            FROM asignaturas as a 
            JOIN matriculas as m ON a.id_asignatura=m.id_asignatura 
            where m.id_alumno=%s
            """
            cursor.execute(query, (id,))
            return cursor.fetchall()
        except Exception as e:
            raise IntegridadDatos(f"Error al consultar asignaturas en BD: {e}")
        finally:
            if cursor:
                cursor.close()

    def crear_alumno(self, dni, nombre, email):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor()
            nuevo_id = self.__crear_persona(self, cursor, dni, nombre, email)
            query = "INSERT INTO alumnos (id_persona) VALUES (%s)"
            cursor.execute(query, (nuevo_id,))
            con.commit()
        except Exception as e:
            con.rollback()
            raise IntegridadDatos(f"Error al crear alumno en BD->{e}")
        finally:
            if cursor:
                cursor.close()

    def crear_profesor(self, dni, nombre, email, especialidad, salario):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor()
            nuevo_id = self.__crear_persona(self, cursor, dni, nombre, email)
            query = "INSERT INTO profesores (id_persona,especialidad,salario) VALUES (%s,%s,%s)"
            cursor.execute(query, (nuevo_id, especialidad, salario))
            con.commit()
        except Exception as e:
            con.rollback()
            raise IntegridadDatos(f"Error al crear profesor en BD->{e}")
        finally:
            if cursor:
                cursor.close()

    def __crear_persona(self, cursor, dni, nombre, email):
        """Submetodo de crear alumno/profesor para dar de alta el mismo en la entidad
        personas"""
        query = "INSERT INTO personas (dni,nombre,email) VALUES (%s,%s,%s)"
        cursor.execute(
            query,
            (dni, nombre, email),
        )
        return cursor.lastrowid

    def existe_dni(self, dni):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor()
            query = "SELECT COUNT(*) FROM personas as p where p.dni=%s"
            cursor.execute(query, (dni,))
            resultado = cursor.fetchone()
            return resultado[0] > 0
        except Exception as e:
            raise IntegridadDatos(f"Error al consultar existencia DNI en BD->{e}")
        finally:
            if cursor:
                cursor.close()

    def actualizar_persona(self, id, dni, nombre, email):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor()
            query = (
                "UPDATE personas SET dni=%s, nombre=%s, email=%s  WHERE  id_persona=%s"
            )
            cursor.execute(
                query,
                (dni, nombre, email, id),
            )
            con.commit()
        except Exception as e:
            con.rollback()
            raise IntegridadDatos(f"Error al actualizar usuario en BD:{e}")
        finally:
            if cursor:
                cursor.close()

    def actualizar_profesor(self, id, especialidad, salario):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor()
            query = (
                "UPDATE profesores SET especialidad=%s, salario=%s where id_persona=%s"
            )
            cursor.execute(
                query,
                (especialidad, salario, id),
            )
            con.commit()
        except Exception as e:
            con.rollback()
            raise IntegridadDatos(f"Error al actualizar profeson en BD: {e}")
        finally:
            if cursor:
                cursor.close()

    def eliminar_usuario(self, dni):
        con = self.__obtener_conexion()
        try:
            cursor = con.cursor()
            query = "DELETE FROM personas where dni=%s"
            cursor.execute(
                query,
                (dni,),
            )
            con.commit()
        except Exception as e:
            con.rollback()
            raise IntegridadDatos(f"Error al eliminar usuario en BD: {e}")
        finally:
            if cursor:
                cursor.close()
