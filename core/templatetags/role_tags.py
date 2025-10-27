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
