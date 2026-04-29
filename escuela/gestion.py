from .common import Duplicado, DatoInvalido
from .modelos import Alumno, Profesor, Persona, Asignatura


class CentroEducativo:
    def __init__(self):
        self._usuarios = []

    def get_usuarios(self):
        return self._usuarios

    def agregar_usuario(self, persona):
        dni_nuevo = persona.get_dni()
        for usuario in self._usuarios:
            if dni_nuevo == usuario.get_dni():
                raise Duplicado(
                    f"{dni_nuevo!r} ya existe en el sistema -> se omite usuario"
                )
        self._usuarios.append(persona)

    def listar_usuarios(self):
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
