from django.core.management.base import BaseCommand
from django.utils import timezone
from digital_shop.models import Category, Brand, Product, ProductImage, ProductAttribute, Banner

class Command(BaseCommand):
    help = 'Set up sample data for Digital File Shop'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Digital File Shop sample data...')
        
        # Create categories
        categories = self.create_categories()
        
        # Create brands
        brands = self.create_brands()
        
        # Create products
        products = self.create_products(categories, brands)
        
        # Create banners
        self.create_banners()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- {len(categories)} categories\n'
                f'- {len(brands)} brands\n'
                f'- {len(products)} products\n'
                f'Digital File Shop is ready!'
            )
        )

    def create_categories(self):
        categories_data = [
            {
                'name': 'Stationery',
                'slug': 'stationery',
                'description': 'High-quality stationery items for office and school use',
                'icon': 'fas fa-pen',
                'color': 'primary',
                'is_featured': True,
                'sort_order': 1
            },
            {
                'name': 'Computer Equipment',
                'slug': 'computer-equipment',
                'description': 'Professional computer equipment and accessories',
                'icon': 'fas fa-laptop',
                'color': 'success',
                'is_featured': True,
                'sort_order': 2
            },
            {
                'name': 'Flash Memory',
                'slug': 'flash-memory',
                'description': 'USB drives, memory cards, and storage solutions',
                'icon': 'fas fa-usb',
                'color': 'info',
                'is_featured': True,
                'sort_order': 3
            },
            {
                'name': 'Games',
                'slug': 'games',
                'description': 'Video games, board games, and gaming accessories',
                'icon': 'fas fa-gamepad',
                'color': 'warning',
                'is_featured': True,
                'sort_order': 4
            },
            {
                'name': 'Computer Parts',
                'slug': 'computer-parts',
                'description': 'Computer components and hardware',
                'icon': 'fas fa-microchip',
                'color': 'danger',
                'is_featured': True,
                'sort_order': 5
            },
            {
                'name': 'Office Supplies',
                'slug': 'office-supplies',
                'description': 'Essential office supplies and equipment',
                'icon': 'fas fa-briefcase',
                'color': 'secondary',
                'sort_order': 6
            }
        ]
        
        categories = []
        for data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        return categories

    def create_brands(self):
        brands_data = [
            {
                'name': 'Samsung',
                'slug': 'samsung',
                'description': 'Leading electronics and technology brand',
                'website': 'https://www.samsung.com',
                'is_featured': True
            },
            {
                'name': 'HP',
                'slug': 'hp',
                'description': 'Professional computing solutions',
                'website': 'https://www.hp.com',
                'is_featured': True
            },
            {
                'name': 'Logitech',
                'slug': 'logitech',
                'description': 'Computer peripherals and accessories',
                'website': 'https://www.logitech.com',
                'is_featured': True
            },
            {
                'name': 'SanDisk',
                'slug': 'sandisk',
                'description': 'Memory and storage solutions',
                'website': 'https://www.sandisk.com',
                'is_featured': True
            },
            {
                'name': 'Microsoft',
                'slug': 'microsoft',
                'description': 'Software and hardware solutions',
                'website': 'https://www.microsoft.com',
                'is_featured': True
            },
            {
                'name': 'ASUS',
                'slug': 'asus',
                'description': 'Computer hardware and components',
                'website': 'https://www.asus.com',
                'is_featured': True
            },
            {
                'name': 'Corsair',
                'slug': 'corsair',
                'description': 'Gaming peripherals and components',
                'website': 'https://www.corsair.com',
                'is_featured': True
            },
            {
                'name': 'Kingston',
                'slug': 'kingston',
                'description': 'Memory and storage products',
                'website': 'https://www.kingston.com',
                'is_featured': True
            }
        ]
        
        brands = []
        for data in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            brands.append(brand)
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
        
        return brands

    def create_products(self, categories, brands):
        products_data = [
            # Stationery Products
            {
                'name': 'Premium Fountain Pen',
                'slug': 'premium-fountain-pen',
                'description': 'High-quality fountain pen with smooth writing experience',
                'short_description': 'Professional fountain pen for elegant writing',
                'sku': 'STN-001',
                'category': categories[0],  # Stationery
                'brand': brands[4],  # Microsoft
                'price': 45.99,
                'compare_price': 59.99,
                'stock_quantity': 50,
                'condition': 'new',
                'is_featured': True,
                'is_new': True,
                'is_on_sale': True
            },
            {
                'name': 'Executive Notebook Set',
                'slug': 'executive-notebook-set',
                'description': 'Professional notebook set with leather cover',
                'short_description': 'Premium notebook set for business use',
                'sku': 'STN-002',
                'category': categories[0],  # Stationery
                'price': 29.99,
                'stock_quantity': 100,
                'condition': 'new',
                'is_featured': True
            },
            
            # Computer Equipment
            {
                'name': 'HP Pavilion Laptop',
                'slug': 'hp-pavilion-laptop',
                'description': '15.6-inch laptop with Intel Core i5 processor and 8GB RAM',
                'short_description': 'Powerful laptop for work and entertainment',
                'sku': 'COMP-001',
                'category': categories[1],  # Computer Equipment
                'brand': brands[1],  # HP
                'price': 699.99,
                'compare_price': 799.99,
                'stock_quantity': 25,
                'condition': 'new',
                'is_featured': True,
                'is_bestseller': True,
                'is_on_sale': True
            },
            {
                'name': 'Logitech Wireless Mouse',
                'slug': 'logitech-wireless-mouse',
                'description': 'Ergonomic wireless mouse with precision tracking',
                'short_description': 'Comfortable wireless mouse for daily use',
                'sku': 'COMP-002',
                'category': categories[1],  # Computer Equipment
                'brand': brands[2],  # Logitech
                'price': 39.99,
                'stock_quantity': 75,
                'condition': 'new',
                'is_featured': True
            },
            
            # Flash Memory
            {
                'name': 'SanDisk 128GB USB Drive',
                'slug': 'sandisk-128gb-usb-drive',
                'description': 'High-speed USB 3.0 flash drive with 128GB storage',
                'short_description': 'Fast and reliable USB storage solution',
                'sku': 'MEM-001',
                'category': categories[2],  # Flash Memory
                'brand': brands[3],  # SanDisk
                'price': 24.99,
                'compare_price': 34.99,
                'stock_quantity': 200,
                'condition': 'new',
                'is_featured': True,
                'is_bestseller': True,
                'is_on_sale': True
            },
            {
                'name': 'Kingston 32GB MicroSD Card',
                'slug': 'kingston-32gb-microsd-card',
                'description': 'Class 10 microSD card for cameras and phones',
                'short_description': 'High-speed microSD card for mobile devices',
                'sku': 'MEM-002',
                'category': categories[2],  # Flash Memory
                'brand': brands[7],  # Kingston
                'price': 12.99,
                'stock_quantity': 150,
                'condition': 'new',
                'is_featured': True
            },
            
            # Games
            {
                'name': 'Gaming Headset Pro',
                'slug': 'gaming-headset-pro',
                'description': '7.1 surround sound gaming headset with microphone',
                'short_description': 'Immersive gaming audio experience',
                'sku': 'GAME-001',
                'category': categories[3],  # Games
                'brand': brands[6],  # Corsair
                'price': 89.99,
                'compare_price': 119.99,
                'stock_quantity': 40,
                'condition': 'new',
                'is_featured': True,
                'is_new': True,
                'is_on_sale': True
            },
            {
                'name': 'Mechanical Gaming Keyboard',
                'slug': 'mechanical-gaming-keyboard',
                'description': 'RGB mechanical keyboard with customizable switches',
                'short_description': 'Professional gaming keyboard with RGB lighting',
                'sku': 'GAME-002',
                'category': categories[3],  # Games
                'brand': brands[6],  # Corsair
                'price': 149.99,
                'stock_quantity': 30,
                'condition': 'new',
                'is_featured': True
            },
            
            # Computer Parts
            {
                'name': 'ASUS RTX 3060 Graphics Card',
                'slug': 'asus-rtx-3060-graphics-card',
                'description': 'NVIDIA RTX 3060 graphics card for gaming and content creation',
                'short_description': 'Powerful graphics card for gaming',
                'sku': 'PART-001',
                'category': categories[4],  # Computer Parts
                'brand': brands[5],  # ASUS
                'price': 399.99,
                'compare_price': 499.99,
                'stock_quantity': 15,
                'condition': 'new',
                'is_featured': True,
                'is_bestseller': True,
                'is_on_sale': True
            },
            {
                'name': 'Kingston 16GB DDR4 RAM',
                'slug': 'kingston-16gb-ddr4-ram',
                'description': '16GB DDR4 memory module for desktop computers',
                'short_description': 'High-performance RAM for desktop PCs',
                'sku': 'PART-002',
                'category': categories[4],  # Computer Parts
                'brand': brands[7],  # Kingston
                'price': 79.99,
                'stock_quantity': 60,
                'condition': 'new',
                'is_featured': True
            },
            
            # Office Supplies
            {
                'name': 'Executive Desk Organizer',
                'slug': 'executive-desk-organizer',
                'description': 'Multi-compartment desk organizer for office supplies',
                'short_description': 'Keep your desk organized and professional',
                'sku': 'OFF-001',
                'category': categories[5],  # Office Supplies
                'price': 34.99,
                'stock_quantity': 80,
                'condition': 'new',
                'is_featured': True
            },
            {
                'name': 'Wireless Charging Pad',
                'slug': 'wireless-charging-pad',
                'description': 'Fast wireless charging pad for smartphones',
                'short_description': 'Convenient wireless charging solution',
                'sku': 'OFF-002',
                'category': categories[5],  # Office Supplies
                'brand': brands[0],  # Samsung
                'price': 49.99,
                'compare_price': 69.99,
                'stock_quantity': 45,
                'condition': 'new',
                'is_featured': True,
                'is_on_sale': True
            }
        ]
        
        products = []
        for data in products_data:
            product, created = Product.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            products.append(product)
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        return products

    def create_banners(self):
        banners_data = [
            {
                'title': 'New Arrivals',
                'subtitle': 'Discover the latest products in our collection',
                'position': 'homepage',
                'is_active': True,
                'sort_order': 1
            },
            {
                'title': 'Special Offers',
                'subtitle': 'Up to 50% off on selected items',
                'position': 'homepage',
                'is_active': True,
                'sort_order': 2
            },
            {
                'title': 'Gaming Gear',
                'subtitle': 'Professional gaming equipment for serious gamers',
                'position': 'category',
                'is_active': True,
                'sort_order': 1
            }
        ]
        
        for data in banners_data:
            banner, created = Banner.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created banner: {banner.title}') 