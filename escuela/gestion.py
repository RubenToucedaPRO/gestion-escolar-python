from .common import Duplicado, DatoInvalido, IntegridadDatos
from .modelos import Alumno, Profesor, Persona, Asignatura
from .ficheros import GestorFicheros


class CentroEducativo:
    def __init__(self):
        self.archivo_alumnos = GestorFicheros("datos/alumnos.json")
        self.archivo_profesores = GestorFicheros("datos/profesores.json")
        self.archivo_asignaturas = GestorFicheros("datos/asignaturas.json")

        self._usuarios = self.set_usuarios(
            self.archivo_alumnos.leer_json() + self.archivo_profesores.leer_json()
        )

    def get_usuarios(self):
        return self._usuarios

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

    def guardar_en_memoria_usuarios(self, persona: Persona):
        """Según el tipo de objeto recibido realiza la salvaguarda en el fichero json
        del tipo correspondiente"""
        if isinstance(persona, Alumno):
            lista = self.obtener_alumnos()
            lista_dict = self.lista_to_dict(lista)
            self.archivo_alumnos.guardar_en_json(lista_dict)
        if isinstance(persona, Profesor):
            lista = self.obtener_profesores()
            lista_dict = self.lista_to_dict(lista)
            self.archivo_profesores.guardar_en_json(lista_dict)

    def guardar_en_memoria_asignaturas(self):
        lista = self.obtener_asignaturas()
        self.archivo_asignaturas.guardar_en_json(lista)

    def lista_to_dict(self, lista):
        lista_dict = []
        for objeto in lista:
            lista_dict.append(objeto.to_dict())
        return lista_dict

    def crear_usuario(self, persona):
        """Se crea el usuario, la verificación de que el dni no existe en el centro se
        hace tras introducir el dni"""
        self._usuarios.append(persona)
        self.guardar_en_memoria_usuarios(persona)

    def get_usuarios(self):
        return self._usuarios

    def obtener_numero_usuarios(self):
        return len(self._usuarios)

    def obtener_usuario(self, dni_usuario) -> Persona:
        encontrado = False

        for usuario in self.get_usuarios():
            if usuario.get_dni() == dni_usuario:
                return usuario

        if not encontrado:
            raise DatoInvalido(
                f"Usuario con dni: {dni_usuario!r}-> No existe el usuario en el centro"
            )

    def verificar_dni_no_registrado(self, dni_usuario):
        for usuario in self.get_usuarios():
            if usuario.get_dni() == dni_usuario:
                raise Duplicado(
                    f"Usuario con dni: {dni_usuario!r}-> Ya existe en el centro"
                )

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
            raise DatoInvalido("No existen alumnos en el centro")
        return lista_alumnos

    def obtener_profesores(self):
        lista_profesores = [
            usuario for usuario in self._usuarios if isinstance(usuario, Profesor)
        ]
        if not lista_profesores:
            raise DatoInvalido("No existen porfesores en el centro")
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
        usuario = self.obtener_usuario(dni_usuario)
        self.get_usuarios().remove(usuario)
        self.guardar_en_memoria_usuarios(usuario)
        # En caso de ser un alumno dado que tiene asignaturas se actualiza el fihero de
        # asignaturas por si se elimina alguna
        if isinstance(usuario, Alumno):
            self.guardar_en_memoria_asignaturas()

    def media_global_centro(self):
        lista_alumnos = self.obtener_alumnos()
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

    def verificar_datos_en_memoria(self):
        """Se comparan los datos de los json de alumnos y profesores dado que asignaturas
        siempre se regulariza con las asignaturas/especialidades existentes en estos"""
        profesores_json = self.archivo_profesores.leer_json()
        lista_profesores_json = self.set_usuarios(profesores_json)
        lista_alumnos_programa = self.obtener_profesores()
        self.comparar_listas(lista_profesores_json, lista_alumnos_programa)

        alumnos_json = self.archivo_alumnos.leer_json()
        lista_alumnos_json = self.set_usuarios(alumnos_json)
        lista_alumnos_programa = self.obtener_alumnos()
        self.comparar_listas(lista_alumnos_json, lista_alumnos_programa)

    def comparar_listas(self, lista_json: list, lista_programa: list):
        """Compara usuario a usuario de la lista del json con la lista del programa
        de alumnos o profesores"""
        tipo = ""
        for usuario_json in lista_json:
            tipo = type(usuario_json).__name__.lower()
            encontrado_en_programa = False
            for usuario_programa in lista_programa:
                if usuario_json.get_dni() == usuario_programa.get_dni():
                    encontrado_en_programa = True
                    # se convierten a diccionarios para poder comparalos con !=
                    if usuario_json.to_dict() != usuario_programa.to_dict():
                        raise IntegridadDatos(
                            f"Los datos del {tipo} entre memoria y programa no coinciden,"
                            "ejecute modificar con el dni "
                            f"{usuario_json.get_dni()!r} en programa para "
                            "regularizar en memoria"
                        )

            if not encontrado_en_programa:
                raise IntegridadDatos(
                    f"El {tipo} con dni {usuario_json.get_dni()!r} "
                    "registrado en memoria no existe en programa "
                    "borrar en memoria o regularizar programa"
                )
            if len(lista_json) != len(lista_programa):
                raise IntegridadDatos(
                    f"La lista de {tipo}s del programa no coincide "
                    "con la lista en memoria "
                )
