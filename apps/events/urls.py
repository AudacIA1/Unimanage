from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('api/', views.eventos_api, name='eventos_api'),
    path('create/', views.evento_create, name='evento_create'),
    path('<int:pk>/update/', views.evento_update, name='evento_update'),
    path('<int:pk>/delete/', views.evento_delete, name='evento_delete'),
    path('<int:pk>/add_attendee/', views.add_attendee, name='add_attendee'),
    path('<int:pk>/remove_attendee/', views.remove_attendee, name='remove_attendee'),
]
