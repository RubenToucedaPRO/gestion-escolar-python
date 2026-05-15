import mysql.connector
from mysql.connector.cursor import MySQLCursor
from .common import BaseDatosError


class DBManager:
    def __init__(self, host, user, password, nombre_bd):
        self.con = None
        self._conectar(host, user, password, nombre_bd)

    def _conectar(self, host: str, user: str, password: str, nombre_bd: str):
        try:
            self.con = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=nombre_bd,
            )
        except Exception as e:
            mensaje = f"Error al crear la conexion a la BD-> {e}"
            raise BaseDatosError(mensaje)

    def leer_alumnos(self) -> list:
        cursor = self.con.cursor(dictionary=True)
        query = """
        SELECT p.* 
        FROM alumnos as a 
        JOIN personas as p 
        ON a.id_persona=p.id_persona
        """
        cursor.execute(query)
        return cursor.fetchall()

    def leer_profesores(self) -> list:
        cursor = self.con.cursor(dictionary=True)
        query = """
        SELECT p.*,pr.especialidad, pr.salario 
        FROM profesores as pr 
        JOIN personas as p 
        ON pr.id_persona=p.id_persona
        """
        cursor.execute(query)
        return cursor.fetchall()

    def obtener_usuario_dni(self, dni: str) -> dict:
        cursor = self.con.cursor(dictionary=True)
        query = """
        SELECT p.*, pr.especialidad, pr.salario
        FROM personas as p 
        LEFT JOIN alumnos as a ON  p.id_persona=a.id_persona 
        LEFT JOIN profesores as pr ON p.id_persona=pr.id_persona 
        where p.dni=%s
        """
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
        cursor.fetchall()
        return resultado

    def obtener_usuario_id(self, id: int) -> dict:
        cursor = self.con.cursor(dictionary=True)
        query = """
        SELECT p.*, pr.especialidad, pr.salario
        FROM personas as p 
        LEFT JOIN alumnos as a ON  p.id_persona=a.id_persona 
        LEFT JOIN profesores as pr ON p.id_persona=pr.id_persona 
        where p.id_persona=%s
        """
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        cursor.fetchall()
        return resultado

    def obtener_asignaturas_alumno(self, id: int) -> list:
        cursor = self.con.cursor(dictionary=True)
        query = """
        SELECT a.*,m.nota
        FROM asignaturas as a 
        JOIN matriculas as m ON a.id_asignatura=m.id_asignatura 
        where m.id_alumno=%s
        """
        cursor.execute(query, (id,))
        return cursor.fetchall()

    def crear_alumno(
        self, dni: str, nombre: str, email: str, rol: str, contrasena: str
    ):
        cursor = self.con.cursor()
        nuevo_id = self.__crear_persona(cursor, dni, nombre, email, rol, contrasena)
        query = "INSERT INTO alumnos (id_persona) VALUES (%s)"
        cursor.execute(query, (nuevo_id,))
        self.con.commit()

    def crear_profesor(
        self,
        dni: str,
        nombre: str,
        email: str,
        especialidad: str,
        salario: float,
        rol: str,
        contrasena: str,
    ):
        cursor = self.con.cursor()
        nuevo_id = self.__crear_persona(cursor, dni, nombre, email, rol, contrasena)
        query = (
            "INSERT INTO profesores (id_persona,especialidad,salario) VALUES (%s,%s,%s)"
        )
        cursor.execute(query, (nuevo_id, especialidad, salario))
        self.con.commit()

    def __crear_persona(
        self,
        cursor: MySQLCursor,
        dni: str,
        nombre: str,
        email: str,
        rol: str,
        contrasena: str,
    ) -> int:
        """Submetodo de crear alumno/profesor para dar de alta el mismo en la entidad
        personas"""
        query = "INSERT INTO personas (dni,nombre,email,rol,contrasena) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(
            query,
            (dni, nombre, email, rol, contrasena),
        )
        return cursor.lastrowid

    def existe_dni_usuario(self, dni: str) -> bool:
        cursor = self.con.cursor()
        query = "SELECT COUNT(*) FROM personas as p where p.dni=%s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
        cursor.fetchall()
        return resultado[0] > 0

    def existe_email_usuario(self, email: str) -> bool:
        cursor = self.con.cursor()
        query = "SELECT COUNT(*) FROM personas as p where p.email=%s"
        cursor.execute(query, (email,))
        resultado = cursor.fetchone()
        cursor.fetchall()
        return resultado[0] > 0

    def actualizar_persona(self, id: int, dni: str, nombre: str, email: str):
        cursor = self.con.cursor()
        query = "UPDATE personas SET dni=%s, nombre=%s, email=%s  WHERE  id_persona=%s"
        cursor.execute(
            query,
            (dni, nombre, email, id),
        )
        self.con.commit()

    def actualizar_profesor(self, id: int, especialidad: str, salario: float):
        cursor = self.con.cursor()
        query = "UPDATE profesores SET especialidad=%s, salario=%s where id_persona=%s"
        cursor.execute(
            query,
            (especialidad, salario, id),
        )
        self.con.commit()

    def eliminar_usuario(self, dni: str):
        cursor = self.con.cursor()
        query = "DELETE FROM personas where dni=%s"
        cursor.execute(
            query,
            (dni,),
        )
        self.con.commit()

    def existe_asignatura(self, nombre: str) -> dict:
        cursor = self.con.cursor()
        query = "SELECT id_asignatura FROM asignaturas where nombre=%s"
        cursor.execute(
            query,
            (nombre,),
        )
        resultado = cursor.fetchone()
        cursor.fetchall()
        return resultado

    def crear_asignatura(self, nombre: str) -> int:
        cursor = self.con.cursor()
        query = "INSERT INTO asignaturas (nombre) VALUES(%s)"
        cursor.execute(
            query,
            (nombre,),
        )
        self.con.commit()
        return cursor.lastrowid

    def matricular_alumno(self, id_alumno: int, id_asignatura: int):
        cursor = self.con.cursor()
        query = "INSERT INTO matriculas (id_alumno,id_asignatura,nota) VALUES(%s,%s,%s)"
        cursor.execute(
            query,
            (id_alumno, id_asignatura, 0),
        )
        self.con.commit()

    def obtener_todas_las_asignaturas(self):
        cursor = self.con.cursor()
        query = "SELECT nombre FROM asignaturas"
        cursor.execute(query)
        return cursor.fetchall()

    def obtener_profesor_asignatura(self, nombre_asignatura: str) -> dict:
        cursor = self.con.cursor(dictionary=True)
        query = "Select * FROM profesores as pr JOIN personas as p ON  pr.id_persona=p.id_persona where especialidad=%s"
        cursor.execute(
            query,
            (nombre_asignatura,),
        )
        resultado = cursor.fetchone()
        cursor.fetchall()
        return resultado

    def asignar_nota_asignatura_alumno(
        self, nota: float, id_alumno: int, id_asignatura: int
    ):
        cursor = self.con.cursor()
        query = "UPDATE matriculas SET nota=%s WHERE id_alumno=%s AND id_asignatura=%s"
        cursor.execute(
            query,
            (nota, id_alumno, id_asignatura),
        )

    def obtener_notas_medias(self) -> list:
        cursor = self.con.cursor(dictionary=True)
        query = """
            SELECT AVG(m.nota) AS media
            FROM personas p
            JOIN alumnos a ON p.id_persona = a.id_persona
            JOIN matriculas m ON a.id_persona = m.id_alumno
            GROUP BY p.id_persona;
        """
        cursor.execute(query)
        return cursor.fetchall()

    def ejecutar_consulta(self, query: str) -> tuple:
        cursor = self.con.cursor()
        cursor.execute(query)
        if cursor.description:
            columnas = [desc[0] for desc in cursor.description]
            return columnas, cursor.fetchall()
        else:
            self.con.commit()
            return [("Nº operaciones",), ((cursor.rowcount,),)]

    def validar_credenciales(self, dni, contrasena):
        cursor = self.con.cursor(dictionary=True, buffered=True)
        # Buscamos en la tabla personas
        query = (
            "SELECT dni, nombre, rol FROM personas WHERE dni = %s AND contrasena = %s"
        )
        cursor.execute(query, (dni, contrasena))
        return cursor.fetchone()

    def cerrar(self):
        if self.con:
            self.con.close()
