from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Evento
from .forms import EventoForm
from apps.accounts.decorators import groups_required

def calendar_view(request):
    return render(request, 'events/calendar.html')

def eventos_api(request):
    eventos = Evento.objects.all()
    data = []
    for e in eventos:
        data.append({
            'id': e.id,
            'title': e.titulo,
            'start': e.fecha_inicio.isoformat(),
            'end': e.fecha_fin.isoformat() if e.fecha_fin else e.fecha_inicio.isoformat(),
            'description': e.descripcion,
            'color': '#2563eb' if e.tipo == 'evento' else '#16a34a',
        })
    return JsonResponse(data, safe=False)

@groups_required(['Admin', 'Staff', 'Tech'])
def evento_create(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:calendar_view')
    else:
        form = EventoForm()
    return render(request, 'events/event_form.html', {'form': form})
