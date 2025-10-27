from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from apps.accounts.decorators import groups_required
from django.utils.decorators import method_decorator

@method_decorator(groups_required(group_names=['Admin', 'Staff', 'Tech']), name='dispatch')
class ReportListView(TemplateView):
    template_name = 'reports/report_list.html'