# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connections
from .models import Usuarios

@receiver(post_save, sender=Usuarios)
def replicar_usuario_en_fly(sender, instance, created, **kwargs):
    if created:
        try:
            with connections['replica'].cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users_usuarios (
                        nombre_usuario, apellido, fecha_nacimiento, telefono, correo,
                        password, ci, ci_departamento, fecha_creacion, fecha_actualizacion,
                        estado_Usuario, imagen_url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    instance.nombre_usuario,
                    instance.apellido,
                    instance.fecha_nacimiento,
                    instance.telefono,
                    instance.correo,
                    instance.password,
                    instance.ci,
                    instance.ci_departamento,
                    instance.fecha_creacion,
                    instance.fecha_actualizacion,
                    instance.estado_Usuario,
                    instance.imagen_url
                ])
                print("Replicado en Fly.io correctamente.")
        except Exception as e:
            print("Error replicando a Fly.io:", e)
