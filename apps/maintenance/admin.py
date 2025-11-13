from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("asset__name", "description", "performed_by")