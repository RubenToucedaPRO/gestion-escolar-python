from escuela import (
    DatoInvalido,
    Duplicado,
    Validator,
    Persona,
    Asignatura,
    Alumno,
    Profesor,
    CentroEducativo,
)


def main():
    centro_educativo = CentroEducativo()

    lista_datos = [
        {
            "tipo": "profesor",
            "dni": "12345678P",
            "nombre": "Pepe",
            "email": "pepe@email.com",
            "especialidad": "Informática",
            "salario": 2001.00,
        },
        {
            "tipo": "alumno",
            "dni": "12345679E",
            "nombre": "Eva",
            "email": "eva@email.com",
        },
        {
            "tipo": "alumno",
            "dni": "12345670J",
            "nombre": "José",
            "email": "jose@email.com",
        },
        {
            "tipo": "alumno",
            "dni": "a12345679",
            "nombre": "Malo",
            "email": "malo@email.com",
        },
    ]
    print("=== SISTEMA DE GESTIÓN ESCOLAR — INICIO ===​\n")
    print("Cargando definiciones de usuarios (lista de diccionarios)...")
    try:
        print("Validando e instanciando")
        for dato in lista_datos:
            if dato["tipo"] == "profesor":
                usuario = Profesor(
                    dato["dni"],
                    dato["nombre"],
                    dato["email"],
                    dato["especialidad"],
                    dato["salario"],
                )
            else:
                usuario = Alumno(dato["dni"], dato["nombre"], dato["email"])

            centro_educativo.agregar_usuario(usuario)

    except DatoInvalido as e:
        print(f"ERROR: {e}")

    centro_educativo.listar_usuarios()


if __name__ == "__main__":
    main()
