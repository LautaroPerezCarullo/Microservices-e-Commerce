FROM python:3.10-slim-bullseye

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias y el código de la aplicación
COPY requirements.txt requirements.txt
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para el servidor
EXPOSE 5004

# Comando para ejecutar la aplicación
CMD ["python", "app.py", "--host=0.0.0.0"]