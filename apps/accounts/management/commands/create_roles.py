from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class Command(BaseCommand):
    help = "Crea grupos de usuario con permisos básicos."

    def handle(self, *args, **options):
        # Definimos los grupos
        roles = {
            "Administrador": {
                "apps": ["assets", "loans", "maintenance", "events", "reports"],
                "permissions": ["add", "change", "delete", "view"]
            },
            "Técnico": {
                "apps": ["maintenance", "assets"],
                "permissions": ["change", "view"]
            },
            "Administrativo": {
                "apps": ["reports", "assets"],
                "permissions": ["view"]
            },
            "Usuario": {
                "apps": ["loans", "events"],
                "permissions": ["view"]
            },
        }

        for role_name, config in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{role_name}' creado."))

            for app_label in config["apps"]:
                for model in apps.get_app_config(app_label).get_models():
                    content_type = ContentType.objects.get_for_model(model)
                    for perm_type in config["permissions"]:
                        perm_codename = f"{perm_type}_{model._meta.model_name}"
                        try:
                            permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
                            group.permissions.add(permission)
                        except Permission.DoesNotExist:
                            self.stdout.write(f"Permiso {perm_codename} no existe para {app_label}.")

        self.stdout.write(self.style.SUCCESS("✅ Todos los grupos y permisos fueron configurados correctamente."))
