from datetime import datetime


class Registrar:
    @staticmethod
    def registrar_log(tarea, resultado):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("escuela.log", "a", encoding="utf-8") as f:
            f.write(f"[{fecha}] TAREA: {tarea} | ESTADO: {resultado}\n")
