import mysql from 'mysql2';
import dotenv from 'dotenv';

// Cargar variables de entorno
dotenv.config();

const db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: parseInt(process.env.DB_PORT || '3306'),
    waitForConnections: true,
    connectionLimit: 25,
    queueLimit: 0,
    idleTimeout: 60000
});

export default db;