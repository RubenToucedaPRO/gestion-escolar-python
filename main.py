from app.interfaz_usuario import InterfazConsola
from escuela.modelos import Duplicado, DatoInvalido
from escuela.registrar import Registrar
from escuela.common import IntegridadDatos


def main():
    """Punto de inicio de la aplicación"""
    app = InterfazConsola()
    salir = 0
    app.mostrar_bienvenida()
    # EL while lo saque de interfaz_usuario para en caso de excepciones se mantenga en el bucle
    while salir != "11":
        try:
            salir = app.ejecutar()
        except (Duplicado, DatoInvalido) as e:
            tarea = app.get_tarea()
            mensaje = f"ERROR: {e}"
            print(mensaje)
            # Mantuve aqui los registros de logs para poder saber en que tarea sucedía
            # la excepcion
            Registrar.registrar_log(tarea, mensaje)
        except IntegridadDatos as e:
            tarea = app.get_tarea()
            mensaje = f"ERROR: {e}"
            print(mensaje)
            Registrar.registrar_log(tarea, mensaje)
        except ValueError as e:
            tarea = app.get_tarea()
            mensaje = f"ERROR: {e}"
            print(mensaje)
            Registrar.registrar_log(tarea, mensaje)
        except Exception as e:
            tarea = app.get_tarea()
            mensaje = f"Ocurrió un error inesperado ({type(e).__name__}): {e}"
            print(mensaje)
            Registrar.registrar_log(tarea, mensaje)

if __name__ == "__main__":
    main()
