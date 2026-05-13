import unittest
from escuela.gestion import CentroEducativo, DatoInvalido, Duplicado


class TestCentroEducativo(unittest.TestCase):
    def setUp(self):
        """Este método se ejecuta antes de cada test."""
        self.centro = CentroEducativo()
        # Borramos usuario con DNI de los test antes de cada test
        # por si en algun test fallido quedó sin borrar
        self.centro.eliminar_usuario("12345678Z")

    def test_crear_alumno_llama_a_db_con_datos_correctos(self):
        """Verifica que crear_alumno procesa bien los datos los guarda en la BD."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni, nombre, email)

        # 2. VERIFICACIÓN REAL: Consultamos a la BD si existe
        existe = self.centro.db.existe_dni_usuario(dni)

        # Comprobamos que se le pasaron los argumentos correctos (convertidos por to_dict)
        self.assertTrue(existe, "El alumno debería haberse guardado en la BD real")

        # Eliminamos el usuario creado en el test
        self.centro.eliminar_usuario(dni)

    def test_crear_alumno_llama_a_db_con_dni_incorrecto(self):
        """Verifica que crear_alumno con DNI no valido provoca la excepcion de DatoInvalido
        y no lo inserta en BD."""

        # 1. DATOS DE PRUEBA
        dni_mal = "12345678"
        nombre = "Test"
        email = "test@correo.com"

        # 2. EJECUCIÓN Y VERIFICACIÓN
        with self.assertRaises(DatoInvalido):
            self.centro.crear_alumno(dni_mal, nombre, email)

        # 3. COMPROBACIÓN EXTRA
        # Verificamos que realmente no existe en la base de datos
        existe = self.centro.db.existe_dni_usuario(dni_mal)
        self.assertFalse(
            existe, "El alumno con DNI erróneo NO debería estar en la base de datos"
        )

    def test_crear_profesor_llama_a_db_con_datos_correctos(self):
        """Verifica que crear_profesor procesa bien los datos los guarda en la BD."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"
        especialidad = "Pythontest"
        salario = "2002.5"

        # 2. EJECUCIÓN
        self.centro.crear_profesor(dni, nombre, email, especialidad, salario)

        # 2. VERIFICACIÓN REAL: Consultamos a la BD si existe
        existe = self.centro.db.existe_dni_usuario(dni)

        # Comprobamos que se creó el profesor
        self.assertTrue(existe, "El profesor existe en la BD real")

        # Eliminamos el usuario creado en el test
        self.centro.eliminar_usuario(dni)

    def test_crear_profesor_llama_a_db_con_salario_incorrecto(self):
        """Verifica que crear_profesor con salario no valido provoca la excepcion de
        DatoInvalido y no lo inserta en BD."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"
        especialidad = "Pythontest"
        salario = "incorrecto"

        # 2. EJECUCIÓN Y VERIFICACIÓN
        with self.assertRaises(DatoInvalido):
            self.centro.crear_profesor(dni, nombre, email, especialidad, salario)

        # 3. COMPROBACIÓN EXTRA
        # Verificamos que realmente no existe en la base de datos
        existe = self.centro.db.existe_dni_usuario(dni)

        self.assertFalse(
            existe, "El profesor con DNI erróneo no debería estar en la base de datos"
        )

    def test_modificar_datos_profesor_llama_a_db_con_datos_correctos(self):
        """Verifica que se modifican los los datos y los guarda en la BD."""

        # 1. DATOS DE PRUEBA PROFESOR A CREAR
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"
        especialidad = "Pythontest"
        salario = "2002.5"

        # DATOS DE PRUEBA QUE MODIFICAREMOS
        email_modificado = "test2@correo.com"
        salario_modificado = 4444.5

        # 2. EJECUCIÓN
        # Creamos el profesor con unos datos iniciales
        self.centro.crear_profesor(dni, nombre, email, especialidad, salario)
        # obtenemos el usuario creado en BD para luego utilizar en la actualizacion
        usuario = self.centro.obtener_usuario(dni)

        # Ejecutamos la actualización
        self.centro.actualizar_persona(usuario, email=email_modificado)
        self.centro.actualizar_profesor(usuario, salario=salario_modificado)

        # 2. VERIFICACIÓN REAL: Consultamos a la BD el usuario modificado
        usuario = self.centro.obtener_usuario(dni)

        # Comprobamos que los datos guardados en BD son los modificados
        self.assertTrue(
            usuario.get_email() == email_modificado,
            "El profesor debería tener el email modificado",
        )
        self.assertTrue(
            usuario.get_salario() == salario_modificado,
            "El profesor debería tener el salario modificado",
        )

        # Eliminamos el usuario creado para el test
        self.centro.eliminar_usuario(dni)

    def test_matricular_alumno_llama_a_db_con_datos_correctos(self):
        """Verifica que se matricula al alumno en la asignatura en la BD."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"
        nombre_asignatura = "Pythontest"

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni, nombre, email)
        usuario = self.centro.obtener_usuario(dni)
        self.centro.matricular_alumno(usuario, nombre_asignatura)

        # 2. VERIFICACIÓN REAL
        usuario = self.centro.obtener_usuario(dni)
        # Comprobamos que se el alumno tiene la asignatura en la que se matriculó
        self.assertTrue(
            usuario.get_asignaturas()[0].get_nombre() == nombre_asignatura,
            "El alumno debería tener la asignatura en la BD real",
        )

        # Eliminamos el usuario creado para el test
        self.centro.eliminar_usuario(dni)

    def test_calificar_alumno_sin_profesor_asignatura_para_calificarlo(self):
        """Verifica que se produce excepcion DatoInvalido al intentar calificar al
        alumno en la asignatura sin tener profesor con la especialidad para dicha
        asignatura."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"
        nombre_asignatura = "Pythontest"
        nota = 9.1

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni, nombre, email)
        usuario = self.centro.obtener_usuario(dni)
        self.centro.matricular_alumno(usuario, nombre_asignatura)

        # 2. EJECUCIÓN Y VERIFICACIÓN:
        # se produce dato invalido al no haber profesor de la asignatura para calificarlo
        with self.assertRaises(DatoInvalido):
            self.centro.calificar_alumno(usuario, nombre_asignatura, nota)

        # Eliminamos el usuario creado para el test
        self.centro.eliminar_usuario(dni)

    def test_calificar_alumno_con_nota_invalida(self):
        """Verifica que se asigna asignatura al alumno en la BD."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"
        nombre_asignatura = "Pythontest"
        nota = "invalida"

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni, nombre, email)
        usuario = self.centro.obtener_usuario(dni)
        self.centro.matricular_alumno(usuario, nombre_asignatura)

        # 2. EJECUCIÓN Y VERIFICACIÓN:
        # se produce dato invalido al no ser una nota valida
        with self.assertRaises(DatoInvalido):
            self.centro.calificar_alumno(usuario, nombre_asignatura, nota)

        # Eliminamos el usuario creado para el test
        self.centro.eliminar_usuario(dni)

    def test_calificar_alumno_llama_a_db_con_datos_correctos(self):
        """Verifica que se califica asignatura al alumno en la BD."""

        # 1. DATOS DE PRUEBA
        dni_alumno = "12345678Z"
        nombre_alumno = "Test"
        email_alumno = "test@correo.com"
        nombre_asignatura = "Pythontest"
        nota = 9.1
        # Datos prueba profesor de la asignatura
        dni_profesor = "12345678X"
        nombre_profesor = "TestProfesor"
        email_profesor = "testprofesor@correo.com"
        especialidad_profesor = "Pythontest"
        salario_profesor = 2002.5

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni_alumno, nombre_alumno, email_alumno)
        self.centro.crear_profesor(
            dni_profesor,
            nombre_profesor,
            email_profesor,
            especialidad_profesor,
            salario_profesor,
        )
        usuario = self.centro.obtener_usuario(dni_alumno)
        self.centro.matricular_alumno(usuario, nombre_asignatura)
        usuario = self.centro.obtener_usuario(dni_alumno)
        self.centro.calificar_alumno(usuario, nombre_asignatura, nota)

        # 2. VERIFICACIÓN REAL
        usuario = self.centro.obtener_usuario(dni_alumno)

        # Comprobamos que se le asignó la nota a la asignatura del alumno
        self.assertTrue(
            usuario.get_asignaturas()[0].get_nota() == nota,
            "El alumno debería tener la nota asignada en la BD real",
        )

        # Eliminamos los usuarios creados para el test
        self.centro.eliminar_usuario(dni_alumno)
        self.centro.eliminar_usuario(dni_profesor)

    def test_verificar_dni_existente_ya_en_bd(self):
        """Verifica dni existente en BD provoca excepcion Duplicado."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni, nombre, email)

        # 3. VERIFICACIÓN
        with self.assertRaises(Duplicado):
            self.centro.verificar_dni_no_registrado(dni)

        # Eliminamos el usuario creado en el test
        self.centro.eliminar_usuario(dni)

    def test_verificar_email_existente_ya_en_bd(self):
        """Verifica email existente en BD provoca excepcion Duplicado."""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni, nombre, email)

        # 3. VERIFICACIÓN
        with self.assertRaises(Duplicado):
            self.centro.verificar_email_no_registrado(email)

        # Eliminamos el usuario creado en el test
        self.centro.eliminar_usuario(dni)

    def test_verificar_consulta_sql_libre(self):
        """Verifica la correcta ejecucion de una consulta SQL libre"""

        # 1. DATOS DE PRUEBA
        dni = "12345678Z"
        nombre = "Test"
        email = "test@correo.com"

        query = f"SELECT * FROM personas WHERE dni='{dni}'"

        # 2. EJECUCIÓN
        self.centro.crear_alumno(dni, nombre, email)

        resultado = self.centro.ejecutar_sql_libre(query)

        # 3. VERIFICACIÓN
        self.assertEqual(
            len(resultado),
            2,
            "Debería haber devuelto exactamente dos registros (titulos columnas y un registro)",
        )
        self.assertEqual(resultado[1][0][1], dni)

        # Eliminamos el usuario creado en el test
        self.centro.eliminar_usuario(dni)

    def test_verificar_delete_sql_libre(self):
        """Verifica la correcta ejecucion de una consulta SQL libre. Dado que en test
        anteriores se creó la asignatura 'Pythontest la eliminamos en este test"""

        # 1. DATOS DE PRUEBA
        nombre_asignatura = "Pythontest"

        query = f"DELETE FROM asignaturas where nombre='{nombre_asignatura}'"

        # 2. EJECUCIÓN
        resultado = self.centro.ejecutar_sql_libre(query)

        # 2. VERIFICACIÓN REAL:
        # Comprobamos respuesta
        self.assertEqual(
            resultado, (None, 1), "La respuesta es sin columnas y 1 registro eliminado"
        )


if __name__ == "__main__":
    unittest.main()
