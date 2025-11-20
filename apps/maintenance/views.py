from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Maintenance
from .forms import MaintenanceForm
from apps.assets.models import Asset
from apps.accounts.decorators import groups_required

@login_required
def maintenance_list(request):
    """
    Muestra una lista de todas las tareas de mantenimiento, con opciones de filtrado por estado.
    Calcula y muestra métricas generales sobre las tareas.
    """
    all_maintenances = Maintenance.objects.select_related("asset").all()

    # Obtener parámetros de filtrado de la solicitud GET.
    status_query = request.GET.get('status', '')

    # Aplicar filtro de estado si se proporciona.
    if status_query:
        all_maintenances = all_maintenances.filter(status=status_query)

    mantenimientos = all_maintenances

    # Calcular métricas para las tarjetas.
    pendientes = mantenimientos.filter(status="Pendiente").count()
    en_progreso = mantenimientos.filter(status="En proceso").count()
    completados = mantenimientos.filter(status="Finalizado").count()

    context = {
        "mantenimientos": mantenimientos,
        "status_query": status_query,
        "pendientes": pendientes,
        "en_progreso": en_progreso,
        "completados": completados,
        "maintenance_statuses": Maintenance._meta.get_field('status').choices,
    }
    return render(request, "maintenance/maintenance_list.html", context)

@groups_required(['Admin', 'Tech'])
def maintenance_create(request):
    """
    Crea una nueva tarea de mantenimiento y actualiza el estado del activo asociado a 'mantenimiento'.
    """
    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            
            # Actualizar el estado del activo a 'mantenimiento'
            asset = maintenance.asset
            asset.status = 'mantenimiento'
            asset.save()
            
            maintenance.save()
            return redirect("maintenance_list")
    else:
        form = MaintenanceForm()
    return render(request, "maintenance/maintenance_form.html", {"form": form})

@groups_required(['Admin', 'Tech'])
def maintenance_edit(request, pk):
    """
    Edita una tarea de mantenimiento existente. Si el estado cambia a 'Finalizado',
    el activo asociado vuelve a estar 'disponible'.
    """
    maintenance = get_object_or_404(Maintenance, pk=pk)
    original_status = maintenance.status

    if request.method == "POST":
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            updated_maintenance = form.save(commit=False)
            
            # Si el estado de mantenimiento ha cambiado a 'Finalizado'
            if original_status != 'Finalizado' and updated_maintenance.status == 'Finalizado':
                asset = updated_maintenance.asset
                asset.status = 'disponible'
                asset.save()
            
            updated_maintenance.save()
            return redirect("maintenance_list")
    else:
        form = MaintenanceForm(instance=maintenance)
    return render(request, "maintenance/maintenance_form.html", {"form": form})

@groups_required(['Admin', 'Tech'])
def maintenance_delete(request, pk):
    """
    Elimina una tarea de mantenimiento existente. El activo asociado
    vuelve a estar 'disponible'.
    """
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == "POST":
        asset = maintenance.asset
        maintenance.delete()
        
        # El activo vuelve a estar disponible
        asset.status = 'disponible'
        asset.save()
        
        return redirect("maintenance_list")
    return render(request, "maintenance/maintenance_confirm_delete.html", {"mantenimiento": maintenance})
