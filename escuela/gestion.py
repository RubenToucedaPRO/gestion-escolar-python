from .common import Duplicado, DatoInvalido
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
        datos = []
        for dato in lista:
            if not dato.get("salario"):
                alumno = Alumno(dato["dni"], dato["nombre"], dato["email"])
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

    def guardar_en_memoria(self, objeto: object):
        """Según el tipo de objeto recibido realiza la salvaguarda en el fichero json
        del tipo correspondiente"""
        if isinstance(objeto, Alumno):
            lista = self.obtener_alumnos()
            lista_dict = self.lista_to_dict(lista)
            self.archivo_alumnos.guardar_en_json(lista_dict)
        if isinstance(objeto, Profesor):
            lista = self.obtener_profesores()
            lista_dict = self.lista_to_dict(lista)
            self.archivo_profesores.guardar_en_json(lista_dict)
        if isinstance(objeto, Asignatura):
            lista = self.obtener_asignaturas()
            self.archivo_asignaturas.guardar_en_json(lista)

    def lista_to_dict(self, lista):
        lisat_dict = []
        for objeto in lista:
            lisat_dict.append(objeto.to_dict())
        return lisat_dict

    def crear_usuario(self, persona):
        dni_nuevo = persona.get_dni()
        for usuario in self._usuarios:
            if dni_nuevo == usuario.get_dni():
                raise Duplicado(
                    f"{dni_nuevo!r} ya existe en el sistema -> se omite usuario"
                )
        self._usuarios.append(persona)
        self.guardar_en_memoria(persona)

    def listar_usuarios(self):
        if not self._usuarios:
            print("Sin usuarios registrados en el centro")
        for usuario in self._usuarios:
            print(usuario)

    def obtener_numero_usuarios(self):
        return len(self._usuarios)

    def obtener_usuario(self, dni_usuario) -> Persona:
        encontrado = False

        for usuario in self.get_usuarios():
            if usuario.get_dni() == dni_usuario:
                return usuario

        if not encontrado:
            raise DatoInvalido(
                f"Usuario con dni: {dni_usuario}-> No existe el usuario en el centro"
            )

    def obtener_alumno(self, dni_alumno):
        encontrado = False

        for usuario in self.obtener_alumnos():
            if usuario.get_dni() == dni_alumno:
                return usuario

        if not encontrado:
            raise DatoInvalido(
                f"Alumno con dni: {dni_alumno}-> No existe el alumno en el centro"
            )

    def obtener_profesor_asignatura(self, asignatura: Asignatura):
        encontrado = False

        for usuario in self.obtener_profesores():
            if usuario.get_especialidad() == asignatura.get_nombre():
                return usuario

        if not encontrado:
            raise DatoInvalido(
                f"No existe el profesor de {asignatura.get_nombre()!r}en el centro para realizar la calificacion"
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
        matriculados los alumnos para tener siempre el json de asignaturas actualizado"""
        lista_asignaturas = []
        lista_alumnos = self.obtener_alumnos()
        for alumno in lista_alumnos:
            if len(alumno.get_asignaturas()) > 0:
                for asignatura in alumno.get_asignaturas():
                    lista_asignaturas.append(asignatura.get_nombre())
        # lo pasamos a conjunto para evitar asignaturas repetidas y volvemos a
        # devolver una lista
        return list(set(lista_asignaturas))

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
        self.guardar_en_memoria(usuario)
        self.guardar_en_memoria(asignatura)
