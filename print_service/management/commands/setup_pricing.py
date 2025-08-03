from django.core.management.base import BaseCommand
from print_service.models import PrintPriceSettings
from typing_service.models import TypingPriceSettings

class Command(BaseCommand):
    help = 'Set up initial pricing settings for print and typing services'

    def handle(self, *args, **options):
        # Set up print pricing settings
        if not PrintPriceSettings.objects.exists():
            PrintPriceSettings.objects.create(
                base_price_per_page=50000,
                color_price_multiplier=1.5,
                double_sided_discount=0.8
            )
            self.stdout.write("Created Print Pricing Settings")
        else:
            self.stdout.write("Print Pricing Settings already exist")

        # Set up typing pricing settings
        if not TypingPriceSettings.objects.exists():
            TypingPriceSettings.objects.create(
                price_per_page=10000
            )
            self.stdout.write("Created Typing Pricing Settings")
        else:
            self.stdout.write("Typing Pricing Settings already exist")

        self.stdout.write(
            self.style.SUCCESS('Pricing settings setup completed!')
        ) 