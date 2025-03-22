# Usar PHP con Apache
FROM php:8.2-apache

# Instalar extensiones necesarias para MySQL
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Copiar archivos del proyecto al servidor Apache
COPY src/ /var/www/html/

# Exponer el puerto 80 para acceder al servicio
EXPOSE 80
