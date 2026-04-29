import json
from pathlib import Path


class GestorFicheros:
    # ATRIBUTOS DE CLASE
    ficheros_abiertos = 0
    operaciones_ficheros = 0

    def __init__(self, ruta: str):
        """Inicialización para un fichero concreto.
        Mantenemos el objeto creado para tratar con un fichero determinado
        Args:
        - ruta: ruta del fichero de estudiantes.json, profesores.json ...
        """
        self._ruta = ruta

    def leer_json(self) -> list:
        """
        Lectura de ficheros JSON (no formatea)
        :param ruta: objeto Path con la ruta del fichero
        :type ruta: Path
        :return: Devuelve un objeto con el contenido del fichero
        :rtype: str
        """
        ruta = Path(self._ruta)

        # Si el fichero no existe, retornamos una lista vacía
        if not ruta.exists():
            return []

        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        lista = list(data)
        return lista

    def guardar_en_json(self, dato: dict) -> None:
        """
        Escritura de ficheros json
        :param ruta: ruta al fichero
        :param contenido: nuevo contenido que va a tener el fichero json"""

        ruta = Path(self._ruta)

        # Si el fichero no existe, creamos una lista vacía
        if not ruta.exists():
            datos = []
        else:
            # Leemos el JSON actual
            with open(ruta, "r", encoding="utf-8") as f:
                try:
                    datos = json.load(f)
                except json.JSONDecodeError:
                    datos = []

        # Añadimos el nuevo libro a la lista
        datos.append(dato)

        # Guardamos de nuevo el fichero
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        print(f"✅ Dato añadido correctamente.")
