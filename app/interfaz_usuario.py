from escuela.gestion import CentroEducativo
from escuela.modelos import (
    Alumno,
    Profesor,
    Asignatura,
    Duplicado,
    DatoInvalido,
    Validator,
)
from escuela.common import IntegridadDatos
from escuela.registrar import Registrar


class InterfazConsola:
    tarea = ""
    mensaje = ""

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
                self.mensaje = f"ERROR: {e}"
            except IntegridadDatos as e:
                self.mensaje = f"ERROR: {e}"
                print(self.mensaje)
                forzar = input("Si desea forzar salida escriba SI: ").strip()
                if forzar == "SI":
                    salir = True
                    self.mensaje += " - Salida forzada"
            except ValueError as e:
                self.mensaje = f"ERROR: {e}"
            except Exception as e:
                self.mensaje = f"Ocurrió un error inesperado ({type(e).__name__}): {e}"
            finally:
                print(self.mensaje)
                Registrar.registrar_log(self.tarea, self.mensaje)

    def mostrar_bienvenida(self):
        print("\n=== SISTEMA DE GESTIÓN ESCOLAR — INICIO ===​\n")
        print("Bienvenido.")

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
                self.tarea = "Listar usuarios"
                self.mostrar_usuarios()
            case "2":
                self.tarea = "Alta alumno"
                self.dar_alta_alumno()
            case "3":
                self.tarea = "Alta profesor"
                self.dar_alta_profesor()
            case "4":
                self.tarea = "Buscar usuario"
                self.mostrar_datos_usuario()
            case "5":
                self.tarea = "Modificar usuario"
                self.actualizar_datos_usuario()
            case "6":
                self.tarea = "Eliminar usuario"
                self.eliminar_usuario()
            case "7":
                self.tarea = "Matricular alumno"
                self.matricular_usuario()
            case "8":
                self.tarea = "Calificar alumno"
                self.get_datos_calificar_alumno()
            case "9":
                self.tarea = "Salir de la aplicacion"
                return self.guardar_salir_aplicacion()
            case _:
                print("Selección errónea")
        print("*" * 40)
        return False

    def mostrar_usuarios(self):
        print("ALumnos del centro:")
        usuarios = self.sistema.get_usuarios()

        if not usuarios:
            print("Sin usuarios registrados en el centro")
            return

        for usuario in usuarios:
            print(usuario)
        self.mensaje = "Visualizacion exitosa"

    def dar_alta_alumno(self) -> Alumno:
        print("Inicio alta alumno->", end="")
        dni = self.solicitar_dni_usuario()

        self.sistema.verificar_dni_no_registrado(dni)

        nombre = input("Nombre: ")
        email = input("Email: ")
        alumno = Alumno(dni, nombre, email)

        self.sistema.crear_usuario(alumno)

        self.mensaje = f"Alumno con dni {dni!r} dado de alta correctamente"

    def dar_alta_profesor(self) -> Profesor:
        print("Inicio alta profesor->", end="")
        dni = self.solicitar_dni_usuario()
        self.sistema.verificar_dni_no_registrado(dni)
        nombre = input("Nombre: ")
        email = input("Email: ")
        especialidad = input("Especialidad: ")
        salario = input("Salario: ")

        profesor = Profesor(
            dni=dni,
            nombre=nombre,
            email=email,
            especialidad=especialidad,
            salario=salario,
        )
        self.sistema.crear_usuario(profesor)

        self.mensaje = f"Profesor con dni {dni!r} dado de alta correctamente"

    def mostrar_datos_usuario(self):
        print("Inicio mostrar usuario->", end="")
        dni_usuario = self.solicitar_dni_usuario()

        usuario = self.sistema.obtener_usuario(dni_usuario)

        # Comprobamos si es alumno o profesor para mostrar los datos del mismo
        if isinstance(usuario, Alumno):
            self.visualizar_datos_alumno(usuario)
        else:
            self.visualizar_datos_profesor(usuario)

        self.mensaje = f"Mostrar usuario con dni {dni_usuario!r} exitosa"

    def actualizar_datos_usuario(self):
        print("Inicio actualizar usuario->", end="")
        dni_usuario = self.solicitar_dni_usuario()

        usuario = self.sistema.obtener_usuario(dni_usuario)

        print("DNI actual:", dni_usuario)
        dato = input("Escriba DNI nuevo o pulse enter para saltar: ")
        if dato:
            usuario.set_dni(dato)
        dato = input("Escriba nombre nuevo o pulse enter para saltar: ")
        if dato:
            usuario.set_nombre(dato)
        dato = input("Escriba email nuevo o pulse enter para saltar: ")
        if dato:
            usuario.set_email(dato)

        if not isinstance(usuario, Alumno):
            dato = input("Escriba especialidad nuevo o pulse enter para saltar: ")
            if dato:
                usuario.set_especialidad(dato)
            dato = input("Escriba salario nuevo o pulse enter para saltar: ")
            if dato:
                usuario.set_salario(dato)

        self.sistema.guardar_en_memoria_usuarios(usuario)

        self.mensaje = f"Usuario con dni {dni_usuario!r} actualizado correctamente"

    def eliminar_usuario(self):
        print("Inicio eliminar usuario->", end="")
        dni_usuario = self.solicitar_dni_usuario()

        self.sistema.eliminar_usuario(dni_usuario)
        self.mensaje = f"Usuario con dni {dni_usuario!r} eliminado correctamente"

    def matricular_usuario(self):
        print("Inicio matricular alumno->", end="")
        dni_usuario = self.solicitar_dni_usuario()

        usuario = self.sistema.obtener_alumno(dni_usuario)

        nombre_asignatura = input("Asignatura en la que matricular al alumno: ")

        self.sistema.matricular_usuario(usuario, nombre_asignatura)

        self.mensaje = f"Usuario {usuario.get_nombre()!r} matriculado correctamente en {nombre_asignatura!r}"

    def get_datos_calificar_alumno(self):
        print("Inicio calificar alumno->", end="")
        dni_alumno = self.solicitar_dni_usuario()

        alumno = self.sistema.obtener_alumno(dni_alumno)

        self.visualizar_datos_alumno(alumno)

        nombre_asignatura = input("Asignatura a calificar del alumno: ")
        nota = float(input("Nota a asignar: "))

        asignatura = Asignatura(nombre_asignatura, nota)
        self.sistema.calificar_alumno(alumno, asignatura)

        self.mensaje = f"{alumno.get_nombre()!r}: Calificación {asignatura.get_nombre()!r} con la nota {asignatura.get_nota()!r} realizada"

    def guardar_salir_aplicacion(self):
        """
        Guarda los datos en ficheros JSON
        :return: True si la operacion fué realizada con exito
        """
        print("Inicio confirmacion simetría datos entre programa y memoria")
        self.sistema.verificar_datos_en_memoria()
        self.mensaje = "Validacion datos en memoria exitosa"
        return True

    # Metodos auxiliares

    def solicitar_dni_usuario(self):
        dni = input("DNI: ")
        return Validator.validar_dni(dni)

    def visualizar_datos_alumno(self, usuario):
        print(f"Los datos del dni {usuario.get_dni()!r} corresponden al alumno:")
        print("Nombre:", usuario.get_nombre())
        print("Email:", usuario.get_email())
        print("Asignaturas:")
        for asignatura in usuario.get_asignaturas():
            print("\t-", asignatura.get_nombre(), " nota:", asignatura.get_nota())

    def visualizar_datos_profesor(self, usuario):
        print(f"Los datos del dni {usuario.get_dni()!r} corresponden al profesor:")
        print("Nombre:", usuario.get_nombre())
        print("Especialidad:", usuario.get_especialidad())
        print("Salario:", usuario.get_salario())
