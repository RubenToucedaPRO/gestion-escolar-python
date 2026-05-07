from .common import Duplicado, DatoInvalido, IntegridadDatos
from .modelos import Alumno, Profesor, Persona, Asignatura
from .registrar import Registrar
from .db_manager import DBManager
# from .ficheros import GestorFicheros


class CentroEducativo:
    def __init__(self):
        self.db = DBManager()
        # self.archivo_alumnos = GestorFicheros("datos/alumnos.json")
        # self.archivo_profesores = GestorFicheros("datos/profesores.json")
        # self.archivo_asignaturas = GestorFicheros("datos/asignaturas.json")

        # self._usuarios = self.set_usuarios(
        #    self.archivo_alumnos.leer_json() + self.archivo_profesores.leer_json()
        # )
        # Asignaturas lo creamos en base a las asignaturas y especialidades
        # registradas en alumnos y profesores. Se instancian en los objetos alumno
        # self.guardar_en_memoria_asignaturas()

    def get_usuarios(self):
        lista_usuarios = []
        datos_bd = self.db.leer_alumnos()
        [lista_usuarios.append(Alumno(**d)) for d in datos_bd]
        datos_bd = self.db.leer_profesores()
        [lista_usuarios.append(Profesor(**d)) for d in datos_bd]

        return lista_usuarios

    def crear_alumno(self, dni, nombre, email):
        self.db.crear_alumno(dni, nombre, email)

    def crear_profesor(self, dni, nombre, email, especialidad, salario):
        self.db.crear_profesor(dni, nombre, email, especialidad, salario)

    def actualizar_persona(self, usuario, **datos):
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

    def set_usuarios(self, lista: list):
        """Convertimos los dict de cada usuario del json al objeto correspondiente"""
        datos = []
        for dato in lista:
            # si no tiene salario es un alumno
            if not dato.get("salario"):
                alumno = Alumno(dato["dni"], dato["nombre"], dato["email"])
                # Instanciamos las asignaturas del alumno con los datos del json
                alumno.set_asignaturas(dato["asignaturas"])
                datos.append(alumno)
            else:
                profesor = Profesor(
                    dato["dni"],
                    dato["nombre"],
                    dato["email"],
                    dato["especialidad"],
                    dato["salario"],
                )
                datos.append(profesor)
        return datos

    # def guardar_en_memoria_usuarios(self, usuario: Persona):
    #     """Según el tipo de objeto recibido realiza la salvaguarda en el fichero json
    #     del tipo correspondiente"""
    #     if isinstance(usuario, Alumno):
    #         self.guardar_en_memoria_alumnos()
    #     if isinstance(usuario, Profesor):
    #         self.guardar_en_memoria_profesores()

    # def guardar_en_memoria_alumnos(self):
    #     lista = self.obtener_alumnos()
    #     lista_dict = self.lista_to_dict(lista)
    #     self.archivo_alumnos.guardar_en_json(lista_dict)

    # def guardar_en_memoria_profesores(self):
    #     lista = self.obtener_profesores()
    #     lista_dict = self.lista_to_dict(lista)
    #     self.archivo_profesores.guardar_en_json(lista_dict)

    # def guardar_en_memoria_asignaturas(self):
    #     lista = self.obtener_asignaturas()
    #     self.archivo_asignaturas.guardar_en_json(lista)

    def lista_to_dict(self, lista):
        lista_dict = []
        for usuario in lista:
            lista_dict.append(usuario.to_dict())
        return lista_dict

    # def crear_usuario(self, usuario):
    #     """Se crea el usuario, la verificación de que el dni no existe en el centro se
    #     hace tras introducir el dni"""
    #     self._usuarios.append(usuario)
    #     self.guardar_en_memoria_usuarios(usuario)

    def obtener_numero_usuarios(self):
        return len(self._usuarios)

    def obtener_usuario(self, dni_usuario) -> Persona:
        encontrado = False
        usuario = self.db.obtener_usuario_dni(dni_usuario)
        if usuario and usuario["es_alumno"]:
            id = usuario.pop("es_alumno")
            usuario.pop("es_profesor")
            usuario.pop("especialidad")
            usuario.pop("salario")
            alumno = Alumno(**usuario)
            asignaturas = self.db.obtener_asignaturas_alumno(id)
            if asignaturas:
                alumno.set_asignaturas(asignaturas)
            return alumno
        if usuario and usuario["es_profesor"]:
            usuario.pop("es_alumno")
            usuario.pop("es_profesor")
            return Profesor(**usuario)

        # for usuario in self.get_usuarios():
        #     if usuario.get_dni() == dni_usuario:
        #         return usuario

        if not encontrado:
            raise DatoInvalido(
                f"Usuario con dni: {dni_usuario!r}-> No existe el usuario en el centro"
            )

    def verificar_dni_no_registrado(self, dni_usuario):
        existe = self.db.existe_dni(dni_usuario)
        if existe:
            raise Duplicado(
                f"Usuario con dni: {dni_usuario!r}-> Ya existe en el centro"
            )
        return False

    def obtener_alumno(self, dni_alumno):
        encontrado = False

        for usuario in self.obtener_alumnos():
            if usuario.get_dni() == dni_alumno:
                return usuario

        if not encontrado:
            raise DatoInvalido(
                f"Alumno con dni: {dni_alumno!r}-> No existe el alumno en el centro"
            )

    def obtener_profesor_asignatura(self, asignatura: Asignatura):
        encontrado = False

        for usuario in self.obtener_profesores():
            if usuario.get_especialidad() == asignatura.get_nombre():
                return usuario

        if not encontrado:
            raise DatoInvalido(
                f"No existe el profesor de {asignatura.get_nombre()!r} en el centro para realizar la calificacion"
            )

    def obtener_alumnos(self):
        lista_alumnos = [
            usuario for usuario in self._usuarios if isinstance(usuario, Alumno)
        ]
        if not lista_alumnos:
            return []
        return lista_alumnos

    def obtener_profesores(self):
        lista_profesores = [
            usuario for usuario in self._usuarios if isinstance(usuario, Profesor)
        ]
        if not lista_profesores:
            return []
        return lista_profesores

    def obtener_asignaturas(self):
        """Obtenemos las asignaturas en funcion del las asignaturas en las que están
        matriculados los alumnos y especializados los profesores para tener siempre
        el json de asignaturas actualizado"""
        lista_asignaturas = []

        lista_alumnos = self.obtener_alumnos()
        for alumno in lista_alumnos:
            if len(alumno.get_asignaturas()) > 0:
                for asignatura in alumno.get_asignaturas():
                    lista_asignaturas.append(asignatura.get_nombre())

        lista_profesores = self.obtener_profesores()
        for profesor in lista_profesores:
            lista_asignaturas.append(profesor.get_especialidad())

        # lo pasamos a conjunto para evitar asignaturas repetidas y volvemos a
        # devolver una lista
        return list(set(lista_asignaturas))

    def eliminar_usuario(self, dni_usuario: str):
        self.db.eliminar_usuario(dni_usuario)

    def media_global_centro(self):
        lista_alumnos = self.obtener_alumnos()
        if not lista_alumnos:
            return 0.0
        medias_alumnos = [alumno.nota_media() for alumno in lista_alumnos]
        return round(sum(medias_alumnos) / len(medias_alumnos), 2)

    def obtener_estadisticas(self):
        lista_profesores = self.obtener_profesores()
        lista_alumnos = self.obtener_alumnos()
        estadisticas = {}
        estadisticas["Total Profesores"] = len(lista_profesores)
        estadisticas["Total Alumnos"] = len(lista_alumnos)
        estadisticas["Total usuarios"] = len(self.get_usuarios())
        estadisticas["Nota media global del centro"] = self.media_global_centro()
        return estadisticas

    def matricular_usuario(self, usuario: Alumno, nombre_asignatura: str):
        asignatura = Asignatura(nombre_asignatura)
        usuario.matricular(asignatura)
        # guardamos en memoria tanto los alumnos como las asignaturas para que queden
        # actualizados
        self.guardar_en_memoria_usuarios(usuario)
        self.guardar_en_memoria_asignaturas()

    def calificar_alumno(self, alumno: Alumno, asignatura: Asignatura):
        """Se reciben los datos del alumno si ha sido matriculado y se procede
        a calificarlo"""
        # Obtenemos el profesor de la asignatura para calificar al alumno
        profesor = self.obtener_profesor_asignatura(asignatura)
        # Calificar el alumno desde el profesor de la asignatura
        profesor.calificar(alumno, asignatura.get_nombre(), asignatura.get_nota())
        self.guardar_en_memoria_usuarios(alumno)

    # def verificar_datos_en_memoria(self):
    #     """Se comparan los datos de los json de alumnos y profesores dado que asignaturas
    #     siempre se regulariza con las asignaturas/especialidades existentes en estos"""
    #     try:
    #         profesores_json = self.archivo_profesores.leer_json()
    #         lista_profesores_json = self.set_usuarios(profesores_json)
    #         lista_alumnos_programa = self.obtener_profesores()
    #         self.comparar_listas(lista_profesores_json, lista_alumnos_programa)

    #         alumnos_json = self.archivo_alumnos.leer_json()
    #         lista_alumnos_json = self.set_usuarios(alumnos_json)
    #         lista_alumnos_programa = self.obtener_alumnos()
    #         self.comparar_listas(lista_alumnos_json, lista_alumnos_programa)
    #     except IntegridadDatos as e:
    #         mensaje = f"ERROR: {e}"
    #         print(mensaje)
    #         Registrar.registrar_log("Salir de la aplicacion", mensaje)
    #         self.guardar_en_memoria_alumnos()
    #         self.guardar_en_memoria_profesores()
    #         self.guardar_en_memoria_asignaturas()

    # def comparar_listas(self, lista_json: list, lista_programa: list):
    #     """Compara usuario a usuario de la lista del json con la lista del programa
    #     de alumnos o profesores"""
    #     tipo = ""
    #     encontrado_en_programa = False
    #     for usuario_json in lista_json:
    #         tipo = type(usuario_json).__name__.lower()
    #         for usuario_programa in lista_programa:
    #             if usuario_json.get_dni() == usuario_programa.get_dni():
    #                 encontrado_en_programa = True
    #                 # se convierten a diccionarios para poder comparalos con !=
    #                 if usuario_json.to_dict() != usuario_programa.to_dict():
    #                     raise IntegridadDatos(
    #                         f"Los datos del {tipo} entre memoria y programa no coinciden,"
    #                         f"{usuario_json.get_dni()!r} -> se regularizan en memoria"
    #                     )

    #         if not encontrado_en_programa:
    #             raise IntegridadDatos(
    #                 f"El {tipo} con dni {usuario_json.get_dni()!r} "
    #                 "registrado en memoria no existe en programa "
    #                 "-> borrado en memoria"
    #             )
    #     if len(lista_json) != len(lista_programa):
    #         raise IntegridadDatos(
    #             f"Alguna lista del programa no coincide "
    #             "con la lista en memoria -> actualizado en memoria "
    #         )

    def registro_historial(self, tarea, mensaje):
        """Realiza registro de las tareas en el log cuando son exitosas"""
        Registrar.registrar_log(tarea, mensaje)
