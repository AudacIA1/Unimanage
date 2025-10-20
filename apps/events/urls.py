from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('api/', views.eventos_api, name='eventos_api'),
    path('create/', views.evento_create, name='evento_create'),
]
