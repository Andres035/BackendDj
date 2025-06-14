import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Carga las variables de entorno del .env en la raíz BackendDj
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Conexión base default (origen) desde variables .env
conn_default = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', 5432)),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

# Conexión base réplica (destino) desde variables .env
conn_replica = psycopg2.connect(
    host=os.getenv('REPLICA_HOST'),
    port=int(os.getenv('REPLICA_PORT', 5432)),
    dbname=os.getenv('REPLICA_NAME'),
    user=os.getenv('REPLICA_USER'),
    password=os.getenv('REPLICA_PASSWORD'),
    sslmode='require'  # Si usas ssl como en tu settings Django
)

def actualizar_tabla(tabla, claves, columnas, conn_def, conn_rep):
    cur_def = conn_def.cursor(cursor_factory=RealDictCursor)
    cur_rep = conn_rep.cursor()

    cur_def.execute(f"SELECT {', '.join(claves + columnas)} FROM {tabla}")
    filas = cur_def.fetchall()

    for fila in filas:
        valores_claves = [fila[clave] for clave in claves]
        valores_columnas = [fila[col] for col in columnas]

        set_str = ", ".join([f"{col} = %s" for col in columnas])
        where_str = " AND ".join([f"{clave} = %s" for clave in claves])

        cur_rep.execute(
            f"UPDATE {tabla} SET {set_str} WHERE {where_str}",
            valores_columnas + valores_claves
        )

    conn_rep.commit()
    cur_def.close()
    cur_rep.close()

def main():
    tablas_a_sincronizar = [
        {
            "tabla": "roles",
            "claves": ["id"],
            "columnas": ["nombre_rol", "estado_rol"]
        },
        {
            "tabla": "permisos",
            "claves": ["id"],
            "columnas": ["nombre_permiso", "descripcion", "estado_permiso"]
        },
        {
            "tabla": "usuarios",
            "claves": ["id"],
            "columnas": [
                "nombre_usuario", "apellido", "fecha_nacimiento", "telefono", "correo",
                "password", "ci", "ci_departamento", "fecha_creacion", "fecha_actualizacion",
                "estado_usuario", "imagen_url"
            ]
        },
        {
            "tabla": "usuariosroles",
            "claves": ["id"],
            "columnas": ["usuario_id", "rol_id"]
        },
        {
            "tabla": "rolespermisos",
            "claves": ["id"],
            "columnas": ["rol_id", "permiso_id"]
        },
        {
            "tabla": "categorias",
            "claves": ["id"],
            "columnas": ["nombre_categoria", "descripcion", "estado_categoria"]
        },
        {
            "tabla": "productos",
            "claves": ["id"],
            "columnas": [
                "nombre_producto", "descripcion", "precio_compra", "precio_unitario",
                "precio_mayor", "stock", "categoria_id", "fecha_creacion", "fecha_actualizacion",
                "codigo_producto", "imagen_productos", "estado_equipo"
            ]
        },
        {
            "tabla": "ventas",
            "claves": ["id"],
            "columnas": ["usuario_id", "fecha_venta", "estado", "total"]
        },
        {
            "tabla": "detallesventas",
            "claves": ["id"],
            "columnas": ["venta_id", "producto_id", "cantidad", "precio", "subtotal", "tipo_venta"]
        },
    ]

    for tabla_info in tablas_a_sincronizar:
        print(f"Sincronizando tabla {tabla_info['tabla']}...")
        actualizar_tabla(
            tabla_info["tabla"],
            tabla_info["claves"],
            tabla_info["columnas"],
            conn_default,
            conn_replica
        )
    print("Sincronización completa.")

    conn_default.close()
    conn_replica.close()

if __name__ == "__main__":
    main()
