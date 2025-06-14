from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import Roles, Permisos, Usuarios, UsuariosRoles, RolesPermisos
from datetime import date


class Command(BaseCommand):
    help = 'Inicializa ambas bases de datos con datos básicos'

    def handle(self, *args, **kwargs):
        for db in ['default']:
            self.stdout.write(f"\nInicializando base de datos: {db}...\n")

            # 1. Crear Rol
            admin_role, _ = Roles.objects.using(db).get_or_create(
                nombre_rol="Administrador",
                defaults={'estado_Rol': True}
            )

            # 2. Crear Permisos
            permisos_data = [
                {"nombre_permiso": "registrarUsuarios", "descripcion": "Permite registrar usuarios"},
                {"nombre_permiso": "registrarRoles", "descripcion": "Permite registrar roles"},
                {"nombre_permiso": "registrarPermisos", "descripcion": "a"},
                {"nombre_permiso": "registrarUsuarioRoles", "descripcion": "a"},
                {"nombre_permiso": "registrarRolesPermisos", "descripcion": "a"},
                {"nombre_permiso": "registrarCategorias", "descripcion": "a"},
                {"nombre_permiso": "registrarProductos", "descripcion": "a"},
                {"nombre_permiso": "registrarVenta", "descripcion": "a"},
                {"nombre_permiso": "registrarDetalleVenta", "descripcion": "a"},
                {"nombre_permiso": "registrarVenta-DetalleVenta-Empleado", "descripcion": "a"},
            ]

            permisos_objects = []
            for permiso in permisos_data:
                p, _ = Permisos.objects.using(db).get_or_create(
                    nombre_permiso=permiso["nombre_permiso"],
                    defaults={
                        'descripcion': permiso.get("descripcion", ""),
                        'estado_Permiso': True
                    }
                )
                permisos_objects.append(p)

            # 3. Crear Usuario Admin
            admin_user, created_admin = Usuarios.objects.using(db).get_or_create(
                ci="13247291",
                defaults={
                    'nombre_usuario': "Andres Benito",
                    'apellido': "Yucra",
                    'fecha_nacimiento': date(1998, 11, 6),
                    'telefono': "72937437",
                    'correo': "benitoandrescalle035@gmail.com",
                    'password': make_password("Andres1234*"),
                    'ci_departamento': "LP",
                    'estado_Usuario': True,
                    'imagen_url': "http://res.cloudinary.com/dlrpns8z7/image/upload/v1743595809/fnsesmm80hgwelhyzaie.jpg"
                }
            )

            if created_admin:
                self.stdout.write(f"[{db}] Usuario administrador creado: {admin_user}")

            UsuariosRoles.objects.using(db).get_or_create(
                usuario=admin_user,
                rol=admin_role
            )

            # 4. Crear Segundo Usuario
            segundo_usuario, created_user2 = Usuarios.objects.using(db).get_or_create(
                ci="98765432",
                defaults={
                    'nombre_usuario': "Maria Fernanda",
                    'apellido': "Lopez",
                    'fecha_nacimiento': date(1995, 5, 21),
                    'telefono': "76432109",
                    'correo': "maria.lopez@gmail.com",
                    'password': make_password("Maria1234*"),
                    'ci_departamento': "CB",
                    'estado_Usuario': True,
                    'imagen_url': "http://res.cloudinary.com/demo/image/upload/sample.jpg"
                }
            )

            if created_user2:
                self.stdout.write(f"[{db}] Segundo usuario creado: {segundo_usuario}")

            UsuariosRoles.objects.using(db).get_or_create(
                usuario=segundo_usuario,
                rol=admin_role
            )

            # 5. Asignar Permisos al Rol
            for permiso in permisos_objects:
                RolesPermisos.objects.using(db).get_or_create(
                    rol=admin_role,
                    permiso=permiso
                )

            self.stdout.write(self.style.SUCCESS(f"[{db}] Base de datos inicializada exitosamente con dos usuarios!"))

        """ paso 1 """
        """ python manage.py initialize_db """ 
        """ ejecutar el comando en la terminal """
        """ paso 2 """
        """ python manage.py runserver """
        """ ejecutar el servidor para ver los cambios en la base de datos """