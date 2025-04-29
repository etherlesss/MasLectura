// Importar dependencias
import express, { Request, Response } from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
// import mysql from 'mysql2';
// import jwt from 'jsonwebtoken';
// import bcrypt from 'bcrypt';

// Importar base de datos
import db from './db';

// Importar rutas
import login from './routes/login';

// Cargar variables de entorno
dotenv.config();

// Definir las variables
const PORT = process.env.PORT || 3000;
// const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY;
// const SALT_ROUNDS = process.env.SALT_ROUNDS;

// Crear la aplicación Express
const app = express();

// Configurar CORS
const corsConfig = {
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'] // PUT para caso que se tenga que editar todo, PATCH para editar solo un(os) campo(s)
}

// Habilitar CORS
app.use(cors(corsConfig));

// Habilitar JSON
app.use(express.json());

// Probar la conexión a MySQL
db.getConnection((err, connection) => {
    if (err) {
        console.error('Error al conectar a MySQL:', err);
        return;
    }
    console.log('Conexión a MySQL exitosa');
    connection.release();
});

// Mensaje de encendido del servidor backend
app.listen(PORT, () => {
    console.log(`Servidor iniciado en http://127.0.0.1:${PORT}`);
});

// Rutas de la API
app.use('/api', login);