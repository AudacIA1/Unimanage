from dal import autocomplete
from apps.assets.models import AssetCategory, Asset

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results if a query is provided
        if self.q:
            return AssetCategory.objects.filter(name__icontains=self.q)
        return AssetCategory.objects.all()

class AssetAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Asset.objects.filter(status='Disponible')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

    def get_result_label(self, item):
        return f'{item.name} ({item.category.name} - {item.status})'