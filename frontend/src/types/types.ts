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