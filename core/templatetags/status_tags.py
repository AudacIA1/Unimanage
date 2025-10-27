from django import template

register = template.Library()

@register.filter
def status_to_class(status):
    if status == 'Aprobada':
        return 'approved'
    elif status == 'Pendiente':
        return 'pending'
    elif status == 'Rechazada':
        return 'rejected'
    return ''
