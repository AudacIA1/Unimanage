from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import UserProfile
from apps.assets.models import AssetCategory, Asset
from apps.loans.models import Loan
from apps.maintenance.models import Maintenance
from apps.events.models import Evento, ChecklistItem, AttendingEntity
from apps.events.forms import EventoForm, ChecklistItemForm
from django.forms import inlineformset_factory
from django.utils import timezone # Import timezone
from django.db.models import Sum, Case, When, IntegerField, Count
from django.db.models.functions import TruncMonth
from apps.request.models import LoanRequest
import csv
from django.http import HttpResponse

@login_required
def dashboard_view(request):
    user = request.user
    
    # Determine user role from groups
    is_admin = user.groups.filter(name='Admin').exists()
    is_staff = user.groups.filter(name='Staff').exists()
    is_tech = user.groups.filter(name='Tech').exists()

    # Admin and Staff get the full dashboard
    if is_admin or is_staff:
        # --- 1. Métricas Generales de Activos ---
        total_assets = Asset.objects.count()
        available_assets = Asset.objects.filter(status="disponible").count()
        in_use_assets = Asset.objects.filter(status="en_uso").count()
        maintenance_assets = Asset.objects.filter(status="mantenimiento").count()
        
        total_categories = AssetCategory.objects.count()

        # --- 2. Datos de Distribución por Categoría ---
        categories = AssetCategory.objects.all()
        data_by_category = []
        for category in categories:
            total = Asset.objects.filter(category=category).count()
            disponibles = Asset.objects.filter(category=category, status="disponible").count()
            en_uso = Asset.objects.filter(category=category, status="en_uso").count()
            mantenimiento = Asset.objects.filter(category=category, status="mantenimiento").count()

            if total > 0:
                disponibles_pct = round((disponibles / total) * 100, 2)
                en_uso_pct = round((en_uso / total) * 100, 2)
                mantenimiento_pct = round((mantenimiento / total) * 100, 2)
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
                "disponibles_pct": str(disponibles_pct).replace(',', '.'),
                "en_uso_pct": str(en_uso_pct).replace(',', '.'),
                "mantenimiento_pct": str(mantenimiento_pct).replace(',', '.'),
                "remaining_pct_for_bar": str(remaining_pct_for_bar).replace(',', '.'),
            })

        # --- 3. Últimos Movimientos ---
        last_10_loans = Loan.objects.select_related('asset', 'user').order_by('-loan_date')[:10]
        last_10_maintenances = Maintenance.objects.select_related('asset').order_by('-created_at')[:10]
        
        overdue_loans = [loan for loan in Loan.objects.filter(status='Activo') if loan.is_overdue]

        # --- 4. Datos para Gráficos ---
        asset_status_labels = ["Disponible", "En uso", "En mantenimiento"]
        asset_status_data = [available_assets, in_use_assets, maintenance_assets]

        asset_category_labels = [c['categoria'] for c in data_by_category]
        asset_category_data = [c['total'] for c in data_by_category]
        upcoming_events_list = list(Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by('fecha_inicio').prefetch_related('checklist_items', 'reserved_assets')[:6])

        nearest_event = upcoming_events_list[0] if upcoming_events_list else None
        other_upcoming_events = upcoming_events_list[1:] if upcoming_events_list else []

        checklist_formset = None
        if nearest_event:
            ChecklistItemFormSet = inlineformset_factory(Evento, ChecklistItem, form=ChecklistItemForm, extra=1, can_delete=True)
            checklist_formset = ChecklistItemFormSet(instance=nearest_event, prefix='checklist')

            if request.method == 'POST' and 'checklist_submit' in request.POST:
                checklist_formset = ChecklistItemFormSet(request.POST, instance=nearest_event, prefix='checklist')
                if checklist_formset.is_valid():
                    checklist_formset.save()
                    return redirect('dashboard_home')

        recent_requests = LoanRequest.objects.order_by('-request_date')[:5]

        entity_stats = AttendingEntity.objects.annotate(
            visit_count=Sum(Case(When(evento__tipo='visita', then=1), default=0, output_field=IntegerField()))
        ).values('name', 'visit_count').order_by('-visit_count')

        entity_events = list(AttendingEntity.objects.annotate(event_count=Count('evento')).values('name', 'event_count').order_by('-event_count'))
        entity_chart_data = {'labels': [item['name'] for item in entity_events], 'data': [item['event_count'] for item in entity_events]}

        event_types = list(Evento.objects.values('tipo').annotate(count=Count('tipo')).order_by('tipo'))
        tipo_display_map = dict(Evento.TIPO_CHOICES)
        type_chart_data = {'labels': [tipo_display_map.get(item['tipo'], item['tipo']) for item in event_types], 'data': [item['count'] for item in event_types]}

        # --- New: Total Visits Over Time ---
        visits_over_time = Evento.objects.annotate(month=TruncMonth('fecha_inicio')) \
                                        .values('month') \
                                        .annotate(total_visits=Count('id')) \
                                        .order_by('month')
        
        visits_labels = [item['month'].strftime('%b %Y') for item in visits_over_time]
        visits_data = [item['total_visits'] for item in visits_over_time]
        total_visits_over_time_data = {'labels': visits_labels, 'data': visits_data}

        # --- New: Events per month chart ---
        events_per_month = Evento.objects.annotate(month=TruncMonth('fecha_inicio')) \
                                          .values('month') \
                                          .annotate(count=Count('id')) \
                                          .order_by('month')

        events_per_month_labels = [item['month'].strftime('%b %Y') for item in events_per_month]
        events_per_month_data = [item['count'] for item in events_per_month]
        events_per_month_chart_data = {'labels': events_per_month_labels, 'data': events_per_month_data}

        # --- 5. Datos para Gráficos de Préstamos ---
        loans = Loan.objects.all()
        status_summary = list(loans.values('status').annotate(total=Count('id')))
        user_summary = list(loans.values('user__username').annotate(total=Count('id')))


        context = {
            "data_by_category": data_by_category, "total_assets": total_assets, "available_assets": available_assets,
            "in_use_assets": in_use_assets, "maintenance_assets": maintenance_assets, "total_categories": total_categories,
            "last_10_loans": last_10_loans, "last_10_maintenances": last_10_maintenances, "overdue_loans": overdue_loans,
            "asset_status_labels": asset_status_labels, "asset_status_data": asset_status_data,
            "asset_category_labels": asset_category_labels, "asset_category_data": asset_category_data,
            "nearest_event": nearest_event, "checklist_formset": checklist_formset,
            "other_upcoming_events": other_upcoming_events, "recent_requests": recent_requests,
            "entity_stats": entity_stats, "entity_chart_data": entity_chart_data, "type_chart_data": type_chart_data,
            "total_visits_over_time_data": total_visits_over_time_data, # Add new data to context
            "events_per_month_chart_data": events_per_month_chart_data,
            "status_summary": status_summary,
            "user_summary": user_summary,
            "now": timezone.now(), # Pass timezone.now() to the template context
        }
        return render(request, "dashboard/admin_dashboard.html", context)

    # Techs get a specific, simpler view
    elif is_tech:
        # Reuse the staff_dashboard template and pass tech-specific data
        full_name = user.get_full_name()
        tech_maintenances = Maintenance.objects.filter(performed_by=full_name).order_by('-created_at') if full_name else Maintenance.objects.none()

        context = {
            'last_10_maintenances': tech_maintenances[:10],
            'maintenance_assets': Maintenance.objects.filter(status='En mantenimiento').count(),
            'pending_maintenances': Maintenance.objects.filter(status='Pendiente').count(),
        }
        return render(request, "dashboard/staff_dashboard.html", context)

    # Default is the user dashboard
    else:
        user_loans = Loan.objects.filter(user=user)
        user_requests = LoanRequest.objects.filter(user=user)
        context = {
            'user_loans': user_loans,
            'user_requests': user_requests,
        }
        return render(request, "dashboard/user_dashboard.html", context)

@login_required
def export_report(request):
    user = request.user
    is_admin = user.groups.filter(name='Admin').exists()
    is_staff = user.groups.filter(name='Staff').exists()

    if not is_admin and not is_staff:
        return HttpResponse("Unauthorized", status=401)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_prestamos_vencidos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Activo', 'Usuario', 'Fecha de Vencimiento', 'Días de Retraso'])

    overdue_loans = Loan.objects.filter(status='Activo', due_date__lt=timezone.now())

    for loan in overdue_loans:
        writer.writerow([
            loan.asset.name,
            loan.user.username,
            loan.due_date.strftime('%d/%m/%Y'),
            (timezone.now().date() - loan.due_date.date()).days
        ])

    return response
