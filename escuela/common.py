class DatoInvalido(Exception):
    """Se lanza cuando los datos introducidos no corresponde con formato requerido."""

    pass


class Duplicado(Exception):
    """Se lanza cuando se inserta dato repetido donde no es admisible."""

    pass


class Validator:
    @staticmethod
    def validar_dni(texto: str)->str:
        texto = texto.strip().upper()
        if len(texto) != 9:
            raise DatoInvalido(
                f"DNI {texto!r} invalido - Longitud erronea. Deben ser 8 numeros y una letra -> se omite usuario"
            )
        numero = texto[:8]
        letra = texto[8]
        if not numero.isdigit():
            raise DatoInvalido(
                f"DNI {texto!r} invalido - Los 8 primeros caracteres deben ser numeros entre 0 y 9 -> se omite usuario"
            )
        if not letra.isalpha():
            raise DatoInvalido(
                f"DNI {texto!r} invalido - El ultimo caracter debe ser una letra -> se omite usuario"
            )
        return texto

    @staticmethod
    def formatear_nombre(texto: str):
        return texto.strip().capitalize()
