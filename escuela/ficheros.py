import json
from pathlib import Path
from .registrar import Registrar


class GestorFicheros:
    def __init__(self, ruta: str):
        """Inicialización para un fichero concreto.
        Mantenemos el objeto creado para tratar con un fichero determinado
        Args:
        - ruta: ruta del fichero de alumnos.json, profesores.json ...
        """
        self._ruta = ruta

    def get_ruta(self):
        return self._ruta

    def get_fichero(self):
        return self.get_ruta().split("/")[-1]

    def leer_json(self) -> list:
        """
        Lectura de ficheros JSON (no formatea)
        :return: Devuelve un objeto con el contenido del fichero
        """
        ruta = Path(self._ruta)

        # Si el fichero no existe, retornamos una lista vacía
        if not ruta.exists():
            return []

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            lista = list(data)
            return lista
        except Exception:
            # captura excepcion en arranque de programa
            mensaje = (
                f"ERROR: El fichero {self.get_fichero()} tiene un formato corrupto."
            )
            print(mensaje)
            Registrar.registrar_log("Lectura json", mensaje)
            return []

    def guardar_en_json(self, lista: list) -> None:
        """
        Escritura de ficheros json
        :param lista: nuevo contenido que va a tener el fichero json"""

        ruta = Path(self._ruta)

        # Creamos la carpeta 'datos' si no existe
        ruta.parent.mkdir(parents=True, exist_ok=True)

        # Guardamos de nuevo el fichero
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON {self.get_fichero()!r} actualizado correctamente.")
