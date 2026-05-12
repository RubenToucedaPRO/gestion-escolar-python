from .common import Duplicado, DatoInvalido, Validator
from .modelos import Alumno, Profesor, Persona, Asignatura
from .registrar import Registrar
from .db_manager import DBManager
# from .ficheros import GestorFicheros


class CentroEducativo:
    def __init__(self):
        self.db = DBManager()

    def get_usuarios(self):
        lista_usuarios = []
        datos_bd = self.db.leer_alumnos()
        [lista_usuarios.append(Alumno(**d)) for d in datos_bd]
        datos_bd = self.db.leer_profesores()
        [lista_usuarios.append(Profesor(**d)) for d in datos_bd]

        return lista_usuarios

    def crear_alumno(self, dni, nombre, email):
        # instanciamos objeto para verificar y estandarizar datos
        alumno = Alumno(None, dni, nombre, email)
        self.db.crear_alumno(**alumno.to_dict())

    def crear_profesor(self, dni, nombre, email, especialidad, salario):
        # instanciamos objeto para verificar y estandarizar datos
        profesor = Profesor(None, dni, nombre, email, especialidad, salario)
        self.db.crear_profesor(**profesor.to_dict())

    def actualizar_persona(self, usuario, **datos):
        """Actualiza los datos de usuario de la entidad persona si estos
        han sido modificados"""
        modificado = False
        if datos.get("dni") and datos["dni"] != usuario.get_dni():
            usuario.set_dni(datos["dni"])
            modificado = True
        if datos.get("nombre") and datos["nombre"] != usuario.get_nombre():
            usuario.set_nombre(datos["nombre"])
            modificado = True
        if datos.get("email") and datos["email"] != usuario.get_email():
            usuario.set_email(datos["email"])
            modificado = True
        if modificado:
            self.db.actualizar_persona(
                usuario.get_id(),
                usuario.get_dni(),
                usuario.get_nombre(),
                usuario.get_email(),
            )

    def actualizar_profesor(self, usuario, **datos):
        """Actualiza los datos de la entidad profesores (especialidad y salario)"""
        modificado = False
        if (
            datos.get("especialidad")
            and datos["especialidad"] != usuario.get_especialidad()
        ):
            usuario.set_especialidad(datos["especialidad"])
            modificado = True
        if datos.get("salario") and datos["salario"] != usuario.get_salario():
            usuario.set_salario(datos["salario"])
            modificado = True
        if modificado:
            self.db.actualizar_profesor(
                usuario.get_id(),
                usuario.get_especialidad(),
                usuario.get_salario(),
            )

    def obtener_usuario(self, dni_usuario) -> Persona:
        encontrado = False
        usuario = self.db.obtener_usuario_dni(dni_usuario)
        if usuario and usuario["es_alumno"]:
            return self.instanciar_datos_db_alumno(usuario)
        if usuario and usuario["es_profesor"]:
            return self.instanciar_datos_db_profesor(usuario)

        if not encontrado:
            raise DatoInvalido(
                f"Usuario con dni: {dni_usuario!r}-> No existe el usuario en el centro"
            )

    def verificar_dni_no_registrado(self, dni_usuario):
        existe = self.db.existe_dni_usuario(dni_usuario)
        if existe:
            raise Duplicado(
                f"Usuario con dni: {dni_usuario!r}-> Ya existe en el centro"
            )

    def obtener_alumno(self, dni_alumno):
        usuario = self.obtener_usuario(dni_alumno)
        if not usuario or not isinstance(usuario, Alumno):
            raise DatoInvalido(
                f"Alumno con dni: {dni_alumno!r}-> No existe en el centro"
            )
        return usuario

    def obtener_profesor_asignatura(self, nombre_asignatura):
        dato = self.db.obtener_profesor_asignatura(nombre_asignatura)

        if not dato:
            raise DatoInvalido(
                f"No existe el profesor de {nombre_asignatura!r} en el centro para realizar la calificacion"
            )
        return Profesor(**dato)

    def eliminar_usuario(self, dni_usuario: str):
        self.db.eliminar_usuario(dni_usuario)

    def media_global_centro(self, numero_alumnos):
        medias = [dato["media"] for dato in self.db.obtener_notas_medias()]
        if numero_alumnos < 1:
            return 0.0

        return round(sum(medias) / numero_alumnos, 2)

    def obtener_estadisticas(self):
        lista_profesores = self.db.leer_profesores()
        lista_alumnos = self.db.leer_alumnos()
        numero_alumnos = len(lista_alumnos)
        estadisticas = {}
        estadisticas["Total Profesores"] = len(lista_profesores)
        estadisticas["Total Alumnos"] = numero_alumnos
        estadisticas["Total usuarios"] = len(self.get_usuarios())
        estadisticas["Nota media global del centro"] = self.media_global_centro(
            numero_alumnos
        )
        return estadisticas

    def matricular_alumno(self, alumno: Alumno, nombre_asignatura: str):
        nombre_asignatura = Validator.formatear_nombre(nombre_asignatura)
        ya_matriculado = any(
            asignatura.get_nombre() == nombre_asignatura
            for asignatura in alumno.get_asignaturas()
        )
        if ya_matriculado:
            raise Duplicado(f"Alumno ya matriculado en {nombre_asignatura}")
        existe_asignatura = self.db.existe_asignatura(nombre_asignatura)
        if not existe_asignatura:
            id_asignatura = self.db.crear_asignatura(nombre_asignatura)
        else:
            id_asignatura = existe_asignatura[0]
        id_alumno = alumno.get_id()
        self.db.matricular_alumno(id_alumno, id_asignatura)

    def calificar_alumno(self, alumno: Alumno, nombre_asignatura, nota):
        """Se reciben los datos del alumno si ha sido matriculado y se procede
        a calificarlo"""
        nombre_asignatura = Validator.formatear_nombre(nombre_asignatura)
        # Obtenemos el profesor con la especialidad de la asignatura para calificar al alumno
        profesor = self.obtener_profesor_asignatura(nombre_asignatura)
        # Calificar el alumno desde el profesor
        id_asignatura = profesor.calificar(alumno, nombre_asignatura, nota)
        self.db.asignar_nota_asignatura_alumno(nota, alumno.get_id(), id_asignatura)

    def ejecutar_sql_libre(self, query):
        query = query.strip()
        if query.count(";") > 1:
            raise ValueError("Error: Solo se permite una sentencia SQL de cada vez")
        return self.db.ejecutar_consulta(query)

    def cerrar_sistema(self):
        self.db.cerrar()

    def instanciar_datos_db_alumno(self, usuario):
        usuario.pop("es_alumno")
        usuario.pop("es_profesor")
        usuario.pop("especialidad")
        usuario.pop("salario")
        alumno = Alumno(**usuario)
        self.obtener_asignaturas_alumno(alumno)
        return alumno

    def instanciar_datos_db_profesor(self, usuario):
        usuario.pop("es_alumno")
        usuario.pop("es_profesor")
        return Profesor(**usuario)

    def obtener_asignaturas_alumno(self, alumno: Alumno):
        asignaturas = self.db.obtener_asignaturas_alumno(alumno.get_id())
        if asignaturas:
            alumno.set_asignaturas(asignaturas)

    def registro_historial(self, tarea, mensaje):
        """Realiza registro de las tareas en el log cuando son exitosas"""
        Registrar.registrar_log(tarea, mensaje)
