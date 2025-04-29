// Importar dependencias
import { Router, Request, Response } from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';

// Importar base de datos
import db from '../db';

// Cargar variables de entorno
dotenv.config();

// Definir las variables
const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY as string;

// Crear el router
const router = Router();

/*
    RUTAS
*/

// Inicio de sesión
router.post('/login', async (req: Request, res: Response) => {
    let connection;
    try {
        const { mail, pwd } = req.body;
        connection = await db.promise().getConnection();
        const [result] = await connection.query('SELECT * FROM Usuario WHERE mail_usuario = ?', [mail]);

        // Comprobar si el usuario existe
        if ((result as any[]).length === 0) {
            res.status(404).send('Usuario o contraseña incorrectos');
            return;
        }

        // Definir el usuario
        const user = (result as any[])[0];

        // Comprobar la contraseña
        const match = await bcrypt.compare(pwd, user.PWDHash);
        if (!match) {
            res.status(401).send('Contraseña incorrecta');
            return;
        }

        // Generar el token JWT con expiración de 4 horas
        const token = jwt.sign({ id: user.id_usuario, email: user.mail_usuario }, JWT_SECRET_KEY, { expiresIn: '4h' });
        
        // Obtener la fecha de expiración del token
        const decodedToken = jwt.decode(token) as { exp: number };
        const expDate = new Date(decodedToken.exp * 1000);

        // Enviar la respuesta con el token y la fecha de expiración
        res.status(200).json({ user: { id: user.id_usuario, nombre: user.nombre_usuario, email: user.mail_usuario }, token, expDate });
    } catch (err) {
        console.error('Error al iniciar sesión:', err);
        res.status(500).send('Error interno del servidor');
    } finally {
        // Liberar la conexión a la base de datos
        if (connection) {
            connection.release();
        }
    }
});

// Exportar el router
export default router;