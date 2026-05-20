from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOG_PATH = BASE_DIR.parent / "escuela.log"


class Registrar:
    @staticmethod
    def registrar_log(tarea, resultado):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{fecha}] TAREA: {tarea} | ESTADO: {resultado}\n")
