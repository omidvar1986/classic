from django.core.management.base import BaseCommand
from print_service.models import PaymentSettings


class Command(BaseCommand):
    help = 'Set up sample payment settings for manual payment system'

    def handle(self, *args, **options):
        # Check if payment settings already exist
        if PaymentSettings.objects.exists():
            self.stdout.write(
                self.style.WARNING('Payment settings already exist. Skipping setup.')
            )
            return

        # Create sample payment settings
        payment_settings = PaymentSettings.objects.create(
            bank_name="بانک ملی ایران",
            account_number="1234567890",
            card_number="6037-1234-5678-9012",
            shaba_number="IR123456789012345678901234",
            account_holder="علی رضایی",
            payment_instructions="""
            لطفاً نکات زیر را رعایت کنید:
            • مبلغ دقیق سفارش را واریز کنید
            • رسید پرداخت را واضح و خوانا آپلود کنید
            • شماره تراکنش را در صورت وجود وارد کنید
            • پرداخت شما در کمتر از 24 ساعت بررسی خواهد شد
            """,
            order_validity_hours=24,
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created payment settings for {payment_settings.bank_name}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Card Number: {payment_settings.card_number}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Account Holder: {payment_settings.account_holder}'
            )
        ) 