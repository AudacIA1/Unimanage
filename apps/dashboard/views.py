from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import UserProfile
from apps.assets.models import AssetCategory, Asset
from apps.loans.models import Loan
from apps.maintenance.models import Maintenance
from apps.events.models import Evento, ChecklistItem, AttendingEntity
from apps.events.forms import EventoForm, ChecklistItemForm
from django.forms import inlineformset_factory
from django.utils import timezone
from django.db.models import Sum, Case, When, IntegerField, Count
from apps.request.models import LoanRequest

@login_required
def dashboard_view(request):
    user = request.user
    # Crear perfil automáticamente si no existe
    from apps.accounts.models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Luego continúa tu lógica:
    if profile.role == "admin":
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
        upcoming_events_list = list(Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio').prefetch_related('checklist_items', 'reserved_assets')[:6])

        nearest_event = upcoming_events_list[0] if upcoming_events_list else None
        other_upcoming_events = upcoming_events_list[1:] if upcoming_events_list else []

        checklist_formset = None
        if nearest_event:
            ChecklistItemFormSet = inlineformset_factory(Evento, ChecklistItem, form=ChecklistItemForm, extra=1, can_delete=True)
            checklist_formset = ChecklistItemFormSet(instance=nearest_event, prefix='checklist')

            if request.method == 'POST':
                if 'checklist_submit' in request.POST:
                    checklist_formset = ChecklistItemFormSet(request.POST, instance=nearest_event, prefix='checklist')
                    if checklist_formset.is_valid():
                        checklist_formset.save()
                        return redirect('dashboard_home')

        recent_requests = LoanRequest.objects.order_by('-request_date')[:5]

        # --- Attending Entity Stats ---
        # Se usa una consulta explícita con Sum y Case para asegurar la precisión del conteo,
        # ya que el método con Count y filter no estaba arrojando el resultado esperado.
        entity_stats = AttendingEntity.objects.annotate(
            visit_count=Sum(
                Case(When(evento__tipo='visita', then=1), default=0, output_field=IntegerField())
            )
        ).values('name', 'visit_count').order_by('-visit_count')

        # --- Datos para Gráficos de Eventos ---
        # 1. Datos para el gráfico de barras (Eventos por Entidad)
        entity_events = list(AttendingEntity.objects.annotate(
            event_count=Count('evento')
        ).values('name', 'event_count').order_by('-event_count'))

        entity_chart_data = {
            'labels': [item['name'] for item in entity_events],
            'data': [item['event_count'] for item in entity_events],
        }

        # 2. Datos para el gráfico circular (Distribución de Tipos de Evento)
        event_types = list(Evento.objects.values('tipo').annotate(
            count=Count('tipo')
        ).order_by('tipo'))
        
        tipo_display_map = dict(Evento.TIPO_CHOICES)
        
        type_chart_data = {
            'labels': [tipo_display_map.get(item['tipo'], item['tipo']) for item in event_types],
            'data': [item['count'] for item in event_types],
        }

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
            "nearest_event": nearest_event,
            "checklist_formset": checklist_formset,
            "other_upcoming_events": other_upcoming_events,
            "recent_requests": recent_requests,
            "entity_stats": entity_stats,
            "entity_chart_data": entity_chart_data,
            "type_chart_data": type_chart_data,
        }
        return render(request, "dashboard/admin_dashboard.html", context)

    elif profile.role == "staff":
        return render(request, "dashboard/staff_dashboard.html")

    else:  # Rol 'user'
        user_loans = Loan.objects.filter(user=request.user)
        user_requests = LoanRequest.objects.filter(user=request.user)
        context = {
            'user_loans': user_loans,
            'user_requests': user_requests,
        }
        return render(request, "dashboard/user_dashboard.html", context)