"""
Define las rutas URL para la aplicación de reportes, incluyendo diversas vistas
para generar informes de activos, préstamos, mantenimientos y eventos en
formatos HTML, PDF y Excel.
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report_list'), # Main reports list
    path('asset-usage/', views.asset_usage_report, name='asset_usage_report'),
    path('asset-category/', views.asset_by_category_report, name='asset_by_category_report'),
    path('asset-location/', views.asset_by_location_report, name='asset_by_location_report'),
    path('pdf/general/', views.general_assets_report_pdf, name='general_assets_report_pdf'),
    path('excel/general/', views.general_assets_report_excel, name='general_assets_report_excel'),
    path('loans/pdf/', views.loan_report_pdf, name='loan_report_pdf'),
    path('loans/excel/', views.loan_report_excel, name='loan_report_excel'),
    path('maintenance/', views.maintenance_report_view, name='maintenance_report'),
    path('maintenance/pdf/', views.maintenance_report_pdf, name='maintenance_report_pdf'),
    path('maintenance/excel/', views.maintenance_report_excel, name='maintenance_report_excel'),
    path('events/general/', views.events_general_report, name='events_general_report'),
    path('events/by-date/', views.events_by_date, name='events_by_date'),

    path('events/general/pdf/', views.events_general_report_pdf, name='events_general_report_pdf'),
    path('events/general/excel/', views.events_general_report_excel, name='events_general_report_excel'),
    path('events/by-date/pdf/', views.events_by_date_pdf, name='events_by_date_pdf'),
    path('events/by-date/excel/', views.events_by_date_excel, name='events_by_date_excel'),
]
