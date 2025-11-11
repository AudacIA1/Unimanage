from django.urls import path
from . import views
from . import autocomplete_views # Import the new autocomplete_views

urlpatterns = [
    path("", views.asset_list, name="asset_list"),
    path("nuevo/", views.asset_create, name="asset_create"),
    path("<int:pk>/editar/", views.asset_edit, name="asset_edit"),
    path("<int:pk>/eliminar/", views.asset_delete, name="asset_delete"),
    path('category-autocomplete/', autocomplete_views.CategoryAutocomplete.as_view(), name='category-autocomplete'), # New autocomplete URL
    path('asset-autocomplete/', autocomplete_views.AssetAutocomplete.as_view(), name='asset-autocomplete'), # Autocomplete for available assets
    path('asset-autocomplete-all/', autocomplete_views.AssetAutocompleteAll.as_view(), name='asset-autocomplete-all'), # Autocomplete for all assets
    path('category/add/', views.asset_category_create_popup, name='asset_category_create_popup'), # New URL for adding category
]
