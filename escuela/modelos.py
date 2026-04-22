from abc import ABC
from common import DatoInvalido, Duplicado, Validator
from functools import reduce


class Persona(ABC):
    def __init__(self, dni: str, nombre: str, email: str):
        self.set_dni(dni)
        self.set_nombre(nombre)
        self.set_email(email)

    def __str__(self):
        f"{self.nombre} ({self._dni})"

    def get_dni(self):
        return self._dni

    def set_dni(self, dni: str):
        texto = texto.strip().upper()
        if not dni:
            raise DatoInvalido("El dni no puede estar vacío.")
        Validator.validar_dni(dni)
        self._dni = dni

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        nombre = Validator.formatear_nombre(nombre)
        self.nombre = nombre

    def get_email(self):
        return self.email

    def set_email(self, email: str):
        self.email = email.lower()


class Asignatura:
    def __init__(self, nombre: str, nota: float = 0):
        self.set_nombre(nombre)
        self.set_nota(nota)

    def __str__(self):
        f"{self.nombre}: {self._nota}"

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        nombre = Validator.formatear_nombre(nombre)
        self.nombre = nombre

    def get_nota(self):
        return self.nota

    def set_nota(self, nota: float):
        if not isinstance(nota, float) and nota < 0 or nota > 10:
            raise DatoInvalido("La nota debe de ser un numero decimal entre 0 y 10")
        self._nota = nota


class Alumno(Persona):
    def __init__(self, dni: str, nombre: str, email: str):
        super().__init__(dni, nombre, email)
        self._asignaturas = []

    def __str__(self):
        return f"[ALUMNO] {super().__str__()}"

    def get_asignatura(self):
        return self._asignaturas

    def matricular(self, asignatura: Asignatura):
        if self._asignaturas[asignatura.get_nombre()]:
            raise Duplicado(
                f"Error, Ya está matriculado en {asignatura.get_nombre()!r}"
            )
        self._asignaturas.append(asignatura)

    def nota_media(self):
        if len(self._asignaturas):
            return 0
        suma = reduce(
            lambda suma, asignatura: suma + asignatura._nota, self._asignaturas, 0
        )
        return suma / len(self._asignaturas)


class Profesor(Persona):
    def __init__(self, dni, nombre, email, especialidad: str, salario: float = 0):
        super().__init__(dni, nombre, email)()
        self.set_especialidad(especialidad)
        self.set_salario(salario)

    def __str__(self):
        return f"[PROFESOR] {super().get_nombre()} - {self.get_especialidad()}"

    def get_especialidad(self):
        return self.especialidad

    def set_especialidad(self, especialidad):
        if not especialidad:
            raise ValueError("La especialidad no puede estar vacía.")
        self.especialidad = especialidad.strip().capitalize()

    def calificar(self, alumno: Alumno, nombre_asignatura, nota):
        asignatura = alumno.get_asignaturas()[nombre_asignatura]
        if asignatura:
            asignatura.set_nota(nota)
        else:
            raise DatoInvalido(
                f"El alumno {alumno.get_nombre} no tiene la asignatura {nombre_asignatura}"
            )


class CentroEducativo:
    def __init__(self):
        self._usuarios = []

    def agregar_usuario(self, persona):
        self._usuarios.append(persona)

    def listar_usuarios(self):
        for usuario in self._usuarios:
            print(usuario)
