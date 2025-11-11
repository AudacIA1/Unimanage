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
