from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from apps.accounts.mixins import RoleRequiredMixin

class ReportListView(RoleRequiredMixin, TemplateView):
    template_name = 'reports/report_list.html'
    allowed_roles = ['admin', 'staff', 'tech']