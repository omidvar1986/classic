from django.core.management.base import BaseCommand
from print_service.models import Accessory, PackageDeal

class Command(BaseCommand):
    help = 'Create sample accessories for print and typing services'

    def handle(self, *args, **options):
        # Clear existing accessories
        Accessory.objects.all().delete()
        PackageDeal.objects.all().delete()
        
        # Create Print Service Accessories
        print_accessories = [
            # Binding Options
            {
                'name': 'Wire Binding',
                'description': 'Professional spiral binding for easy page turning and durability',
                'base_price': 2.50,
                'category': 'binding',
                'service_type': 'print',
                'icon': 'fas fa-spiral',
                'sort_order': 1
            },
            {
                'name': 'Plastic Comb Binding',
                'description': 'Affordable plastic comb binding for documents',
                'base_price': 1.80,
                'category': 'binding',
                'service_type': 'print',
                'icon': 'fas fa-link',
                'sort_order': 2
            },
            {
                'name': 'Ring Binder',
                'description': 'Professional ring binder for easy page removal',
                'base_price': 3.20,
                'category': 'binding',
                'service_type': 'print',
                'icon': 'fas fa-circle',
                'sort_order': 3
            },
            {
                'name': 'Staples',
                'description': 'Simple stapling for documents',
                'base_price': 0.50,
                'category': 'binding',
                'service_type': 'print',
                'icon': 'fas fa-thumbtack',
                'sort_order': 4
            },
            
            # Finishing Options
            {
                'name': 'Lamination',
                'description': 'Protective lamination for durability and professional look',
                'base_price': 1.00,
                'category': 'finishing',
                'service_type': 'print',
                'icon': 'fas fa-shield-alt',
                'sort_order': 1
            },
            {
                'name': 'UV Coating',
                'description': 'High-quality UV coating for premium finish',
                'base_price': 1.50,
                'category': 'finishing',
                'service_type': 'print',
                'icon': 'fas fa-paint-brush',
                'sort_order': 2
            },
            {
                'name': 'Corner Rounding',
                'description': 'Rounded corners for professional appearance',
                'base_price': 0.30,
                'category': 'finishing',
                'service_type': 'print',
                'icon': 'fas fa-circle-notch',
                'sort_order': 3
            },
            {
                'name': 'Hole Punching',
                'description': 'Standard hole punching for binders',
                'base_price': 0.25,
                'category': 'finishing',
                'service_type': 'print',
                'icon': 'fas fa-circle',
                'sort_order': 4
            },
            
            # Packaging
            {
                'name': 'Envelope',
                'description': 'Standard envelope for document protection',
                'base_price': 0.50,
                'category': 'packaging',
                'service_type': 'print',
                'icon': 'fas fa-envelope',
                'sort_order': 1
            },
            {
                'name': 'Folder',
                'description': 'Professional folder for document organization',
                'base_price': 1.00,
                'category': 'packaging',
                'service_type': 'print',
                'icon': 'fas fa-folder',
                'sort_order': 2
            },
            {
                'name': 'Plastic Sleeve',
                'description': 'Clear plastic sleeve for document protection',
                'base_price': 0.25,
                'category': 'packaging',
                'service_type': 'print',
                'icon': 'fas fa-file-alt',
                'sort_order': 3
            },
        ]
        
        # Create Typing Service Accessories
        typing_accessories = [
            {
                'name': 'Wire Binding',
                'description': 'Professional spiral binding for typed documents',
                'base_price': 2.50,
                'category': 'binding',
                'service_type': 'typing',
                'icon': 'fas fa-spiral',
                'sort_order': 1
            },
            {
                'name': 'Plastic Comb Binding',
                'description': 'Affordable binding for typed documents',
                'base_price': 1.80,
                'category': 'binding',
                'service_type': 'typing',
                'icon': 'fas fa-link',
                'sort_order': 2
            },
            {
                'name': 'Ring Binder',
                'description': 'Professional ring binder for typed documents',
                'base_price': 3.20,
                'category': 'binding',
                'service_type': 'typing',
                'icon': 'fas fa-circle',
                'sort_order': 3
            },
            {
                'name': 'Envelope',
                'description': 'Envelope for typed document delivery',
                'base_price': 0.50,
                'category': 'packaging',
                'service_type': 'typing',
                'icon': 'fas fa-envelope',
                'sort_order': 1
            },
            {
                'name': 'Folder',
                'description': 'Professional folder for typed documents',
                'base_price': 1.00,
                'category': 'packaging',
                'service_type': 'typing',
                'icon': 'fas fa-folder',
                'sort_order': 2
            },
        ]
        
        # Create accessories
        created_accessories = []
        for acc_data in print_accessories + typing_accessories:
            accessory = Accessory.objects.create(**acc_data)
            created_accessories.append(accessory)
            self.stdout.write(f"Created accessory: {accessory.name}")
        
        # Create package deals
        package_deals = [
            {
                'name': 'Wire Binding + Lamination',
                'description': 'Professional wire binding with protective lamination',
                'discount_price': 3.00,
                'original_price': 3.50,
                'service_type': 'print',
                'accessories': ['Wire Binding', 'Lamination']
            },
            {
                'name': 'Complete Professional Package',
                'description': 'Wire binding, lamination, and folder for maximum protection',
                'discount_price': 4.00,
                'original_price': 4.50,
                'service_type': 'print',
                'accessories': ['Wire Binding', 'Lamination', 'Folder']
            },
            {
                'name': 'Typing Professional Package',
                'description': 'Wire binding and folder for typed documents',
                'discount_price': 3.00,
                'original_price': 3.50,
                'service_type': 'typing',
                'accessories': ['Wire Binding', 'Folder']
            }
        ]
        
        for deal_data in package_deals:
            accessories = deal_data.pop('accessories')
            deal = PackageDeal.objects.create(**deal_data)
            
            # Add accessories to package deal
            for acc_name in accessories:
                try:
                    acc = Accessory.objects.get(name=acc_name, service_type=deal.service_type)
                    deal.accessories.add(acc)
                except Accessory.DoesNotExist:
                    self.stdout.write(f"Warning: Accessory '{acc_name}' not found for deal '{deal.name}'")
            
            self.stdout.write(f"Created package deal: {deal.name} (Save ${deal.savings})")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_accessories)} accessories and {len(package_deals)} package deals!'
            )
        ) 