import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.assets.models import Asset
from apps.maintenance.models import Maintenance
from apps.loans.models import Loan # Import Loan model

def sync_asset_statuses():
    """
    Synchronizes the status of all assets based on active loans and maintenance tasks.
    """
    print("Starting asset status synchronization...")

    all_assets = Asset.objects.all()

    for asset in all_assets:
        current_status = asset.status
        new_status = current_status # Assume status remains unchanged unless a rule dictates otherwise

        # Rule 1: Check for active maintenance
        active_maintenance_exists = Maintenance.objects.filter(
            asset=asset,
            status__in=['Pendiente', 'En proceso']
        ).exists()

        # Rule 2: Check for active loans
        active_loan_exists = Loan.objects.filter(
            asset=asset,
            status='Activo'
        ).exists()

        if active_maintenance_exists:
            new_status = 'mantenimiento'
        elif active_loan_exists:
            new_status = 'en_uso'
        else:
            new_status = 'disponible'

        print(f"Asset '{asset.name}' (ID: {asset.id}) status changed from '{current_status}' to '{new_status}'.")
        asset.status = new_status
        asset.save()

    print("Asset status synchronization finished.")

if __name__ == "__main__":
    sync_asset_statuses()