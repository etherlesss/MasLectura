export interface User {
    id_usuario: number;
    nombre_usuario: string;
    mail_usuario: string;
    genero_usuario: string;
    rol: string;
    fecha_nacimiento: string;
}

export interface List {
    id_lista: number;
    id_usuario: number;
    nombre_lista: string;
    descripcion: string;
}

export interface Book {
    id_libro: number;
    id_usuario: number;
    titulo: string;
    autor: string;
    artista: string;
    anio_publicacion: string;
    portada: string;
    estado: string;
    link_compra: string;
    promedio: number;
    tipo: string;
    editorial: string;
    idioma: string;
    es_saga: string;
    titulo_saga: string;
    num_libro: number;
    num_capitulos: number;
    sinopsis: string;
    fecha: string; // Este viene en conjunto al hacer inner join con la tabla libro_lista
}

export interface Tag {
    id_etiqueta: number;
    nombre: string;
    descripcion: string;
}

export interface Genre {
    id_genero: number;
    nombre: string;
    descripcion: string;
}