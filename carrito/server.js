const express = require('express');
const carritoRoutes = require('./routes/carrito');
require('dotenv').config();

const app = express();

const cors = require("cors");

// Permitir CORS
app.use(cors());

app.use(express.json());

// Rutas
app.use('/carrito', carritoRoutes);

const PORT = process.env.PORT || 3000; 

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});