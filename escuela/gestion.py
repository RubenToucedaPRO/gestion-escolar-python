from .common import Duplicado, DatoInvalido, Validator
from .modelos import Alumno, Profesor, Persona, Administrador, Asignatura
from .config import (
    CONTRASENA_POR_DEFECTO,
    ROL_ALUMNO,
    ROL_PROFESOR,
    ROL_ADMIN,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
)
from .registrar import Registrar
from .db_manager import DBManager


class CentroEducativo:
    def __init__(self):
        self.db = DBManager(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

    def validar_login(self, dni, contrasena):
        datos_usuario = self.db.validar_credenciales(dni, contrasena)

        if datos_usuario:
            return self.obtener_usuario(dni, datos_usuario["rol"])
        return None

    def get_alumnos(self):
        lista_usuarios = []
        datos_bd = self.db.leer_alumnos()
        [lista_usuarios.append(Alumno(**d)) for d in datos_bd]
        return lista_usuarios

    def get_profesores(self):
        lista_usuarios = []
        datos_bd = self.db.leer_profesores()
        [lista_usuarios.append(Profesor(**d)) for d in datos_bd]
        return lista_usuarios

    def crear_alumno(self, dni: str, nombre: str, email: str):
        contrasena = CONTRASENA_POR_DEFECTO
        rol = ROL_ALUMNO
        # instanciamos objeto para verificar y estandarizar datos
        alumno = Alumno(None, dni, nombre, email, rol, contrasena)
        self.verificar_dni_no_registrado(alumno.get_dni())
        self.verificar_email_no_registrado(alumno.get_email())
        self.db.crear_alumno(**alumno.to_dict())
        return alumno

    def crear_profesor(
        self, dni: str, nombre: str, email: str, especialidad: str, salario: float
    ):
        contrasena = CONTRASENA_POR_DEFECTO
        rol = ROL_PROFESOR
        # instanciamos objeto para verificar y estandarizar datos
        profesor = Profesor(
            None, dni, nombre, email, especialidad, salario, rol, contrasena
        )
        self.verificar_dni_no_registrado(profesor.get_dni())
        self.verificar_email_no_registrado(profesor.get_email())
        self.db.crear_profesor(**profesor.to_dict())

    def actualizar_persona(self, usuario: Persona, **datos):
        """Actualiza los datos de usuario de la entidad persona si estos
        han sido modificados"""
        modificado = False
        if datos.get("dni") and datos["dni"] != usuario.get_dni():
            self.verificar_dni_no_registrado(datos.get("dni"))
            usuario.set_dni(datos["dni"])
            modificado = True
        if datos.get("nombre") and datos["nombre"] != usuario.get_nombre():
            usuario.set_nombre(datos["nombre"])
            modificado = True
        if datos.get("email") and datos["email"] != usuario.get_email():
            self.verificar_email_no_registrado(datos["email"])
            usuario.set_email(datos["email"])
            modificado = True
        if modificado:
            self.db.actualizar_persona(
                usuario.get_id(),
                usuario.get_dni(),
                usuario.get_nombre(),
                usuario.get_email(),
            )

    def actualizar_profesor(self, usuario: Profesor, **datos):
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

    def obtener_usuario(self, dni_usuario: str, rol: str) -> Persona:
        Validator.validar_dni(dni_usuario)
        encontrado = False
        usuario = self.db.obtener_usuario_dni(dni_usuario)
        if usuario and usuario["rol"] == ROL_ALUMNO:
            encontrado = True
            usuario = self.instanciar_datos_db_alumno(usuario)
        elif usuario and usuario["rol"] == ROL_PROFESOR:
            encontrado = True
            usuario = self.instanciar_datos_db_profesor(usuario)
        elif usuario and usuario["rol"] == ROL_ADMIN:
            encontrado = True
            usuario = self.instanciar_datos_db_admin(usuario)

        if not encontrado or usuario.get_rol() != rol:
            raise DatoInvalido(
                f"Dni: {dni_usuario!r}-> No existe el {rol} en el centro"
            )
        return usuario

    def obtener_usuario_por_id(self, id: int, rol: str) -> Persona:
        encontrado = False
        usuario = self.db.obtener_usuario_id(id)
        if usuario and usuario["rol"] == ROL_ALUMNO:
            encontrado = True
            usuario_instanciado = self.instanciar_datos_db_alumno(usuario)
        if usuario and usuario["rol"] == ROL_PROFESOR:
            encontrado = True
            usuario_instanciado = self.instanciar_datos_db_profesor(usuario)
        if usuario and usuario["rol"] == ROL_ADMIN:
            encontrado = True
            usuario_instanciado = self.instanciar_datos_db_admin(usuario)

        if not encontrado or usuario_instanciado.get_rol() != rol:
            raise DatoInvalido(
                f"Usuario con id: {id!r}-> No existe el {rol} en el centro"
            )

        return usuario_instanciado

    def verificar_dni_no_registrado(self, dni_usuario: str):
        # Formateamos el dni
        dni_usuario = Validator.validar_dni(dni_usuario)
        # Comprobamos en BD que no existe otro usuario
        existe = self.db.existe_dni_usuario(dni_usuario)
        if existe:
            raise Duplicado(
                f"Usuario con dni: {dni_usuario!r}-> Ya existe en el centro"
            )

    def verificar_email_no_registrado(self, email: str):
        # Formateamos el email
        email = email.strip().lower()
        # Comprobamos en BD que no existe ya en otro usuario
        existe = self.db.existe_email_usuario(email)
        if existe:
            raise Duplicado(
                f"Email: {email!r}-> Ya usado por otro usuario en el centro"
            )

    def obtener_alumno(self, dni_alumno: str) -> Alumno:
        Validator.validar_dni(dni_alumno)
        usuario = self.obtener_usuario(dni_alumno, ROL_ALUMNO)
        if not usuario or not isinstance(usuario, Alumno):
            raise DatoInvalido(
                f"Alumno con dni: {dni_alumno!r}-> No existe en el centro"
            )
        return usuario

    def obtener_profesor_asignatura(self, nombre_asignatura: str) -> Profesor:
        dato = self.db.obtener_profesor_asignatura(nombre_asignatura)

        if not dato:
            raise DatoInvalido(
                f"No existe el profesor de {nombre_asignatura!r} en el centro para realizar la calificacion"
            )
        return Profesor(**dato)

    def eliminar_usuario(self, dni_usuario: str):
        dni_usuario = Validator.validar_dni(dni_usuario)
        self.db.eliminar_usuario(dni_usuario)
        return dni_usuario

    def media_global_centro(self, numero_alumnos) -> float:
        medias = [dato["media"] for dato in self.db.obtener_notas_medias()]
        if numero_alumnos < 1:
            return 0.0

        return round(sum(medias) / numero_alumnos, 2)

    def obtener_estadisticas(self) -> dict:
        lista_profesores = self.db.leer_profesores()
        lista_alumnos = self.db.leer_alumnos()
        numero_alumnos = len(lista_alumnos)
        numero_profesores = len(lista_profesores)
        estadisticas = {}
        estadisticas["Total Profesores"] = numero_profesores
        estadisticas["Total Alumnos"] = numero_alumnos
        estadisticas["Total usuarios"] = numero_profesores + numero_alumnos
        estadisticas["Nota media global del centro"] = self.media_global_centro(
            numero_alumnos
        )
        return estadisticas

    def matricular_alumno(self, alumno: Alumno, nombre_asignatura: str):
        asignatura = Asignatura(None, nombre_asignatura, 0.0)
        ya_matriculado = any(
            asignatura_alumno.get_nombre() == asignatura.get_nombre()
            for asignatura_alumno in alumno.get_asignaturas()
        )
        if ya_matriculado:
            raise Duplicado(f"Alumno ya matriculado en {asignatura.get_nombre()}")
        existe_asignatura = self.db.existe_asignatura(asignatura.get_nombre())
        id_asignatura = existe_asignatura[0]
        id_alumno = alumno.get_id()
        self.db.matricular_alumno(id_alumno, id_asignatura)
        return asignatura.get_nombre()

    def calificar_alumno(self, alumno: Alumno, nombre_asignatura: str, nota: float):
        """Se reciben los datos del alumno si ha sido matriculado y se procede
        a calificarlo"""
        asignatura = Asignatura(None, nombre_asignatura, nota)
        # Obtenemos el profesor con la especialidad de la asignatura para calificar al alumno
        profesor = self.obtener_profesor_asignatura(asignatura.get_nombre())
        # Calificar el alumno desde el profesor
        id_asignatura = profesor.calificar(
            alumno, asignatura.get_nombre(), asignatura.get_nota()
        )
        self.db.asignar_nota_asignatura_alumno(
            asignatura.get_nota(), alumno.get_id(), id_asignatura
        )
        return asignatura

    def ejecutar_sql_libre(self, query: str):
        # Limipamos la consulta y la pasamos a minusculas para que reconozca las entidades
        # dado que estas están en minusculas
        query = query.strip().lower()
        if query.count(";") > 1:
            raise DatoInvalido("Error: Solo se permite una sentencia SQL de cada vez")
        return self.db.ejecutar_consulta(query)

    def cerrar_sistema(self):
        self.db.cerrar()

    def obtener_todas_las_asignaturas(self):
        lista = [dato[0] for dato in self.db.obtener_todas_las_asignaturas()]
        return lista

    def crear_asignatura(self, nombre: str):
        asignatura = Asignatura(None, nombre, 0.0)
        existe_asignatura = self.db.existe_asignatura(asignatura.get_nombre())
        if not existe_asignatura:
            self.db.crear_asignatura(asignatura.get_nombre())
        else:
            raise Duplicado(
                f"Asignatura {asignatura.get_nombre() | r} ya existe en el centro"
            )

    def eliminar_asignatura(self, nombre: str):
        self.db.eliminar_asignatura(nombre)
        return nombre

    def instanciar_datos_db_alumno(self, usuario: Alumno):
        usuario.pop("especialidad")
        usuario.pop("salario")
        alumno = Alumno(**usuario)
        self.obtener_asignaturas_alumno(alumno)
        return alumno

    def instanciar_datos_db_profesor(self, usuario: Profesor):
        return Profesor(**usuario)

    def instanciar_datos_db_admin(self, usuario: Alumno):
        usuario.pop("especialidad")
        usuario.pop("salario")
        administrador = Administrador(**usuario)
        return administrador

    def obtener_asignaturas_alumno(self, alumno: Alumno):
        asignaturas = self.db.obtener_asignaturas_alumno(alumno.get_id())
        if asignaturas:
            alumno.set_asignaturas(asignaturas)

    def registro_historial(self, tarea: str, mensaje: str):
        """Realiza registro de las tareas en el log cuando son exitosas"""
        Registrar.registrar_log(tarea, mensaje)
