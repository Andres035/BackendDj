from django.core.management.base import BaseCommand
import psycopg2
import os

class Command(BaseCommand):
    help = 'Sincroniza las tablas entre base default y réplica'

    def handle(self, *args, **kwargs):
        replica_host = os.getenv('REPLICA_HOST')
        self.stdout.write(f"REPLICA_HOST: {replica_host}")

        conn_default = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', '5432'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        conn_replica = psycopg2.connect(
            host=os.getenv('REPLICA_HOST'),
            port=os.getenv('REPLICA_PORT', '5432'),
            dbname=os.getenv('REPLICA_NAME'),
            user=os.getenv('REPLICA_USER'),
            password=os.getenv('REPLICA_PASSWORD')
        )

        def actualizar_tabla(tabla, claves, columnas, conexion_default, conexion_replica):
            cur_def = conexion_default.cursor()
            cur_rep = conexion_replica.cursor()

            # Poner entre comillas dobles las columnas (Postgres case sensitive)
            columnas_quoted = [f'"{col}"' for col in columnas]
            claves_quoted = [f'"{col}"' for col in claves]

            cur_def.execute(f"SELECT {', '.join(claves_quoted + columnas_quoted)} FROM {tabla}")
            filas = cur_def.fetchall()

            for fila in filas:
                valores_claves = fila[:len(claves)]
                valores_columnas = fila[len(claves):]

                set_str = ", ".join([f'"{col}" = %s' for col in columnas])
                where_str = " AND ".join([f'"{clave}" = %s' for clave in claves])

                cur_rep.execute(
                    f'UPDATE {tabla} SET {set_str} WHERE {where_str}',
                    valores_columnas + valores_claves
                )

            conexion_replica.commit()
            cur_def.close()
            cur_rep.close()

        # Lista con todas las tablas a sincronizar y sus columnas clave y columnas a actualizar
        tablas = [
            {
                'tabla': 'users_roles',  # cambiar a nombre correcto
                'claves': ['id'],
                'columnas': ['nombre_rol', 'estado_Rol']
            },
            {
                'tabla': 'users_permisos',
                'claves': ['id'],
                'columnas': ['nombre_permiso', 'descripcion', 'estado_Permiso']
            },
            {
                'tabla': 'users_usuarios',
                'claves': ['id'],
                'columnas': [
                    'nombre_usuario', 'apellido', 'fecha_nacimiento', 'telefono', 'correo',
                    'password', 'ci', 'ci_departamento', 'fecha_creacion', 'fecha_actualizacion',
                    'estado_Usuario', 'imagen_url'
                ]
            },
            {
                'tabla': 'users_usuariosroles',
                'claves': ['id'],
                'columnas': ['usuario_id', 'rol_id']
            },
            {
                'tabla': 'users_rolespermisos',
                'claves': ['id'],
                'columnas': ['rol_id', 'permiso_id']
            },
            {
                'tabla': 'users_categorias',
                'claves': ['id'],
                'columnas': ['nombre_categoria', 'descripcion', 'estado_categoria']
            },
            {
                'tabla': 'users_productos',
                'claves': ['id'],
                'columnas': [
                    'nombre_producto', 'descripcion', 'precio_compra', 'precio_unitario',
                    'precio_mayor', 'stock', 'categoria_id', 'fecha_creacion',
                    'fecha_actualizacion', 'codigo_producto', 'imagen_productos', 'estado_equipo'
                ]
            },
            {
                'tabla': 'users_ventas',
                'claves': ['id'],
                'columnas': ['usuario_id', 'fecha_venta', 'estado', 'total']
            },
            {
                'tabla': 'users_detallesventas',
                'claves': ['id'],
                'columnas': ['venta_id', 'producto_id', 'cantidad', 'precio', 'subtotal', 'tipo_venta']
            }
        ]

        for t in tablas:
            self.stdout.write(f"Sincronizando tabla {t['tabla']}...")
            actualizar_tabla(
                tabla=t['tabla'],
                claves=t['claves'],
                columnas=t['columnas'],
                conexion_default=conn_default,
                conexion_replica=conn_replica
            )

        self.stdout.write("Sincronización completa para todas las tablas.")
