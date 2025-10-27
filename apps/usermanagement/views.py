# usermanagement/views.py
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que restringe el acceso a vistas solo para superusuarios.

    Combina `LoginRequiredMixin` para asegurar que el usuario esté autenticado
    y `UserPassesTestMixin` para verificar si el usuario es un superusuario.
    """
    def test_func(self):
        """Comprueba si el usuario que realiza la solicitud es un superusuario."""
        return self.request.user.is_superuser

class UserOwnerOrAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.pk == self.get_object().pk

class UserListView(SuperuserRequiredMixin, ListView):
    """
    Vista para mostrar una lista de todos los usuarios del sistema.
    
    Solo los superusuarios pueden acceder a esta vista.
    """
    model = User
    template_name = 'usermanagement/user_list.html'
    context_object_name = 'users'

class UserCreateView(SuperuserRequiredMixin, CreateView):
    """
    Vista para que un superusuario pueda crear nuevos usuarios.
    
    Utiliza el formulario `UserCreationForm` de Django.
    """
    model = User
    form_class = UserCreationForm
    template_name = 'usermanagement/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        """Añade un título al contexto de la plantilla."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Nuevo Usuario'
        return context

class UserUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar los datos de un usuario.
    
    Permite a un superusuario modificar los campos principales de un usuario.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']

class UserUpdateView(UserOwnerOrAdminMixin, UpdateView):
    """
    Vista para que un superusuario pueda actualizar un usuario existente.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'usermanagement/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        """Añade un título al contexto de la plantilla."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        return context

class UserDeleteView(SuperuserRequiredMixin, DeleteView):
    """
    Vista para que un superusuario pueda eliminar un usuario.
    
    Muestra una página de confirmación antes de la eliminación.
    """
    model = User
    template_name = 'usermanagement/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
