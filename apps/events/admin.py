from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Evento, AttendingEntity

admin.site.register(Evento)
admin.site.register(AttendingEntity, MPTTModelAdmin)
