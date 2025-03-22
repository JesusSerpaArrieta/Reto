<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

require_once "conexion.php";

// Consulta SQL
$sql = "SELECT id, nombre, descripcion, precio, stock FROM producto";
$result = $conn->query($sql);

$productos = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $productos[] = $row;
    }
}

// Cerrar conexión
$conn->close();

// Devolver respuesta en JSON
echo json_encode($productos);
?>
