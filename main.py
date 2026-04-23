from escuela import (
    DatoInvalido,
    Duplicado,
    Validator,
    Persona,
    Asignatura,
    Alumno,
    Profesor,
    CentroEducativo,
)
import random


def main():
    print("=== SISTEMA DE GESTIÓN ESCOLAR — INICIO ===​\n")
    centro_educativo = CentroEducativo()

    cargar_datos(centro_educativo)

    numero_usuarios = centro_educativo.obtener_numero_usuarios()
    print(f"\nRegistro en Centro Educativo completado: {numero_usuarios} usuarios.")

    print("\nListado de todos los usuarios (Polimorfismo):")
    centro_educativo.listar_usuarios()

    print("\nGestión Académica (Matriculación y Calificación):")
    matricular_alumnos(centro_educativo)

    print("\nEstadisticas del centro")
    obtener_estadisticas(centro_educativo)


def cargar_datos(centro_educativo: CentroEducativo):
    lista_datos = [
        {
            "tipo": "profesor",
            "dni": "12345678P",
            "nombre": "pepe",
            "email": "pepe@email.com",
            "especialidad": "Python",
            "salario": 2001.00,
        },
        {
            "tipo": "alumno",
            "dni": "12345679A",
            "nombre": "Javier",
            "email": "javier@email.com",
        },
        {
            "tipo": "alumno",
            "dni": "1234567J",  # dni invalido
            "nombre": "José",
            "email": "jose@email.com",
        },
        {
            "tipo": "alumno",
            "dni": "12345679A",  # dni duplicado
            "nombre": "Maria",
            "email": "maria@email.com",
        },
        {
            "tipo": "alumno",
            "dni": "12345679E",
            "nombre": "eva",
            "email": "eva@email.com",
        },
        {
            "tipo": "profesor",
            "dni": "22223333P",
            "nombre": "Marta",
            "email": "marta@email.com",
            "especialidad": "Bases de datos",
            "salario": 3001.00,
        },
        {
            "tipo": "alumno",
            "dni": "99999999E",
            "nombre": "Ana",
            "email": "ana@email.com",
        },
    ]

    print("Cargando definiciones de usuarios (lista de diccionarios)...")
    print("Validando e instanciando")

    # recorremos la lista de datos y se añaden alumnos y profesores al centro
    for dato in lista_datos:
        try:
            if dato["tipo"] == "profesor":
                usuario = Profesor(
                    dato["dni"],
                    dato["nombre"],
                    dato["email"],
                    dato["especialidad"],
                    dato["salario"],
                )
            else:
                usuario = Alumno(dato["dni"], dato["nombre"], dato["email"])

            centro_educativo.agregar_usuario(usuario)
            print(f"OK: {usuario.get_dni()} {usuario}")

        except (DatoInvalido, Duplicado) as e:
            print(f"ERROR: {e}")


def matricular_alumnos(centro_educativo: CentroEducativo):
    # lista de dnis alumnos, asignaturas y notas
    # hay dni inexistente en centro, asignaturas sin profesor y
    # alumno para matricular dos veces en la misma asignatura
    lista_datos = [
        {
            "dni": "12345678P",
            "asignatura": "python",
            "nota": 9.5,
        },  # alumno inexistente en centro
        {"dni": "12345679E", "asignatura": "python", "nota": 9.5},
        {"dni": "12345679A", "asignatura": "python", "nota": 4.0},
        {
            "dni": "12345679E",
            "asignatura": "Bases de datos",
            "nota": 9.5,
        },
        {"dni": "99999999E", "asignatura": "python", "nota": 19.5},
        {
            "dni": "99999999E",
            "asignatura": "python",
            "nota": 9.5,
        },  # ya matriculado en esta asignatura
        {
            "dni": "19999999E",
            "asignatura": "religion",
            "nota": 9.5,
        },  # no existe profesor de religion
    ]
    # Recorre la lista de datos realizando las matriculaciones en las asignaturas,
    # si la asignatura es valida se llama al metodo calificar alumno
    for dato in lista_datos:
        try:
            dni_alumno = dato["dni"]
            asignatura = Asignatura(dato["asignatura"])
            alumno = centro_educativo.obtener_alumno(dni_alumno)
            alumno.matricular(asignatura)
            print(
                f"{alumno.get_nombre()}: Matriculando en {asignatura.get_nombre()}...OK"
            )
            asignatura.set_nota(dato["nota"])
            calificar_alumno(centro_educativo, alumno, asignatura)

        except (DatoInvalido, Duplicado) as e:
            print(f"ERROR: {e}")


def calificar_alumno(
    centro_educativo: CentroEducativo, alumno: Alumno, asignatura: Asignatura
):
    """Se reciben los datos del alumno si ha sido matriculado y se procede
    a calificarlo"""
    try:
        # Obtenemos el profesor de la asignatura para calificar al alumno
        profesor = centro_educativo.obtener_profesor(asignatura)
        # Calificar el alumno desde el profesor de la asignatura
        profesor.calificar(alumno, asignatura.get_nombre(), asignatura.get_nota())
        print(
            f"{alumno.get_nombre()}: Calificando {asignatura.get_nombre()} con {asignatura.get_nota()}"
        )
    except DatoInvalido as e:
        print(f"ERROR: {e}")


def obtener_estadisticas(centro_educativo: CentroEducativo):
    estadisticas = centro_educativo.obtener_estadisticas()
    for descripcion, dato in estadisticas.items():
        print(f"- {descripcion}: {dato}")


if __name__ == "__main__":
    main()
