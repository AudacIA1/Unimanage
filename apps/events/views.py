from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Evento, AttendingEntity
from .forms import EventoForm, ChecklistItemFormSet, AttendingEntityForm
from apps.accounts.decorators import groups_required

def calendar_view(request):
    events_for_table = Evento.objects.all().select_related('responsable', 'attending_entity')
    context = {
        'events_for_table': events_for_table,
    }
    return render(request, 'events/calendar.html', context)

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


@groups_required(['Admin', 'Staff'])
def attending_entity_list(request):
    entities = AttendingEntity.objects.all()
    return render(request, 'events/attending_entity_list.html', {'entities': entities})

@groups_required(['Admin', 'Staff'])
def attending_entity_create(request):
    if request.method == 'POST':
        form = AttendingEntityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:attending_entity_list')
    else:
        form = AttendingEntityForm()
    return render(request, 'events/attending_entity_form.html', {'form': form})

@groups_required(['Admin', 'Staff'])
def attending_entity_update(request, pk):
    entity = get_object_or_404(AttendingEntity, pk=pk)
    if request.method == 'POST':
        form = AttendingEntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            return redirect('events:attending_entity_list')
    else:
        form = AttendingEntityForm(instance=entity)
    return render(request, 'events/attending_entity_form.html', {'form': form})

@groups_required(['Admin'])
def attending_entity_delete(request, pk):
    entity = get_object_or_404(AttendingEntity, pk=pk)
    if request.method == 'POST':
        entity.delete()
        return redirect('events:attending_entity_list')
    return render(request, 'events/attending_entity_confirm_delete.html', {'entity': entity})
