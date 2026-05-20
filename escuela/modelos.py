from abc import ABC, abstractmethod
from .common import DatoInvalido, Duplicado, Validator


class Persona(ABC):
    def __init__(
        self,
        id_persona: int,
        dni: str,
        nombre: str,
        email: str,
        rol: str,
        contrasena: str,
    ):
        self.set_id(id_persona)
        self.set_dni(dni)
        self.set_nombre(nombre)
        self.set_email(email)
        self.set_rol(rol)
        self.set_contrasena(contrasena)

    @abstractmethod
    def __str__(self):
        return f"{self.nombre} ({self._dni})"

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

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

    def set_rol(self, rol: str):
        self._rol = rol

    def get_rol(self):
        return self._rol

    def set_contrasena(self, contrasena: str):
        if contrasena.find(" ") > 0:
            raise DatoInvalido("La contraseña no puede tener espacios.")
        self._contrasena = contrasena

    def get_contrasena(self):
        return self._contrasena

    def to_dict(self):
        return {
            "dni": self._dni,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self._rol,
            "contrasena": self._contrasena,
        }


class Asignatura:
    def __init__(self, id_asignatura: int, nombre: str, nota: float = 0.0):
        self.set_id(id_asignatura)
        self.set_nombre(nombre)
        self.set_nota(nota)

    def __str__(self):
        return f"{self.nombre}: {self._nota}"

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

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
    def __init__(
        self,
        id_persona: int,
        dni: str,
        nombre: str,
        email: str,
        rol: str,
        contrasena: str,
    ):
        super().__init__(id_persona, dni, nombre, email, rol, contrasena)
        self._asignaturas = []

    def __str__(self):
        return f"[ALUMNO] {super().__str__()}"

    def get_asignaturas(self):
        return self._asignaturas

    def set_asignaturas(self, asignaturas: list):
        """Se crean las instancias de las asignaturas en cada usuario"""
        for asignatura in asignaturas:
            self._asignaturas.append(
                Asignatura(
                    asignatura["id_asignatura"],
                    asignatura["nombre"],
                    float(asignatura["nota"]),
                )
            )

    def matricular(self, asignatura: Asignatura):
        existe_asignatura = [
            True
            for asignatura_alumno in self._asignaturas
            if asignatura.get_nombre() == asignatura_alumno.get_nombre()
        ]
        if self._asignaturas and any(existe_asignatura):
            raise Duplicado(
                f"Alumno con DNI: {self.get_dni()!r}-> Ya está matriculado en {asignatura.get_nombre()!r}"
            )
        self._asignaturas.append(asignatura)


class Profesor(Persona):
    def __init__(
        self,
        id_persona: int,
        dni,
        nombre,
        email,
        especialidad: str,
        salario: float,
        rol: str,
        contrasena: str,
    ):
        super().__init__(id_persona, dni, nombre, email, rol, contrasena)
        self.set_especialidad(especialidad)
        self.set_salario(salario)

    def __str__(self):
        return f"[PROFESOR] {super().get_nombre()} - {self.get_especialidad()}"

    def get_especialidad(self):
        return self.especialidad

    def set_especialidad(self, especialidad):
        if not especialidad:
            raise ValueError(
                f"Profesor {self.get_nombre()!r}-> La especialidad no puede estar vacía."
            )
        self.especialidad = especialidad.strip().capitalize()

    def get_salario(self):
        return self.salario

    def set_salario(self, salario):
        try:
            valor_float = float(salario)
            if valor_float <= 0:
                raise ValueError(
                    f"El salario {salario} debe ser un numero decimal positivo"
                )
            self.salario = valor_float
        except ValueError:
            raise DatoInvalido(
                f"Salario '{salario}' no es un número decimal positivo válido"
            )

    def calificar(self, alumno: Alumno, nombre_asignatura, nota) -> int:
        """Se califica la asignatura correspondiente
        :return: id de la asignatura para guardarlo en BD"""
        nombre_asignatura = nombre_asignatura.strip().capitalize()
        lista_asignaturas = alumno.get_asignaturas()
        encontrada = False
        for asignatura in lista_asignaturas:
            if asignatura.get_nombre() == nombre_asignatura:
                encontrada = True
                asignatura.set_nota(nota)
                return asignatura.get_id()
        if not encontrada:
            raise DatoInvalido(
                f"El alumno {alumno.get_dni()!r} no tiene la asignatura {nombre_asignatura!r}"
            )

    def to_dict(self):
        data = super().to_dict()
        data.update({"especialidad": self.especialidad, "salario": self.salario})
        return data


class Administrador(Persona):
    def __init__(
        self,
        id_persona: int,
        dni: str,
        nombre: str,
        email: str,
        rol: str,
        contrasena: str,
    ):
        super().__init__(id_persona, dni, nombre, email, rol, contrasena)

    def __str__(self):
        return f"[ADMIN] {super().__str__()}"
