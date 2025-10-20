from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.assets.models import AssetCategory, Asset
from apps.loans.models import Loan
from apps.maintenance.models import Maintenance
from apps.events.models import Evento
from django.utils import timezone

@login_required
def dashboard(request):
    """
    Muestra el panel de control principal (página de 'Inicio').

    Esta vista recopila una variedad de estadísticas sobre los activos,
    préstamos y mantenimientos para mostrarlas en el dashboard.
    Solo los usuarios autenticados pueden acceder a esta página.

    Args:
        request: El objeto HttpRequest.

    Returns:
        HttpResponse: La plantilla del dashboard renderizada con los datos de contexto.
    """
    # --- 1. Métricas Generales de Activos ---
    # Se cuentan los activos totales y por cada estado principal.
    total_assets = Asset.objects.count()
    available_assets = Asset.objects.filter(status="Disponible").count()
    in_use_assets = Asset.objects.filter(status="En uso").count()
    maintenance_assets = Asset.objects.filter(status="En mantenimiento").count()
    total_categories = AssetCategory.objects.count()

    # --- 2. Datos de Distribución por Categoría ---
    # Se itera sobre cada categoría para calcular sus estadísticas específicas.
    categories = AssetCategory.objects.all()
    data_by_category = []
    for category in categories:
        total = Asset.objects.filter(category=category).count()
        disponibles = Asset.objects.filter(category=category, status="Disponible").count()
        en_uso = Asset.objects.filter(category=category, status="En uso").count()
        mantenimiento = Asset.objects.filter(category=category, status="En mantenimiento").count()

        if total > 0:
            disponibles_pct = round((disponibles / total) * 100, 2)
            en_uso_pct = round((en_uso / total) * 100, 2)
            mantenimiento_pct = round((mantenimiento / total) * 100, 2)
            # Se calcula un porcentaje restante para asegurar que la barra de progreso sume 100%,
            # compensando posibles errores de redondeo.
            remaining_pct_for_bar = round(100 - (disponibles_pct + en_uso_pct + mantenimiento_pct), 2)
            if remaining_pct_for_bar < 0:
                remaining_pct_for_bar = 0
        else:
            disponibles_pct, en_uso_pct, mantenimiento_pct, remaining_pct_for_bar = 0, 0, 0, 0

        data_by_category.append({
            "categoria": category.name,
            "total": total,
            "disponibles": disponibles,
            "en_uso": en_uso,
            "mantenimiento": mantenimiento,
            # Se convierten a string con punto para asegurar compatibilidad con CSS.
            "disponibles_pct": str(disponibles_pct).replace(',', '.'),
            "en_uso_pct": str(en_uso_pct).replace(',', '.'),
            "mantenimiento_pct": str(mantenimiento_pct).replace(',', '.'),
            "remaining_pct_for_bar": str(remaining_pct_for_bar).replace(',', '.'),
        })

    # --- 3. Últimos Movimientos ---
    # Se obtienen los 10 préstamos y mantenimientos más recientes.
    last_10_loans = Loan.objects.select_related('asset', 'user').order_by('-loan_date')[:10]
    last_10_maintenances = Maintenance.objects.select_related('asset').order_by('-created_at')[:10]

    # --- 4. Datos para Gráficos ---
    # Se preparan los datos para el gráfico de distribución de estados de activos.
    asset_status_labels = ["Disponible", "En uso", "En mantenimiento"]
    asset_status_data = [available_assets, in_use_assets, maintenance_assets]

    # Se preparan los datos para el gráfico de activos por categoría.
    asset_category_labels = [c['categoria'] for c in data_by_category]
    asset_category_data = [c['total'] for c in data_by_category]
    upcoming_events=Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio')[:5]

    # --- 5. Contexto para la Plantilla ---
    context = {
        "data_by_category": data_by_category,
        "total_assets": total_assets,
        "available_assets": available_assets,
        "in_use_assets": in_use_assets,
        "maintenance_assets": maintenance_assets,
        "total_categories": total_categories,
        "last_10_loans": last_10_loans,
        "last_10_maintenances": last_10_maintenances,
        "asset_status_labels": asset_status_labels,
        "asset_status_data": asset_status_data,
        "asset_category_labels": asset_category_labels,
        "asset_category_data": asset_category_data,
        "upcoming_events":upcoming_events
    }

    return render(request, "dashboard.html", context)
