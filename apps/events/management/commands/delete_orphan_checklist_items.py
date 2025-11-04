from django.core.management.base import BaseCommand
from apps.events.models import ChecklistItem

class Command(BaseCommand):
    help = 'Deletes all checklist items that are not associated with any event.'

    def handle(self, *args, **options):
        orphan_items = ChecklistItem.objects.filter(event__isnull=True)
        count = orphan_items.count()
        orphan_items.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} orphan checklist items.'))
