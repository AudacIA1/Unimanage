from django import template

register = template.Library()

@register.simple_tag
def in_group(user, group_name):
    """
    Retorna True si el usuario pertenece al grupo dado.
    Uso en plantillas: {% in_group user "Tech" as is_tech %}
    """
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()
@register.simple_tag
def is_in_groups(user, group_names):
    """
    Retorna True si el usuario pertenece a alguno de los grupos dados.
    Los nombres de los grupos se pasan como un string separado por comas.
    Uso en plantillas: {% is_in_groups user "Admin,Staff" as is_admin_or_staff %}
    """
    if not user or not user.is_authenticated:
        return False
    group_list = [group.strip() for group in group_names.split(',')]
    return user.groups.filter(name__in=group_list).exists()
