from django import template

register = template.Library()

@register.filter
def status_to_class(status):
    if status == 'Aprobada':
        return 'font-bold text-green-600 dark:text-green-400'
    elif status == 'Pendiente':
        return 'font-bold text-yellow-600 dark:text-yellow-400'
    elif status == 'Rechazada':
        return 'font-bold text-red-600 dark:text-red-400'
    return ''
