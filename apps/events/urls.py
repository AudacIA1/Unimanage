"""
Define las rutas URL para la aplicación de eventos, incluyendo la vista de calendario,
endpoints de API para eventos, y operaciones CRUD para eventos y entidades asistentes.
"""
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('api/', views.eventos_api, name='eventos_api'),
    path('create/', views.evento_create, name='evento_create'),
    path('<int:pk>/update/', views.evento_update, name='evento_update'),
    path('<int:pk>/delete/', views.evento_delete, name='evento_delete'),


    path('attending-entities/', views.attending_entity_list, name='attending_entity_list'),
    path('attending-entities/create/', views.attending_entity_create, name='attending_entity_create'),
    path('attending-entities/<int:pk>/update/', views.attending_entity_update, name='attending_entity_update'),
    path('attending-entities/<int:pk>/delete/', views.attending_entity_delete, name='attending_entity_delete'),
]
