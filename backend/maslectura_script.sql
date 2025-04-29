CREATE DATABASE maslectura;

USE maslectura;

CREATE TABLE Usuario (
	id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre_usuario VARCHAR(255) NOT NULL,
    mail_usuario VARCHAR(255) UNIQUE NOT NULL,
    contrasenia VARCHAR(255) NOT NULL, -- HASH
    genero_usuario VARCHAR(50) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL
);

CREATE TABLE Genero (
	id_genero INT PRIMARY KEY AUTO_INCREMENT,
    nombre_genero VARCHAR(255) NOT NULL,
    descripcion VARCHAR(1024) NOT NULL
);

CREATE TABLE Etiqueta (
	id_etiqueta INT PRIMARY KEY AUTO_INCREMENT,
    nombre_etiqueta VARCHAR(255) NOT NULL,
    descripcion VARCHAR(1024) NOT NULL
);

CREATE TABLE Lista (
	id_lista INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    nombre_lista VARCHAR(255) NOT NULL,
    descripcion VARCHAR(1024),
	CONSTRAINT lista_fk FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Libro (
	id_libro INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    fecha_publicacion DATE NOT NULL,
    portada VARCHAR(255),
    promedio DECIMAL(2, 1) NOT NULL, -- maximo 2 digitos de numero, 1 digito decimal
    tipo_libro VARCHAR(255) NOT NULL,
    editorial VARCHAR(255) NOT NULL,
	CONSTRAINT libro_fk FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Comentario (
	id_comentario INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    descripcion VARCHAR(1024),
	CONSTRAINT comentario_fk FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Calificacion_Usuario (
	id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    puntaje INT NOT NULL,
    CONSTRAINT calificacion_usuario_pk PRIMARY KEY (id_usuario, id_libro),
    CONSTRAINT calificacion_usuario_usuario_fk FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    CONSTRAINT calificacion_usuario_libro_fk FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)
);

CREATE TABLE Libro_Lista (
	id_lista INT NOT NULL,
    id_libro INT NOT NULL,
    fecha DATE NOT NULL,
    CONSTRAINT libro_lista_pk PRIMARY KEY (id_lista, id_libro),
    CONSTRAINT libro_lista_lista_fk FOREIGN KEY (id_lista) REFERENCES Lista(id_lista),
    CONSTRAINT libro_lista_libro_fk FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)
);

CREATE TABLE Libro_Genero (
	id_genero INT NOT NULL,
    id_libro INT NOT NULL,
    CONSTRAINT libro_genero_pk PRIMARY KEY (id_genero, id_libro),
    CONSTRAINT libro_genero_genero_fk FOREIGN KEY (id_genero) REFERENCES Genero(id_genero),
    CONSTRAINT libro_genero_libro_fk FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)
);

CREATE TABLE Libro_Etiquetas (
	id_libro INT NOT NULL,
    id_etiquetas INT NOT NULL,
    CONSTRAINT libro_etiquetas_pk PRIMARY KEY (id_libro, id_etiquetas),
    CONSTRAINT libro_etiquetas_libro_fk FOREIGN KEY (id_libro) REFERENCES Libro(id_libro),
    CONSTRAINT libro_etiquetas_etiquetas_fk FOREIGN KEY (id_etiquetas) REFERENCES Etiqueta(id_etiqueta)
);