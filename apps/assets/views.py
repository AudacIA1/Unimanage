from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import AssetCategory, Asset
from .forms import AssetForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AssetCategoryForm # We will create this form
from django.template.loader import render_to_string
from apps.accounts.decorators import groups_required, group_required

@login_required
def asset_list(request):
    """
    Muestra una lista de todos los activos, con opciones de filtrado.
    Permite filtrar los activos por nombre, categoría, ubicación y estado.
    También calcula y muestra métricas generales sobre los activos filtrados.
    """
    categories = AssetCategory.objects.all()
    all_assets = Asset.objects.select_related("category").all()

    # Obtener parámetros de filtrado de la solicitud GET.
    name_query = request.GET.get('name', '')
    selected_category_id = request.GET.get('category', '')
    location_query = request.GET.get('location', '')
    status_query = request.GET.get('status', '')

    # Aplicar filtros al queryset de activos.
    if name_query:
        all_assets = all_assets.filter(name__icontains=name_query)
    if selected_category_id:
        all_assets = all_assets.filter(category__id=selected_category_id)
    if location_query:
        all_assets = all_assets.filter(location__icontains=location_query)
    if status_query:
        all_assets = all_assets.filter(status=status_query)

    # El queryset filtrado final.
    activos = all_assets

    # Calcular métricas para las tarjetas basadas en el queryset filtrado.
    total_assets = activos.count()
    available_assets = activos.filter(status="disponible").count()
    in_use_assets = activos.filter(status="en_uso").count()
    maintenance_assets = activos.filter(status="mantenimiento").count()

    context = {
        "activos": activos,
        "categories": categories,
        "asset_statuses": Asset._meta.get_field('status').choices,
        "name_query": name_query,
        "selected_category_id": selected_category_id,
        "location_query": location_query,
        "status_query": status_query,
        "total_assets": total_assets,
        "available_assets": available_assets,
        "in_use_assets": in_use_assets,
        "maintenance_assets": maintenance_assets,
    }
    return render(request, "assets/asset_list.html", context)

@groups_required(['Admin', 'Staff'])
def asset_create(request):
    """
    Vista para crear un nuevo activo.
    Muestra un formulario para crear un nuevo activo y procesa la información enviada.
    """
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("asset_list")
    else:
        form = AssetForm()
    return render(request, "assets/asset_form.html", {"form": form, "title": "Crear Activo"})

@groups_required(['Admin', 'Staff', 'Tech'])
def asset_edit(request, pk):
    """
    Vista para editar un activo existente.
    Muestra un formulario pre-rellenado para editar un activo identificado por su clave primaria (pk).
    """
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect("asset_list")
    else:
        form = AssetForm(instance=asset)
    return render(request, "assets/asset_form.html", {"form": form, "title": "Editar Activo"})

@group_required('Admin')
def asset_delete(request, pk):
    """
    Vista para eliminar un activo existente.
    Pide confirmación antes de eliminar un activo identificado por su clave primaria (pk).
    """
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        asset.delete()
        return redirect("asset_list")
    return render(request, "assets/asset_confirm_delete.html", {"asset": asset})

def asset_category_create_popup(request):
    """
    Vista para crear una nueva categoría de activo a través de un popup (AJAX).
    Devuelve la nueva categoría creada o errores de validación en formato JSON.
    """
    if request.method == "POST":
        form = AssetCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse({'id': category.id, 'text': category.name})
        else:
            # If form is not valid, render the form with errors and return as JSON
            return JsonResponse({'error': form.errors.get_json_data(), 'form_html': render_to_string('assets/category_form_inner.html', {'form': form}, request=request)}, status=400)
    else:
        form = AssetCategoryForm()
    # For GET requests, render only the form fields for AJAX loading into modal
    return render(request, 'assets/category_form_inner.html', {'form': form})