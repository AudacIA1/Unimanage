from django.urls import path
from . import views

urlpatterns = [
    path("", views.loan_list, name="loan_list"),
    path("nuevo/", views.loan_create, name="loan_create"),
    path("<int:pk>/editar/", views.loan_edit, name="loan_edit"),
    path("<int:pk>/eliminar/", views.loan_delete, name="loan_delete"),
    path("<int:pk>/devolver/", views.loan_return, name="loan_return"),
]
