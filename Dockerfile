FROM python:3.10-slim

# Instalar cron, postgresql-client y bash
RUN apt-get update && apt-get install -y cron postgresql-client bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts y crontab
COPY sync_db.sh /app/sync_db.sh
COPY crontab.txt /etc/cron.d/sync_db_cron

# Dar permisos de ejecución al script
RUN chmod +x /app/sync_db.sh

# Aplicar crontab
RUN crontab /etc/cron.d/sync_db_cron

# Crear archivo de log para cron
RUN touch /var/log/sync_db.log

# Copiar el resto del código de Django
COPY . .

# Exponer el puerto para Django
EXPOSE 8000

# Arrancar cron en segundo plano y luego Django con gunicorn
CMD cron && gunicorn main.wsgi:application --bind 0.0.0.0:8000
