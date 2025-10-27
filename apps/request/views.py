from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import LoanRequest
from apps.assets.models import Asset
from django.contrib import messages
from apps.accounts.decorators import group_required, groups_required

@login_required
def request_list(request):
    if request.user.is_staff:
        requests = LoanRequest.objects.all().order_by('-request_date')
    else:
        requests = LoanRequest.objects.filter(user=request.user).order_by('-request_date')
    return render(request, 'request/request_list.html', {'requests': requests})

@login_required
def request_detail(request, pk):
    req = get_object_or_404(LoanRequest, pk=pk)
    return render(request, 'request/request_detail.html', {'req': req})

@group_required('User')
def request_create(request):
    assets = Asset.objects.filter(status='disponible') # Filter by lowercase 'disponible'
    if request.method == 'POST':
        asset_id = request.POST.get('asset_id')
        reason = request.POST.get('reason')
        asset = get_object_or_404(Asset, id=asset_id)
        if asset.status != 'disponible':
            messages.error(request, f"""El activo '{asset.name}' no está disponible.""")
            return redirect('request:request_create')
        LoanRequest.objects.create(user=request.user, asset=asset, reason=reason)
        return redirect('request:request_list')
    return render(request, 'request/request_create.html', {'assets': assets})

@groups_required(['Admin', 'Staff'])
def request_approve(request, pk):
    req = get_object_or_404(LoanRequest, pk=pk)
    req.status = 'approved'
    req.reviewed_by = request.user
    req.reviewed_at = timezone.now()
    req.save()
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

def search_assets(request):
    query = request.GET.get('q', '')
    assets = Asset.objects.filter(name__icontains=query)[:10]
    results = [
        {
            'id': a.id,
            'name': a.name,
            'status': a.get_status_display(),
            'category': a.category.name if a.category else '',
            'location': a.location,
        } for a in assets
    ]
    return JsonResponse({'results': results})
