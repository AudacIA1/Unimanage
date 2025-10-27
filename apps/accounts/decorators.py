from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def role_required(role, redirect_to_login=True):
    def check(u):
        return u.is_authenticated and getattr(u, 'profile', None) and u.profile.role == role
    decorator = user_passes_test(check)
    return decorator

def roles_required(*roles):
    def check(u):
        return u.is_authenticated and getattr(u, 'profile', None) and u.profile.role in roles
    return user_passes_test(check)
