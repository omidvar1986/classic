from django.core.management.base import BaseCommand
from typing_service.models import TypingOrder
from django.utils import timezone

class Command(BaseCommand):
    help = 'Updates old order statuses to the new, refactored status choices.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting status update process...')

        # Define a mapping from old statuses to new ones
        status_map = {
            'accepted': 'in_progress',
            'done': 'completed',
            # Add any other old statuses you remember here
        }

        updated_count = 0
        for old_status, new_status in status_map.items():
            orders_to_update = TypingOrder.objects.filter(status=old_status)
            count = orders_to_update.count()
            if count > 0:
                orders_to_update.update(status=new_status, updated_at=timezone.now())
                self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} orders from "{old_status}" to "{new_status}".'))
                updated_count += count

        if updated_count == 0:
            self.stdout.write(self.style.WARNING('No orders with old statuses were found to update.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Finished: A total of {updated_count} orders were updated.')) 