const express = require('express');
const router = express.Router();
const db = require('../db');
const verificarJWT = require('../middlewares/auth'); // Middleware de autenticación

// Agregar producto al carrito (protegido con JWT)
router.post('/agregar', verificarJWT, async (req, res) => {
    const { producto_id, cantidad } = req.body;
    const { id: usuario_id, tipoId: usuario_tipoId } = req.user; // Obtener datos del usuario autenticado

    if (!producto_id || !cantidad || cantidad <= 0) {
        return res.status(400).json({ error: 'producto_id y cantidad válida son obligatorios' });
    }

    try {
        // Verificar si el producto existe y hay stock disponible
        const [producto] = await db.query(
            'SELECT stock FROM producto WHERE id = ? AND stock >= ?',
            [producto_id, cantidad]
        );

        if (!producto || producto.length === 0) {
            return res.status(404).json({ error: 'Producto no disponible o sin stock suficiente' });
        }

        // Insertar o actualizar cantidad en el carrito
        await db.query(
            `INSERT INTO carrito (usuario_id, usuario_tipoId, producto_id, cantidad)
             VALUES (?, ?, ?, ?)
             ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)`,
            [usuario_id, usuario_tipoId, producto_id, cantidad]
        );

        res.status(201).json({ message: 'Producto agregado al carrito correctamente' });
    } catch (error) {
        console.error('Error al agregar producto al carrito:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Eliminar producto del carrito (protegido con JWT)
router.post('/eliminar', verificarJWT, async (req, res) => {
    const { producto_id } = req.body; // Recibir producto_id desde el cuerpo de la solicitud
    const { id: usuario_id, tipoId: usuario_tipoId } = req.user; // Obtener datos del usuario autenticado

    if (!producto_id) {
        return res.status(400).json({ error: 'producto_id es obligatorio' });
    }

    try {
        // Verificar si el producto existe en el carrito del usuario
        const [carritoItem] = await db.query(
            'SELECT 1 FROM carrito WHERE usuario_id = ? AND usuario_tipoId = ? AND producto_id = ?',
            [usuario_id, usuario_tipoId, producto_id]
        );

        if (carritoItem.length === 0) {
            return res.status(404).json({ error: 'Producto no encontrado en el carrito' });
        }

        // Eliminar el producto del carrito
        await db.query(
            'DELETE FROM carrito WHERE usuario_id = ? AND usuario_tipoId = ? AND producto_id = ?',
            [usuario_id, usuario_tipoId, producto_id]
        );

        res.status(200).json({ message: 'Producto eliminado del carrito correctamente' });
    } catch (error) {
        console.error('Error al eliminar producto del carrito:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Listar productos en el carrito del usuario autenticado
router.get('/listar', verificarJWT, async (req, res) => {
    console.log("Usuario autenticado:", req.user);
    
    const { id: usuario_id, tipoId: usuario_tipoId } = req.user;

    if (!usuario_id || !usuario_tipoId) {
        return res.status(400).json({ error: 'Datos de usuario inválidos' });
    }

    try {
        const [productos] = await db.query(
            `SELECT p.id, p.nombre, p.precio, c.cantidad, p.stock
            FROM carrito c
            JOIN producto p ON c.producto_id = p.id
            WHERE c.usuario_id = ? AND c.usuario_tipoId = ?`,
            [usuario_id, usuario_tipoId]
        );

        console.log("Productos encontrados:", productos);

        res.json({ productos });
    } catch (error) {
        console.error('Error al listar productos en el carrito:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});


module.exports = router;
