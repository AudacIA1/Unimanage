from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role in self.allowed_roles

    def handle_no_permission(self):
        return redirect('no_permission')
