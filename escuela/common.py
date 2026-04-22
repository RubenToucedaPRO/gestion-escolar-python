class DatoInvalido(Exception):
    pass


class Duplicado(Exception):
    pass


class Validator:
    @staticmethod
    def validar_dni(texto: str):
        if len(texto) != 9:
            raise DatoInvalido(
                "Longitud del dni erronea. Deben ser 8 numeros y una letra"
            )
        numero = texto[:8]
        letra = texto[8]
        if not numero.isdigit():
            raise DatoInvalido(
                "Los 8 primeros caracteres deben ser numeros entre 0 y 9"
            )
        if not letra.isalpha():
            raise DatoInvalido("El ultimo caracter debe ser una letra")

    @staticmethod
    def formatear_nombre(texto: str):
        return texto.strip().capitalize()
