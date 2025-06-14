# C:\Users\benit\Downloads\Tienda-Online-main\BackendDj\Dockerfile
FROM python:3.10.4-alpine3.15

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc musl-dev postgresql-dev python3-dev libffi-dev libpq \
    && pip install --upgrade pip

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "entrypoint.sh"]
