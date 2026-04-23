class CentroEducativo:
    def __init__(self):
        self._usuarios = []

    def agregar_usuario(self, persona):
        dni_nuevo = persona.get_dni()
        for usuario in self._usuarios:
            if dni_nuevo == usuario.get_dni():
                raise Duplicado(
                    f"{dni_nuevo!r} ya existe en el sistema -> se omite usuario"
                )
        self._usuarios.append(persona)

    def listar_usuarios(self):
        for usuario in self._usuarios:
            print(usuario)

    def obtener_numero_usuarios(self):
        return len(self._usuarios)
