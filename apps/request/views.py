from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import LoanRequest
from apps.assets.models import Asset
from apps.loans.models import Loan
from django.contrib import messages
from apps.accounts.decorators import group_required, groups_required

@login_required
def request_list(request):
    if request.user.groups.filter(name__in=['Administrador', 'Staff']).exists():
        requests = LoanRequest.objects.all().order_by('-request_date')
    else:
        requests = LoanRequest.objects.filter(user=request.user).order_by('-request_date')
    return render(request, 'request/request_list.html', {'requests': requests})

@login_required
def request_detail(request, pk):
    req = get_object_or_404(LoanRequest, pk=pk)
    return render(request, 'request/request_detail.html', {'req': req})

from django.http import JsonResponse

from datetime import datetime

from django.db import transaction

def request_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Debes iniciar sesión para crear una solicitud.'}, status=401)

    if request.method == 'POST':
        asset_id = request.POST.get('asset_id')
        reason = request.POST.get('reason')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if not all([asset_id, start_date_str, end_date_str]):
            return JsonResponse({'status': 'error', 'message': 'Debes completar todos los campos.'}, status=400)

        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)

        if start_date > end_date:
            return JsonResponse({'status': 'error', 'message': 'La fecha de inicio no puede ser posterior a la fecha de fin.'}, status=400)

        try:
            with transaction.atomic():
                asset = Asset.objects.select_for_update().get(id=asset_id)

                if not asset.is_available(start_date, end_date):
                    return JsonResponse({'status': 'error', 'message': f"El activo '{asset.name}' no está disponible en las fechas seleccionadas."})

                LoanRequest.objects.create(
                    user=request.user, 
                    asset=asset, 
                    reason=reason,
                    start_date=start_date,
                    end_date=end_date
                )
                return JsonResponse({'status': 'success', 'message': 'Tu solicitud de préstamo ha sido enviada con éxito.'})
        except Asset.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'El activo seleccionado no existe.'}, status=404)

    if request.method == 'GET':
        return JsonResponse({}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

from apps.events.models import Evento

@groups_required(['Administrador', 'Staff'])
def request_approve(request, pk):
    req = get_object_or_404(LoanRequest, pk=pk)

    if not req.start_date:
        messages.error(request, f"La solicitud de '{req.user.username}' para '{req.asset.name}' no se puede aprobar porque no tiene fecha de inicio.")
        return redirect('request:request_list')

    req.status = 'approved'
    req.response_date = timezone.now()
    req.save()

    # Cambiar el estado del activo a 'en_uso'
    asset = req.asset
    asset.status = 'en_uso'
    asset.save()

    # Crear el préstamo
    loan = Loan.objects.create(
        asset=req.asset,
        user=req.user,
        status='Activo',
        loan_date=req.start_date,
        return_date=req.end_date
    )

    # Crear el evento para bloquear el activo
    evento = Evento.objects.create(
        titulo=f"Préstamo de {req.asset.name}",
        descripcion=f"Préstamo a {req.user.username}",
        fecha_inicio=req.start_date,
        fecha_fin=req.end_date,
        responsable=req.user,
        status='active',
        tipo='prestamo'
    )
    evento.reserved_assets.add(req.asset)

    messages.success(request, f"La solicitud de '{req.user.username}' para '{req.asset.name}' ha sido aprobada.")
    return redirect('request:request_list')

from django.http import JsonResponse

@groups_required(['Admin', 'Staff'])
def request_reject(request, pk):
    req = get_object_or_404(LoanRequest, pk=pk)
    req.status = 'rejected'
    req.reviewed_by = request.user
    req.reviewed_at = timezone.now()
    req.save()
    return redirect('request:request_list')

from apps.assets.utils import activos_disponibles

@groups_required(['Administrador'])
def request_delete(request, pk):
    req = get_object_or_404(LoanRequest, pk=pk)
    req.delete()
    messages.success(request, f"La solicitud de '{req.user.username}' para '{req.asset.name}' ha sido borrada.")
    return redirect('request:request_list')

def search_assets(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        return JsonResponse({'results': []})

    assets = activos_disponibles(start_date, end_date).filter(name__icontains=query)[:10]

    results = [
        {
            'id': a.id,
            'name': a.name,
            'category': a.category.name if a.category else '',
            'location': a.location,
            'status': a.status,
        } for a in assets
    ]
    return JsonResponse({'results': results})
