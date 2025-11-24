from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class AdminOrSuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que restringe el acceso a vistas solo para superusuarios o miembros del grupo Admin.
    """
    def test_func(self):
        """Comprueba si el usuario es superusuario o pertenece al grupo 'Admin'."""
        return self.request.user.is_superuser or self.request.user.groups.filter(name='administrador').exists()

class UserOwnerOrAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que permite el acceso si el usuario es el dueño del objeto, un superusuario o un Admin.
    """
    def test_func(self):
        is_admin_or_superuser = self.request.user.is_superuser or self.request.user.groups.filter(name='administrador').exists()
        is_owner = self.request.user.pk == self.get_object().pk
        return is_admin_or_superuser or is_owner

class UserListView(AdminOrSuperuserRequiredMixin, ListView):
    """
    Vista para mostrar una lista de todos los usuarios del sistema y gestionar sus roles.
    
    Solo los administradores o superusuarios pueden acceder a esta vista.
    """
    model = User
    template_name = 'usermanagement/user_list.html'
    context_object_name = 'users' # Re-adding this

    def get_queryset(self):
        queryset = User.objects.exclude(username='admin').order_by('username')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        users_with_groups = []
        for user in self.object_list:
            users_with_groups.append({
                'user': user,
                'current_group': user.groups.first()
            })
        
        context['users_with_groups'] = users_with_groups
        context['all_groups'] = Group.objects.all()
        context['title'] = 'Gestionar Usuarios y Roles'
        return context

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        
        try:
            user_to_update = User.objects.get(id=user_id)
            
            if user_to_update.is_superuser and user_to_update.username == 'admin':
                 messages.error(request, 'No se puede modificar el rol del superusuario principal.')
                 return redirect('user_list')

            user_to_update.groups.clear()
            if group_id:
                new_group = Group.objects.get(id=group_id)
                user_to_update.groups.add(new_group)
                messages.success(request, f'Rol de {user_to_update.username} actualizado a {new_group.name}.')
            else:
                messages.success(request, f'Se han quitado todos los roles de {user_to_update.username}.')
                
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
        except Group.DoesNotExist:
            messages.error(request, 'El grupo seleccionado no existe.')
            
        return redirect('user_list')

class UserCreateView(AdminOrSuperuserRequiredMixin, CreateView):
    """
    Vista para que un administrador pueda crear nuevos usuarios.
    """
    model = User
    form_class = UserCreationForm
    template_name = 'usermanagement/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Nuevo Usuario'
        return context

class UserUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar los datos de un usuario, incluyendo su rol.
    """
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        empty_label="--- Sin Rol ---",
        label="Rol del Usuario"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'group']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['group'].initial = self.instance.groups.first()

        # Check if the user is an admin/superuser
        is_admin_or_superuser = False
        if request and request.user.is_authenticated:
            is_admin_or_superuser = request.user.is_superuser or request.user.groups.filter(name='administrador').exists()
        
        # If the user is not an admin, remove the fields for role and permissions
        if not is_admin_or_superuser:
            self.fields.pop('group', None)
            self.fields.pop('is_staff', None)
            self.fields.pop('is_superuser', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Only update group if the field was present in the form
            if 'group' in self.cleaned_data:
                if self.cleaned_data['group']:
                    user.groups.set([self.cleaned_data['group']])
                else:
                    user.groups.clear()
        return user

class UserUpdateView(UserOwnerOrAdminMixin, UpdateView):
    """
    Vista para que un administrador pueda actualizar un usuario existente, incluyendo su rol.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'usermanagement/user_form.html'
    # success_url = reverse_lazy('user_list') # Removed static success_url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        return context

    def form_valid(self, form):
        # This check is only relevant if the 'group' field is part of the form,
        # which is only true for admins.
        if 'group' in form.cleaned_data:
            user_to_update = self.get_object()
            # Security check to prevent modification of the main superuser's role
            if user_to_update.is_superuser and user_to_update.username == 'admin':
                if form.cleaned_data['group'] and form.cleaned_data['group'].name != 'administrador':
                    messages.error(self.request, 'No se puede modificar el rol del superusuario principal.')
                    return self.form_invalid(form)
                if not form.cleaned_data['group']:
                    messages.error(self.request, 'No se puede quitar el rol al superusuario principal.')
                    return self.form_invalid(form)

        messages.success(self.request, f'Usuario {self.get_object().username} actualizado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        is_admin_or_superuser = self.request.user.is_superuser or self.request.user.groups.filter(name='administrador').exists()
        
        if is_admin_or_superuser:
            return reverse_lazy('user_list')
        else:
            return reverse_lazy('dashboard_home')

class UserDeleteView(AdminOrSuperuserRequiredMixin, DeleteView):
    """
    Vista para que un administrador pueda eliminar un usuario.
    """
    model = User
    template_name = 'usermanagement/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
