from .common import DatoInvalido, Duplicado, BaseDatosError, Validator
from .modelos import Persona, Asignatura, Alumno, Profesor
from .gestion import CentroEducativo
from .registrar import Registrar

__all__ = [
    "DatoInvalido",
    "Duplicado",
    "BaseDatosError",
    "Validator",
    "Persona",
    "Asignatura",
    "Alumno",
    "Profesor",
    "CentroEducativo",
    "Registrar",
]
