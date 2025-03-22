require('dotenv').config();
const jwt = require("jsonwebtoken");

function verificarJWT(req, res, next) {
    const token = req.headers["authorization"];

    if (!token) {
        return res.status(401).json({ error: "Token no proporcionado" });
    }

    const tokenParts = token.split(" ");
    if (tokenParts.length !== 2 || tokenParts[0] !== "Bearer") {
        return res.status(401).json({ error: "Formato de token inválido" });
    }

    jwt.verify(tokenParts[1], "CecarTeAmoMucho", (err, decoded) => {
        if (err) {
            return res.status(401).json({ error: "Token inválido o expirado" });
        }
        req.user = decoded; // Guardar info del usuario autenticado
        next();
    });
}

module.exports = verificarJWT;
