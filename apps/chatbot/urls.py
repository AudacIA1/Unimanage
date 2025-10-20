from django.urls import path
from . import views

urlpatterns = [
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/reset_chatbot_session/', views.reset_chatbot_session, name='reset_chatbot_session'),
]
