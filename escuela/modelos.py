from abc import ABC, abstractmethod
from .common import DatoInvalido, Duplicado, Validator
from functools import reduce


class Persona(ABC):
    def __init__(self, dni: str, nombre: str, email: str):
        self.set_dni(dni)
        self.set_nombre(nombre)
        self.set_email(email)

    @abstractmethod
    def __str__(self):
        return f"{self.nombre} ({self._dni})"

    def get_dni(self):
        return self._dni

    def set_dni(self, dni: str):
        if not dni:
            raise DatoInvalido("El dni no puede estar vacío.")
        dni = Validator.validar_dni(dni)
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

    def to_dict(self):
        return {"dni": self._dni, "nombre": self.nombre, "email": self.email}


class Asignatura:
    def __init__(self, nombre: str, nota: float = 0.0):
        self.set_nombre(nombre)
        self.set_nota(nota)

    def __str__(self):
        return f"{self.nombre}: {self._nota}"

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        nombre = Validator.formatear_nombre(nombre)
        self.nombre = nombre

    def get_nota(self):
        return self._nota

    def set_nota(self, nota: float):
        if not isinstance(nota, float) or (nota < 0.0 or nota > 10.0):
            raise DatoInvalido("La nota debe de ser un numero decimal entre 0 y 10")
        self._nota = nota

    def to_dict(self):
        return {
            "nombre": self.nombre,
        }

    def to_dict_alumno(self):
        return {
            "nombre": self.nombre,
            "nota": self._nota,
        }


class Alumno(Persona):
    def __init__(self, dni: str, nombre: str, email: str):
        super().__init__(dni, nombre, email)
        self._asignaturas = []

    def __str__(self):
        return f"[ALUMNO] {super().get_nombre()}"

    def get_asignaturas(self):
        return self._asignaturas

    def set_asignaturas(self, asignaturas: list):
        for asignatura in asignaturas:
            self._asignaturas.append(
                Asignatura(asignatura["nombre"], asignatura["nota"])
            )

    def matricular(self, asignatura: Asignatura):
        existe_asignatura = [
            True
            for asignatura_alumno in self._asignaturas
            if asignatura.get_nombre() == asignatura_alumno.get_nombre()
        ]
        if self._asignaturas and any(existe_asignatura):
            raise Duplicado(
                f"Alumon con DNI: {self.get_dni()}-> Ya está matriculado en {asignatura.get_nombre()!r}"
            )
        self._asignaturas.append(asignatura)

    def nota_media(self):
        if not self._asignaturas:
            return 0
        suma = reduce(
            lambda suma, asignatura: suma + asignatura.get_nota(), self._asignaturas, 0
        )
        return round(suma / len(self._asignaturas), 2)

    def to_dict(self):
        asignaturas = [asignatura.to_dict_alumno() for asignatura in self._asignaturas]
        return {
            "dni": self._dni,
            "nombre": self.nombre,
            "email": self.email,
            "asignaturas": asignaturas,
        }


class Profesor(Persona):
    def __init__(self, dni, nombre, email, especialidad: str, salario: float = 0):
        super().__init__(dni, nombre, email)
        self.set_especialidad(especialidad)
        self.set_salario(salario)

    def __str__(self):
        return f"[PROFESOR] {super().get_nombre()} - {self.get_especialidad()}"

    def get_especialidad(self):
        return self.especialidad

    def set_especialidad(self, especialidad):
        if not especialidad:
            raise ValueError(
                f"Profesor {self.get_nombre()}-> La especialidad no puede estar vacía."
            )
        self.especialidad = especialidad.strip().capitalize()

    def get_salario(self):
        return self.salario

    def set_salario(self, salario):
        try:
            valor_float = float(salario)
            self.salario = valor_float
        except ValueError:
            raise DatoInvalido(f"'{salario}' no es un número decimal válido")

    def calificar(self, alumno: Alumno, nombre_asignatura, nota):
        nombre_asignatura = nombre_asignatura.strip().capitalize()
        lista_asignaturas = alumno.get_asignaturas()
        encontrada = False
        for asignatura in lista_asignaturas:
            if asignatura.get_nombre() == nombre_asignatura:
                encontrada = True
                asignatura.set_nota(nota)
        if not encontrada:
            raise DatoInvalido(
                f"El alumno {alumno.get_nombre()} no tiene la asignatura {nombre_asignatura}"
            )

    def to_dict(self):
        return {
            "dni": self._dni,
            "nombre": self.nombre,
            "email": self.email,
            "especialidad": self.especialidad,
            "salario": self.salario,
        }
