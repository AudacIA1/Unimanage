from django.shortcuts import render
from apps.assets.models import Asset, AssetCategory # Import AssetCategory
from .forms import AssetUsageFilterForm
from django.db.models import Count, Sum # Sum is still needed for potential future use or other models
from apps.accounts.decorators import group_required, groups_required # For permissions

@group_required('Admin') # Restrict to Admin for now
def asset_usage_report(request):
    form = AssetUsageFilterForm(request.GET or None)
    assets = Asset.objects.all()

    # Apply filters
    if form.is_valid():
        if form.cleaned_data['category']:
            assets = assets.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['location']:
            assets = assets.filter(location=form.cleaned_data['location'])
        
        # Filter by updated_at for date range
        if form.cleaned_data['start_date']:
            assets = assets.filter(updated_at__gte=form.cleaned_data['start_date'])
        if form.cleaned_data['end_date']:
            assets = assets.filter(updated_at__lte=form.cleaned_data['end_date'])

    # Group by status
    summary_data = assets.values('status').annotate(total=Count('id'))
    total_assets_count = assets.count()

    # Calculate percentages
    summary = []
    for row in summary_data:
        percentage = (row['total'] / total_assets_count * 100) if total_assets_count > 0 else 0
        summary.append({
            'status': dict(Asset.STATUS_CHOICES).get(row['status'], row['status']), # Get display name
            'total': row['total'],
            'percentage': round(percentage, 2)
        })

    return render(request, 'reports/asset_usage.html', {
        'form': form,
        'summary': summary,
        'total': total_assets_count,
        'title': 'Reporte de Utilización de Activos'
    })

@group_required('Admin') # Restrict to Admin for now
def asset_by_category_report(request):
    data = (Asset.objects
            .values('category__name')
            .annotate(total=Count('id')) # Removed Sum('value')
            .order_by('category__name'))

    return render(request, 'reports/asset_by_category.html', {
        'data': data,
        'title': 'Reporte de Activos por Categoría'
    })

@group_required('Admin') # Restrict to Admin for now
def asset_by_location_report(request):
    data = (Asset.objects
            .values('location') # Changed to 'location'
            .annotate(total_assets=Count('id')) # Removed Sum('value')
            .order_by('location'))

    return render(request, 'reports/asset_by_location.html', {
        'data': data,
        'title': 'Reporte de Activos por Ubicación'
    })

@group_required('Admin') # Restrict to Admin for now
def report_list(request):
    return render(request, 'reports/report_list.html', {'title': 'Lista de Reportes'})

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

@group_required('Admin') # Restrict to Admin for now
def general_assets_report_pdf(request):
    # Consulta 1: Estado general
    estado_data = Asset.objects.values('status').annotate(total=Count('id'))

    # Consulta 2: Por categoría
    categoria_data = (Asset.objects
                      .values('category__name')
                      .annotate(total=Count('id')) # Removed Sum('value')
                      .order_by('category__name'))

    # Consulta 3: Por ubicación
    ubicacion_data = (Asset.objects
                      .values('location') # Changed to 'location'
                      .annotate(total=Count('id')) # Removed Sum('value')
                      .order_by('location'))

    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_general_activos.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Reporte General de Activos")

    width, height = letter

    # Encabezado
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(150, height - 80, "REPORTE GENERAL DE ACTIVOS")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(450, height - 100, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

    y = height - 140

    # --- Sección 1: Estado General ---
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "1. Resumen por Estado")
    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, y, "Estado")
    pdf.drawString(250, y, "Cantidad")
    pdf.drawString(400, y, "Porcentaje (%)")
    y -= 20
    pdf.setFont("Helvetica", 11)

    total_activos = sum([e['total'] for e in estado_data]) or 1
    for e in estado_data:
        porcentaje = (e['total'] / total_activos) * 100
        pdf.drawString(60, y, dict(Asset.STATUS_CHOICES).get(e['status'], e['status']).capitalize()) # Get display name
        pdf.drawString(250, y, str(e['total']))
        pdf.drawString(400, y, f"{porcentaje:.1f}%")
        y -= 18

    y -= 20

    # --- Sección 2: Distribución por Categoría ---
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "2. Distribución por Categoría")
    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, y, "Categoría")
    pdf.drawString(250, y, "Cantidad")
    # pdf.drawString(400, y, "Valor Total ($)") # Removed as 'value' field does not exist
    y -= 20
    pdf.setFont("Helvetica", 11)

    for c in categoria_data:
        pdf.drawString(60, y, c['category__name'] or "Sin categoría")
        pdf.drawString(250, y, str(c['total']))
        # pdf.drawString(400, y, f"{c['total_value'] or 0:,.2f}") # Removed
        y -= 18
        if y < 100:
            pdf.showPage()
            y = height - 100

    y -= 20

    # --- Sección 3: Distribución por Ubicación ---
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "3. Distribución por Ubicación")
    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, y, "Ubicación")
    pdf.drawString(250, y, "Cantidad")
    # pdf.drawString(400, y, "Valor Total ($)") # Removed
    y -= 20
    pdf.setFont("Helvetica", 11)

    for u in ubicacion_data:
        pdf.drawString(60, y, u['location'] or "Sin ubicación") # Changed to 'location'
        pdf.drawString(250, y, str(u['total']))
        # pdf.drawString(400, y, f"{u['total_value'] or 0:,.2f}") # Removed
        y -= 18
        if y < 100:
            pdf.showPage()
            y = height - 100

    # Pie de página
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.setFillColor(colors.grey)
    pdf.drawString(50, 50, f"Reporte generado automáticamente - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    pdf.save()

    return response
