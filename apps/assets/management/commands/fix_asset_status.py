from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.loans.models import Loan

class Command(BaseCommand):
    help = '''Recalculates and corrects the status of all assets based on active loans.'''

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting asset status recalculation...'))

        assets_in_use = Asset.objects.filter(status='en_uso')
        updated_count = 0

        for asset in assets_in_use:
            active_loans = Loan.objects.filter(asset=asset, status='Activo').exists()
            if not active_loans:
                asset.status = 'disponible'
                asset.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"  - Asset '{asset.name}' status updated to \"disponible\"."))

        self.stdout.write(self.style.SUCCESS(f'Recalculation complete. {updated_count} assets updated.'))
