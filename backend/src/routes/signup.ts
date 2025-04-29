// Importar dependencias
import { Router, Request, Response } from 'express';
import bcrypt from 'bcrypt';
import dotenv from 'dotenv';

// Importar base de datos
import db from '../db';

// Cargar variables de entorno
dotenv.config();

// Definir las variables
const SALT_ROUNDS = 10;

// Crear el router
const router = Router();

/*
    RUTAS
*/

// Registro de usuario
router.post('/signup', async (req: Request, res: Response) => {
    let connection;
    try {
        const { username, mail, pwd, birthdate, gender } = req.body;
        connection = await db.promise().getConnection();
        
        // Comprobar si el usuario ya existe
        const [existingUser] = await connection.query('SELECT * FROM Usuario WHERE mail_usuario = ?', [mail]);
        if ((existingUser as any[]).length > 0) {
            res.status(409).send('El correo electrónico ya está en uso');
            return;
        }

        // Hashear la contraseña
        const pwdHash = await bcrypt.hash(pwd, SALT_ROUNDS);

        // Insertar el nuevo usuario en la base de datos
        await connection.query('INSERT INTO Usuario (nombre_usuario, mail_usuario, contrasenia, genero_usuario, rol, fecha_nacimiento) VALUES (?, ?, ?, ?, "Usuario", ?)', [username, mail, pwdHash, gender, birthdate]);
        
        // Enviar respuesta de éxito
        res.status(201).send('Usuario registrado con éxito');
    } catch (err) {
        console.error('Error al registrar el usuario:', err);
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