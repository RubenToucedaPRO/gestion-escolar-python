from escuela.gestion import CentroEducativo
from escuela.modelos import (
    Alumno,
    Profesor,
    Persona,
    Asignatura,
    Duplicado,
    DatoInvalido,
    Validator,
)


class InterfazConsola:
    def __init__(self):
        self.sistema = CentroEducativo()

    def ejecutar(self):
        self.mostrar_bienvenida()
        salir = False
        while not salir:
            try:
                input("Pulse tecla para mostrar menu\n")
                self.mostrar_menu()
                seleccion = input("Ingrese numero de opción menu a seleccionar: ")
                salir = self.seleccionar_opcion(seleccion)
            except (Duplicado, DatoInvalido) as e:
                print(f"ERROR: {e}")
            except Exception as e:
                print(f"Ocurrió un error inesperado ({type(e).__name__}): {e}")

    def mostrar_bienvenida(self):
        print("=== SISTEMA DE GESTIÓN ESCOLAR — INICIO ===​\n")

    def mostrar_menu(self):
        print("1. Listar: Alumnos y Profesores.")
        print("2. Alta de Alumno.")
        print("3. Alta de Profesor.")
        print("4. Buscar: Localizar a un usuario por su DNI.")
        print("5. Modificar un usuario existente.")
        print(
            "6. Eliminar: Dar de baja a un usuario o eliminar una asignatura de un alumno."
        )
        print(
            "7. Matricular Alumno: Busca a un alumno por DNI y le añade una Asignatura."
        )
        print("8. Calificar: Busca un alumno y una asignatura para poner la nota.")
        print("9. Guardar y Salir: Volcará los cambios a los ficheros JSON.")

    def seleccionar_opcion(self, seleccion: str):
        print("*" * 40)
        match seleccion:
            case "1":
                self.sistema.listar_usuarios()
            case "2":
                alumno = self.pedir_datos_alumno()
                self.sistema.crear_usuario(alumno)
            case "3":
                profesor = self.pedir_datos_profesor()
                self.sistema.crear_usuario(profesor)
            case "4":
                dni_usuario = self.pedir_dni()
                usuario = self.sistema.obtener_usuario(dni_usuario)
                self.mostrar_datos_usuario(usuario)
            case "5":
                dni_usuario = self.pedir_dni()
                usuario = self.sistema.obtener_usuario(dni_usuario)
                self.actualizar_datos_usuario(usuario)
            case "6":
                print("")
            case "7":
                dni_usuario = self.pedir_dni()
                usuario = self.sistema.obtener_alumno(dni_usuario)
                nombre_asignatura = input(
                    "Introduzca asignatura en la que matricular al alumno: "
                )
                self.sistema.matricular_usuario(usuario, nombre_asignatura)
            case "8":
                print("")
            case "9":
                print("Cerrando aplicación!")
                return True
            case _:
                print("Selección errónea")
        print("*" * 40)
        return False

    def pedir_datos_alumno(self) -> Alumno:
        """Solicita por teclado los datos para crear un alumno"""
        dni = input("DNI: ")
        nombre = input("Nombre: ")
        email = input("Email: ")

        return Alumno(dni=dni, nombre=nombre, email=email)

    def pedir_datos_profesor(self) -> Profesor:
        """Solicita por teclado los datos para crear un profesor"""
        dni = input("DNI: ")
        nombre = input("Nombre: ")
        email = input("Email: ")
        especialidad = input("Especialidad: ")
        salario = input("Salario: ")
        return Profesor(
            dni=dni,
            nombre=nombre,
            email=email,
            especialidad=especialidad,
            salario=salario,
        )

    def pedir_dni(self):
        dni = input("DNI: ")
        return Validator.validar_dni(dni)

    def mostrar_datos_usuario(self, persona: Persona):
        if isinstance(persona, Alumno):
            print(f"Los datos del dni {persona.get_dni()!r} corresponden al alumno:")
            print("Nombre:", persona.get_nombre())
            print("Asignaturas:")
            for asignatura in persona.get_asignaturas():
                print("\t-", asignatura.get_nombre(), " nota:", asignatura.get_nota())
        else:
            print(f"Los datos del dni {persona.get_dni()!r} corresponden al profesor:")
            print("Nombre:", persona.get_nombre())
            print("Especialidad:", persona.get_especialidad())
            print("Salario:", persona.get_salario())

    def actualizar_datos_usuario(self, persona: Persona):
        print("DNI actual:", persona.get_dni())
        dato = input("Escriba DNI nuevo o pulse enter para saltar: ")
        if dato:
            persona.set_dni(dato)
        dato = input("Escriba nombre nuevo o pulse enter para saltar: ")
        if dato:
            persona.set_nombre(dato)
        dato = input("Escriba email nuevo o pulse enter para saltar: ")
        if dato:
            persona.set_email(dato)
        if not isinstance(persona, Alumno):
            dato = input("Escriba especialidad nuevo o pulse enter para saltar: ")
            if dato:
                persona.set_especialidad(dato)
            dato = input("Escriba salario nuevo o pulse enter para saltar: ")
            if dato:
                persona.set_salario(dato)
        self.sistema.guardar_en_memoria(persona)
