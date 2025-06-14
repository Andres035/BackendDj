#!/bin/bash

set -e

echo "Iniciando sincronización de bases de datos..."

# Variables (puedes exportarlas también en .env)
RENDER_HOST=${RENDER_HOST:-dpg-d0mu25umcj7s739lbnkg-a.oregon-postgres.render.com}
RENDER_DB=${RENDER_DB:-themauses}
RENDER_USER=${RENDER_USER:-themauses_user}
RENDER_PASS=${RENDER_PASS:-feVslwNMHceEdHBpUnUsHZhYfbnjb5EM}
RENDER_PORT=${RENDER_PORT:-5432}

RAILWAY_HOST=${RAILWAY_HOST:-metro.proxy.rlwy.net}
RAILWAY_DB=${RAILWAY_DB:-railway}
RAILWAY_USER=${RAILWAY_USER:-postgres}
RAILWAY_PASS=${RAILWAY_PASS:-sLSwHKlamEOIJXoQdVIbHBaNZXpXALww}
RAILWAY_PORT=${RAILWAY_PORT:-29383}

DUMP_FILE="/tmp/dump.sql"

export PGPASSWORD=$RENDER_PASS
echo "Dumping base de datos maestra (Render)..."
pg_dump -h $RENDER_HOST -U $RENDER_USER -p $RENDER_PORT -d $RENDER_DB -f $DUMP_FILE

export PGPASSWORD=$RAILWAY_PASS
echo "Restaurando dump en base réplica (Railway)..."
psql -h $RAILWAY_HOST -U $RAILWAY_USER -p $RAILWAY_PORT -d $RAILWAY_DB -f $DUMP_FILE

echo "Sincronización finalizada."
