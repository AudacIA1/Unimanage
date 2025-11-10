import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 🔑 Cambia estos valores si quieres
username = "Eric"
password = "Eric2004"
email = "eric@gmail.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superusuario creado correctamente")
else:
    print("⚠️ El superusuario ya existe")
