from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Evento
from .forms import EventoForm, ChecklistItemFormSet # Importar ChecklistItemFormSet
from apps.accounts.decorators import groups_required

def calendar_view(request):
    return render(request, 'events/calendar.html')

def eventos_api(request):
    eventos = Evento.objects.exclude(tipo='prestamo')
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
            evento = form.save(commit=False)
            evento.save()
            form.save_m2m() # Guarda los ManyToMany fields como reserved_assets

            formset = ChecklistItemFormSet(request.POST, instance=evento, prefix='checklist_items')
            if formset.is_valid():
                formset.save()
                return redirect('events:calendar_view')
            else:
                # Si el formset no es válido, renderiza el formulario con errores del formset
                return render(request, 'events/event_form.html', {'form': form, 'formset': formset})
        else:
            # Si el formulario principal no es válido, renderiza el formulario con errores
            formset = ChecklistItemFormSet(request.POST, prefix='checklist_items') # No instance for new event
            return render(request, 'events/event_form.html', {'form': form, 'formset': formset})
    else:
        form = EventoForm()
        formset = ChecklistItemFormSet(prefix='checklist_items') # No instance for new event
    return render(request, 'events/event_form.html', {'form': form, 'formset': formset})

from django.contrib import messages

@groups_required(['Admin', 'Staff', 'Tech'])
def evento_update(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        formset = ChecklistItemFormSet(request.POST, instance=evento, prefix='checklist_items')
        if form.is_valid() and formset.is_valid():
            evento = form.save(commit=False)
            evento.save()
            form.save_m2m() # Guarda los ManyToMany fields como reserved_assets
            formset.save()
            return redirect('events:calendar_view')
        else:
            return render(request, 'events/event_form.html', {'form': form, 'formset': formset, 'evento': evento})
    else:
        form = EventoForm(instance=evento)
        formset = ChecklistItemFormSet(instance=evento, prefix='checklist_items')
    return render(request, 'events/event_form.html', {'form': form, 'formset': formset, 'evento': evento})

@groups_required(['Administrador'])

def evento_delete(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    evento.delete()
    messages.success(request, f"El evento '{evento.titulo}' ha sido eliminado.")
    return redirect('events:calendar_view')

@groups_required(['Administrador'])
def add_attendee(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if evento.max_attendees is None or evento.current_attendees < evento.max_attendees:
        evento.current_attendees += 1
        evento.save()
    return redirect('events:evento_update', pk=pk)

@groups_required(['Administrador'])
def remove_attendee(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if evento.current_attendees > 0:
        evento.current_attendees -= 1
        evento.save()
    return redirect('events:evento_update', pk=pk)
