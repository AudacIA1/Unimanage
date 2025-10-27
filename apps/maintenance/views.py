from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Maintenance
from .forms import MaintenanceForm
from apps.assets.models import Asset
from apps.accounts.decorators import groups_required

@login_required
def maintenance_list(request):
    """
    Muestra una lista de todas las tareas de mantenimiento, con opciones de filtrado.

    Permite filtrar las tareas por su estado ('Pendiente', 'En proceso', 'Finalizado').
    También calcula y muestra métricas generales sobre las tareas.
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
    Crea una nueva tarea de mantenimiento.

    Muestra un formulario para crear una nueva tarea y procesa los datos
    enviados.
    """
    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("maintenance_list")
    else:
        form = MaintenanceForm()
    return render(request, "maintenance/maintenance_form.html", {"form": form})

@groups_required(['Admin', 'Tech'])
def maintenance_edit(request, pk):
    """
    Edita una tarea de mantenimiento existente.

    Muestra un formulario pre-rellenado para editar una tarea
    identificada por su clave primaria (pk).
    """
    mantenimiento = get_object_or_404(Maintenance, pk=pk)
    if request.method == "POST":
        form = MaintenanceForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            return redirect("maintenance_list")
    else:
        form = MaintenanceForm(instance=mantenimiento)
    return render(request, "maintenance/maintenance_form.html", {"form": form})

@groups_required(['Admin', 'Tech'])
def maintenance_delete(request, pk):
    """
    Elimina una tarea de mantenimiento existente.

    Pide confirmación antes de eliminar una tarea identificada por su
    clave primaria (pk).
    """
    mantenimiento = get_object_or_404(Maintenance, pk=pk)
    if request.method == "POST":
        mantenimiento.delete()
        return redirect("maintenance_list")
    return render(request, "maintenance/maintenance_confirm_delete.html", {"mantenimiento": mantenimiento})
