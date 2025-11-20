from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    """
    Vista para el registro de nuevos usuarios.
    Maneja la creación de cuentas de usuario y redirige al login tras un registro exitoso.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login') # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def no_permission_view(request):
    """
    Vista que se muestra cuando un usuario intenta acceder a una página sin los permisos adecuados.
    """
    return render(request, 'accounts/no_permission.html')