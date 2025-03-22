# Usar imagen base de Python
FROM python:3.9

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos y dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer puerto 5000
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "app.py"]
