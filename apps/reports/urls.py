from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'), # Main reports list
    path('asset-usage/', views.asset_usage_report, name='asset_usage_report'),
    path('asset-category/', views.asset_by_category_report, name='asset_by_category_report'),
    path('asset-location/', views.asset_by_location_report, name='asset_by_location_report'),
]