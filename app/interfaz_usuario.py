from escuela.gestion import CentroEducativo
from escuela.modelos import (
    Alumno,
    Profesor,
    Asignatura,
    Validator,
)


class InterfazConsola:
    def __init__(self):
        self.sistema = CentroEducativo()
        self.tarea = ""  # variable para registrar tarea seleccionada

    def ejecutar(self):
        input("Pulse tecla para mostrar menu\n")
        self.mostrar_menu()
        seleccion = input("Ingrese numero de opción menu a seleccionar: ")
        self.seleccionar_opcion(seleccion)
        return seleccion

    def get_tarea(self):
        return self.tarea

    def set_tarea(self, tarea: str):
        self.tarea = tarea

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
        self.set_tarea("")
        print("*" * 40)
        match seleccion:
            case "1":
                self.set_tarea("Listar usuarios")
                mensaje = self.mostrar_usuarios()
            case "2":
                self.set_tarea("Alta alumno")
                mensaje = self.dar_alta_alumno()
            case "3":
                self.set_tarea("Alta profesor")
                mensaje = self.dar_alta_profesor()
            case "4":
                self.set_tarea("Buscar usuario")
                mensaje = self.mostrar_datos_usuario()
            case "5":
                self.set_tarea("Modificar usuario")
                mensaje = self.actualizar_datos_usuario()
            case "6":
                self.set_tarea("Eliminar usuario")
                mensaje = self.eliminar_usuario()
            case "7":
                self.set_tarea("Matricular alumno")
                mensaje = self.matricular_usuario()
            case "8":
                self.set_tarea("Calificar alumno")
                mensaje = self.get_datos_calificar_alumno()
            case "9":
                self.set_tarea("Salir de la aplicacion")
                mensaje = self.guardar_salir_aplicacion()
            case _:
                print("Selección errónea")
        print(mensaje)
        print("*" * 40)
        self.sistema.registro_historial(self.tarea, mensaje)
        return False

    def mostrar_usuarios(self):
        print("Usuarios del centro:")
        usuarios = self.sistema.get_usuarios()

        if not usuarios:
            print("Sin usuarios registrados en el centro")
            return

        for usuario in usuarios:
            print(usuario)
        return "Visualizacion exitosa"

    def dar_alta_alumno(self) -> Alumno:
        print("Inicio alta alumno->", end="")
        dni = self.solicitar_dni_usuario()

        self.sistema.verificar_dni_no_registrado(dni)

        nombre = input("Nombre: ")
        email = input("Email: ")

        self.sistema.crear_alumno(dni, nombre, email)

        return f"Alumno con dni {dni!r} dado de alta correctamente"

    def dar_alta_profesor(self) -> Profesor:
        print("Inicio alta profesor->", end="")
        dni = self.solicitar_dni_usuario()
        self.sistema.verificar_dni_no_registrado(dni)
        nombre = input("Nombre: ")
        email = input("Email: ")
        especialidad = input("Especialidad: ")
        salario = input("Salario: ")

        self.sistema.crear_profesor(dni, nombre, email, especialidad, salario)

        return f"Profesor con dni {dni!r} dado de alta correctamente"

    def mostrar_datos_usuario(self):
        print("Inicio mostrar usuario->", end="")
        dni_usuario = self.solicitar_dni_usuario()

        usuario = self.sistema.obtener_usuario(dni_usuario)

        # Comprobamos si es alumno o profesor para mostrar los datos del mismo
        if isinstance(usuario, Alumno):
            self.visualizar_datos_alumno(usuario)
        else:
            self.visualizar_datos_profesor(usuario)

        return f"Mostrar usuario con dni {dni_usuario!r} exitosa"

    def actualizar_datos_usuario(self):
        print("Inicio actualizar usuario->", end="")
        dni_usuario = self.solicitar_dni_usuario()

        usuario = self.sistema.obtener_usuario(dni_usuario)

        datos = {}
        print("DNI actual:", dni_usuario)
        dato = input("Escriba DNI nuevo o pulse enter para saltar: ")
        if dato:
            datos["dni"] = dato
        dato = input("Escriba nombre nuevo o pulse enter para saltar: ")
        if dato:
            datos["nombre"] = dato
        dato = input("Escriba email nuevo o pulse enter para saltar: ")
        if dato:
            datos["email"] = dato
        self.sistema.actualizar_persona(usuario, **datos)

        if not isinstance(usuario, Alumno):
            dato = input("Escriba especialidad nuevo o pulse enter para saltar: ")
            if dato:
                datos["especialidad"] = dato
            dato = input("Escriba salario nuevo o pulse enter para saltar: ")
            if dato:
                datos["salario"] = dato
            self.sistema.actualizar_profesor(usuario, **datos)

        return f"Usuario con dni {dni_usuario!r} actualizado correctamente"

    def eliminar_usuario(self):
        print("Inicio eliminar usuario->", end="")
        dni_usuario = self.solicitar_dni_usuario()

        self.sistema.eliminar_usuario(dni_usuario)

        return f"Usuario con dni {dni_usuario!r} eliminado correctamente"

    def matricular_usuario(self):
        print("Inicio matricular alumno->", end="")
        dni_alumno = self.solicitar_dni_usuario()

        alumno = self.sistema.obtener_alumno(dni_alumno)

        nombre_asignatura = input("Asignatura en la que matricular al alumno: ")

        self.sistema.matricular_alumno(alumno, nombre_asignatura)

        return f"Alumno {alumno.get_dni()!r} matriculado correctamente en {nombre_asignatura!r}"

    def get_datos_calificar_alumno(self):
        print("Inicio calificar alumno->", end="")
        dni_alumno = self.solicitar_dni_usuario()

        alumno = self.sistema.obtener_alumno(dni_alumno)

        self.visualizar_datos_alumno(alumno)

        nombre_asignatura = input("Asignatura a calificar del alumno: ")
        nota = float(input("Nota a asignar: "))

        asignatura = Asignatura(nombre_asignatura, nota)
        self.sistema.calificar_alumno(alumno, asignatura)

        return f"{alumno.get_dni()!r}: Calificación {asignatura.get_nombre()!r} con la nota {asignatura.get_nota()!r} realizada"

    def guardar_salir_aplicacion(self):
        """
        Guarda los datos en ficheros JSON
        :return: True si la operacion fué realizada con exito
        """
        print("Confirmacion simetría datos entre programa y memoria")
        self.sistema.verificar_datos_en_memoria()

        return "Verificacion datos memoria y salir de la aplicacion"

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
