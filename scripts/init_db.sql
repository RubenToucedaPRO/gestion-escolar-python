-- 1. Desactivar verificacion de la integridad referencial
SET FOREIGN_KEY_CHECKS = 0;

-- 2. Borrar tablas si existen (en orden inverso a la creacion)
DROP TABLE IF EXISTS matriculas;
DROP TABLE IF EXISTS asignaturas;
DROP TABLE IF EXISTS alumnos;
DROP TABLE IF EXISTS profesores;
DROP TABLE IF EXISTS personas;

-- 3. Activar verificacion de la integridad referencial
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE personas (
    id_persona INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(9) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE profesores (
    id_persona INT PRIMARY KEY,
    especialidad VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2),
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona) ON DELETE CASCADE
);

CREATE TABLE alumnos (
    id_persona INT PRIMARY KEY,
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona) ON DELETE CASCADE
);

CREATE TABLE asignaturas (
    id_asignatura INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE matriculas (
    id_alumno INT,
    id_asignatura INT,
    nota DECIMAL(4,2),
    PRIMARY KEY (id_alumno, id_asignatura),
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_persona) ON DELETE CASCADE,
    FOREIGN KEY (id_asignatura) REFERENCES asignaturas(id_asignatura) ON DELETE CASCADE
);

-- INSERCION DE DATOS EN BD

-- 1. INSERTAR ASIGNATURAS
INSERT INTO asignaturas (nombre) VALUES 
('Bases de datos'),
('Python'),
('Mates'),
('Fol'),
('Religion'),
('Android');

-- 2. INSERTAR PROFESORES
-- Jose
INSERT INTO personas (dni, nombre, email) VALUES ('64993018D', 'Jose', 'jose@email.com');
INSERT INTO profesores (id_persona, especialidad, salario) 
VALUES (LAST_INSERT_ID(), 'Bases de datos', 2005.0);

-- Arturo
INSERT INTO personas (dni, nombre, email) VALUES ('05732516L', 'Arturo', 'arturo@email.com');
INSERT INTO profesores (id_persona, especialidad, salario) 
VALUES (LAST_INSERT_ID(), 'Fol', 1900.0);

-- 3. INSERTAR ALUMNOS Y SUS MATRICULAS
-- Jacinto
INSERT INTO personas (dni, nombre, email) VALUES ('33551578Y', 'Jacinto', 'jacinto@email.com');
SET @id_jacinto = LAST_INSERT_ID();
INSERT INTO alumnos (id_persona) VALUES (@id_jacinto);
-- Matrículas de Jacinto
INSERT INTO matriculas (id_alumno, id_asignatura, nota) VALUES 
(@id_jacinto, (SELECT id_asignatura FROM asignaturas WHERE nombre='Bases de datos'), 7.9),
(@id_jacinto, (SELECT id_asignatura FROM asignaturas WHERE nombre='Python'), 0.0),
(@id_jacinto, (SELECT id_asignatura FROM asignaturas WHERE nombre='Android'), 0.0);

-- Leo
INSERT INTO personas (dni, nombre, email) VALUES ('63789776N', 'Leo', 'leo@email.com');
SET @id_leo = LAST_INSERT_ID();
INSERT INTO alumnos (id_persona) VALUES (@id_leo);
-- Matrículas de Leo
INSERT INTO matriculas (id_alumno, id_asignatura, nota) VALUES 
(@id_leo, (SELECT id_asignatura FROM asignaturas WHERE nombre='Mates'), 0.0),
(@id_leo, (SELECT id_asignatura FROM asignaturas WHERE nombre='Python'), 0.0);

-- Alba
INSERT INTO personas (dni, nombre, email) VALUES ('17403564Q', 'Alba', 'alba@email.com');
SET @id_alba = LAST_INSERT_ID();
INSERT INTO alumnos (id_persona) VALUES (@id_alba);
-- Matrículas de Alba
INSERT INTO matriculas (id_alumno, id_asignatura, nota) VALUES 
(@id_alba, (SELECT id_asignatura FROM asignaturas WHERE nombre='Mates'), 0.0),
(@id_alba, (SELECT id_asignatura FROM asignaturas WHERE nombre='Religion'), 0.0);

-- Ana
INSERT INTO personas (dni, nombre, email) VALUES ('85029528T', 'Ana', 'ana@email.com');
INSERT INTO alumnos (id_persona) VALUES (LAST_INSERT_ID());