"""
Define las rutas URL para la API del chatbot, incluyendo el endpoint principal
para la interacción y un endpoint para reiniciar la sesión del chatbot.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/reset_chatbot_session/', views.reset_chatbot_session, name='reset_chatbot_session'),
]
