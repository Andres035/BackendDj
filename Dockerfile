# Dockerfile  C:\Users\benit\Downloads\Tienda-Online-main\BackendDj\Dockerfile

# Usamos una imagen oficial de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para arrancar Django (en desarrollo)
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]
