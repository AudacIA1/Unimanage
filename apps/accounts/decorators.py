from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def role_required(role, redirect_to_login=True):
    def check(u):
        return u.is_authenticated and getattr(u, 'profile', None) and u.profile.role == role
    decorator = user_passes_test(check)
    return decorator

def roles_required(*roles):
    def check(u):
        return u.is_authenticated and getattr(u, 'profile', None) and u.profile.role in roles
    return user_passes_test(check)

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser or request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permisos para ver esta página.")
        return _wrapped
    return decorator

def groups_required(group_names):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser or request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permisos para ver esta página.")
        return _wrapped
    return decorator
