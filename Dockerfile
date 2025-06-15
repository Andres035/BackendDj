
# BackendDj/Dockerfile
# Usamos una imagen base oficial de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copiamos el archivo de dependencias y las instalamos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación al contenedor
COPY . /app/

# Establecemos las variables de entorno para Django
ENV PYTHONUNBUFFERED 1

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]
