from .models import Asset

def activos_disponibles(start, end):
    return Asset.objects.exclude(
        events_reserved_for__fecha_inicio__lt=end,
        events_reserved_for__fecha_fin__gt=start,
        events_reserved_for__status__in=['approved','active']
    ).distinct()
