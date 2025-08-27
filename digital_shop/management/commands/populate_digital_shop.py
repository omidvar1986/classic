from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.utils import timezone
from digital_shop.models import (
    Category, Brand, Product, ProductImage, ProductAttribute, 
    Banner, Coupon
)
from io import BytesIO
from PIL import Image
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate digital shop with comprehensive sample data'

    def create_sample_image(self, name, width=400, height=400, color='#3498db'):
        """Create a simple colored sample image"""
        image = Image.new('RGB', (width, height), color)
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        return ContentFile(buffer.getvalue(), name=f'{slugify(name)}.jpg')

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate digital shop...')
        
        # Create Categories
        categories_data = [
            {
                'name': 'لپ تاپ و کامپیوتر',
                'description': 'انواع لپ تاپ، کامپیوتر و لوازم جانبی',
                'icon': 'fas fa-laptop',
                'color': 'primary',
                'is_featured': True,
            },
            {
                'name': 'موبایل و تبلت',
                'description': 'گوشی موبایل، تبلت و لوازم جانبی',
                'icon': 'fas fa-mobile-alt',
                'color': 'success',
                'is_featured': True,
            },
            {
                'name': 'لوازم گیمینگ',
                'description': 'کیبورد، ماوس، هدست گیمینگ',
                'icon': 'fas fa-gamepad',
                'color': 'warning',
                'is_featured': True,
            },
            {
                'name': 'لوازم التحریر',
                'description': 'خودکار، مداد، دفترچه و لوازم التحریر',
                'icon': 'fas fa-pen',
                'color': 'info',
                'is_featured': True,
            },
            {
                'name': 'حافظه و ذخیره سازی',
                'description': 'فلش مموری، هارد دیسک، SSD',
                'icon': 'fas fa-hdd',
                'color': 'secondary',
                'is_featured': True,
            },
            {
                'name': 'لوازم دفتری',
                'description': 'لوازم اداری و دفتری',
                'icon': 'fas fa-briefcase',
                'color': 'dark',
                'is_featured': False,
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'is_featured': cat_data['is_featured'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create Brands
        brands_data = [
            {'name': 'اپل', 'description': 'محصولات اپل', 'is_featured': True},
            {'name': 'سامسونگ', 'description': 'محصولات سامسونگ', 'is_featured': True},
            {'name': 'ایسوس', 'description': 'لپ تاپ و کامپیوتر ایسوس', 'is_featured': True},
            {'name': 'اچ پی', 'description': 'محصولات HP', 'is_featured': True},
            {'name': 'لنوو', 'description': 'لپ تاپ لنوو', 'is_featured': True},
            {'name': 'دل', 'description': 'محصولات Dell', 'is_featured': True},
            {'name': 'لاجیتک', 'description': 'لوازم جانبی لاجیتک', 'is_featured': True},
            {'name': 'کینگستون', 'description': 'حافظه کینگستون', 'is_featured': False},
        ]

        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=slugify(brand_data['name']),
                defaults={
                    'name': brand_data['name'],
                    'description': brand_data['description'],
                    'is_featured': brand_data['is_featured'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'Created brand: {brand.name}')

        # Create Products
        products_data = [
            {
                'name': 'لپ تاپ ایسوس VivoBook 15',
                'short_description': 'لپ تاپ 15 اینچی با عملکرد بالا',
                'description': 'لپ تاپ ایسوس VivoBook 15 با پردازنده Intel Core i5، 8GB RAM و 256GB SSD',
                'category': 'لپ تاپ و کامپیوتر',
                'brand': 'ایسوس',
                'price': Decimal('18500000'),
                'compare_price': Decimal('22000000'),
                'stock_quantity': 15,
                'is_featured': True,
                'is_new': True,
                'is_on_sale': True,
                'attributes': [
                    ('پردازنده', 'Intel Core i5-1135G7'),
                    ('رم', '8GB DDR4'),
                    ('حافظه', '256GB SSD'),
                    ('صفحه نمایش', '15.6 اینچ Full HD'),
                ]
            },
            {
                'name': 'گوشی موبایل سامسونگ Galaxy A54',
                'short_description': 'گوشی هوشمند با دوربین فوق العاده',
                'description': 'گوشی سامسونگ Galaxy A54 با دوربین 50 مگاپیکسل و باتری قوی',
                'category': 'موبایل و تبلت',
                'brand': 'سامسونگ',
                'price': Decimal('12800000'),
                'compare_price': Decimal('14500000'),
                'stock_quantity': 25,
                'is_featured': True,
                'is_bestseller': True,
                'is_on_sale': True,
                'attributes': [
                    ('صفحه نمایش', '6.4 اینچ Super AMOLED'),
                    ('دوربین', '50MP + 12MP + 5MP'),
                    ('باتری', '5000mAh'),
                    ('حافظه', '128GB'),
                ]
            },
            {
                'name': 'کیبورد مکانیکی گیمینگ لاجیتک G Pro X',
                'short_description': 'کیبورد مکانیکی حرفه‌ای برای گیمرها',
                'description': 'کیبورد مکانیکی لاجیتک G Pro X با سوییچ GX Blue و نورپردازی RGB',
                'category': 'لوازم گیمینگ',
                'brand': 'لاجیتک',
                'price': Decimal('3200000'),
                'compare_price': Decimal('3800000'),
                'stock_quantity': 8,
                'is_featured': True,
                'is_bestseller': True,
                'attributes': [
                    ('نوع سوییچ', 'GX Blue Clicky'),
                    ('نورپردازی', 'RGB LIGHTSYNC'),
                    ('اتصال', 'USB-C'),
                ]
            },
            {
                'name': 'ماوس گیمینگ لاجیتک G502 HERO',
                'short_description': 'ماوس گیمینگ با دقت بالا',
                'description': 'ماوس گیمینگ لاجیتک G502 HERO با سنسور 25600 DPI',
                'category': 'لوازم گیمینگ',
                'brand': 'لاجیتک',
                'price': Decimal('1850000'),
                'stock_quantity': 12,
                'is_featured': True,
                'attributes': [
                    ('DPI', '25600'),
                    ('دکمه‌ها', '11 قابل برنامه‌ریزی'),
                    ('وزن', '121 گرم'),
                ]
            },
            {
                'name': 'هدست گیمینگ لاجیتک G733',
                'short_description': 'هدست بی‌سیم با کیفیت صدای عالی',
                'description': 'هدست گیمینگ بی‌سیم لاجیتک G733 با نورپردازی RGB و میکروفون',
                'category': 'لوازم گیمینگ',
                'brand': 'لاجیتک',
                'price': Decimal('2650000'),
                'stock_quantity': 6,
                'is_featured': True,
                'is_new': True,
                'attributes': [
                    ('اتصال', 'بی‌سیم 2.4GHz'),
                    ('باتری', 'تا 29 ساعت'),
                    ('میکروفون', 'قابل جداسازی'),
                ]
            },
            {
                'name': 'فلش مموری کینگستون 64GB USB 3.2',
                'short_description': 'فلش مموری پرسرعت و قابل اعتماد',
                'description': 'فلش مموری کینگستون DataTraveler 64GB با سرعت بالا',
                'category': 'حافظه و ذخیره سازی',
                'brand': 'کینگستون',
                'price': Decimal('420000'),
                'stock_quantity': 45,
                'is_bestseller': True,
                'attributes': [
                    ('ظرفیت', '64GB'),
                    ('نوع اتصال', 'USB 3.2 Gen 1'),
                    ('سرعت خواندن', 'تا 100MB/s'),
                ]
            },
            {
                'name': 'خودکار ژل بیک Cristal',
                'short_description': 'خودکار ژل با کیفیت بالا',
                'description': 'خودکار ژل بیک Cristal با جوهر آبی و نوشتار روان',
                'category': 'لوازم التحریر',
                'brand': 'بیک',
                'price': Decimal('8500'),
                'stock_quantity': 200,
                'is_bestseller': True,
                'attributes': [
                    ('نوع جوهر', 'ژل'),
                    ('رنگ', 'آبی'),
                    ('ضخامت نوک', '0.7mm'),
                ]
            },
            {
                'name': 'لپ تاپ اپل MacBook Air M2',
                'short_description': 'لپ تاپ فوق العاده سبک اپل',
                'description': 'لپ تاپ MacBook Air 13 اینچ با پردازنده M2 و طراحی فوق العاده سبک',
                'category': 'لپ تاپ و کامپیوتر',
                'brand': 'اپل',
                'price': Decimal('52000000'),
                'compare_price': Decimal('56000000'),
                'stock_quantity': 3,
                'is_featured': True,
                'is_new': True,
                'is_on_sale': True,
                'attributes': [
                    ('پردازنده', 'Apple M2'),
                    ('رم', '8GB'),
                    ('حافظه', '256GB SSD'),
                    ('صفحه نمایش', '13.6 اینچ Liquid Retina'),
                ]
            },
            {
                'name': 'تبلت سامسونگ Galaxy Tab A8',
                'short_description': 'تبلت اندروید با صفحه نمایش بزرگ',
                'description': 'تبلت سامسونگ Galaxy Tab A8 با صفحه 10.5 اینچی و عملکرد قدرتمند',
                'category': 'موبایل و تبلت',
                'brand': 'سامسونگ',
                'price': Decimal('7800000'),
                'stock_quantity': 18,
                'is_featured': True,
                'attributes': [
                    ('صفحه نمایش', '10.5 اینچ TFT'),
                    ('رم', '4GB'),
                    ('حافظه', '64GB'),
                    ('باتری', '7040mAh'),
                ]
            },
            {
                'name': 'دفترچه یادداشت A5',
                'short_description': 'دفترچه با کیفیت برای یادداشت‌برداری',
                'description': 'دفترچه یادداشت سایز A5 با 200 صفحه و جلد سخت',
                'category': 'لوازم التحریر',
                'brand': None,
                'price': Decimal('45000'),
                'stock_quantity': 85,
                'attributes': [
                    ('سایز', 'A5'),
                    ('تعداد صفحات', '200'),
                    ('نوع جلد', 'سخت'),
                ]
            },
        ]

        # Get category and brand objects
        categories = {cat.name: cat for cat in Category.objects.all()}
        brands = {brand.name: brand for brand in Brand.objects.all()}

        for prod_data in products_data:
            # Get category and brand
            category = categories.get(prod_data['category'])
            brand = brands.get(prod_data['brand']) if prod_data['brand'] else None
            
            if not category:
                self.stdout.write(f'Category not found: {prod_data["category"]}')
                continue
            
            # Create product
            product, created = Product.objects.get_or_create(
                sku=slugify(prod_data['name'])[:50],
                defaults={
                    'name': prod_data['name'],
                    'slug': slugify(prod_data['name']),
                    'short_description': prod_data['short_description'],
                    'description': prod_data['description'],
                    'category': category,
                    'brand': brand,
                    'price': prod_data['price'],
                    'compare_price': prod_data.get('compare_price'),
                    'stock_quantity': prod_data['stock_quantity'],
                    'is_active': True,
                    'is_featured': prod_data.get('is_featured', False),
                    'is_new': prod_data.get('is_new', False),
                    'is_bestseller': prod_data.get('is_bestseller', False),
                    'is_on_sale': prod_data.get('is_on_sale', False),
                    'view_count': random.randint(10, 500),
                    'sold_count': random.randint(0, 50),
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
                
                # Create product image
                image_colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
                color = random.choice(image_colors)
                sample_image = self.create_sample_image(product.name, color=color)
                
                ProductImage.objects.create(
                    product=product,
                    image=sample_image,
                    alt_text=product.name,
                    is_primary=True,
                    sort_order=0
                )
                
                # Create product attributes
                for attr_name, attr_value in prod_data.get('attributes', []):
                    ProductAttribute.objects.create(
                        product=product,
                        name=attr_name,
                        value=attr_value,
                        sort_order=0
                    )

        # Create Banners
        banners_data = [
            {
                'title': 'فروشگاه دیجیتال کلاسیک',
                'subtitle': 'بهترین محصولات دیجیتال را از ما بخرید',
                'position': 'homepage',
            },
            {
                'title': 'تخفیف ویژه لپ تاپ',
                'subtitle': 'تا 30% تخفیف روی لپ تاپ‌های منتخب',
                'position': 'homepage',
            },
            {
                'title': 'لوازم گیمینگ حرفه‌ای',
                'subtitle': 'کیبورد، ماوس و هدست گیمینگ با کیفیت',
                'position': 'homepage',
            }
        ]

        for banner_data in banners_data:
            banner, created = Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults={
                    'subtitle': banner_data['subtitle'],
                    'position': banner_data['position'],
                    'is_active': True,
                    'sort_order': 0,
                    'start_date': timezone.now(),
                }
            )
            if created:
                self.stdout.write(f'Created banner: {banner.title}')

        # Create Coupons
        coupons_data = [
            {
                'code': 'WELCOME10',
                'description': '10% تخفیف برای خرید اول',
                'discount_type': 'percentage',
                'discount_value': Decimal('10.00'),
                'minimum_order_amount': Decimal('500000'),
                'usage_limit': 100,
            },
            {
                'code': 'SAVE50K',
                'description': '50000 تومان تخفیف',
                'discount_type': 'fixed',
                'discount_value': Decimal('50000'),
                'minimum_order_amount': Decimal('1000000'),
                'usage_limit': 50,
            }
        ]

        for coupon_data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults={
                    'description': coupon_data['description'],
                    'discount_type': coupon_data['discount_type'],
                    'discount_value': coupon_data['discount_value'],
                    'minimum_order_amount': coupon_data['minimum_order_amount'],
                    'usage_limit': coupon_data['usage_limit'],
                    'is_active': True,
                    'valid_from': timezone.now(),
                    'valid_until': timezone.now() + timezone.timedelta(days=365),
                }
            )
            if created:
                self.stdout.write(f'Created coupon: {coupon.code}')

        # Final statistics
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✓ Digital shop populated successfully!'))
        self.stdout.write('\n📊 Final Statistics:')
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Brands: {Brand.objects.count()}')
        self.stdout.write(f'  Products: {Product.objects.count()}')
        self.stdout.write(f'  Product Images: {ProductImage.objects.count()}')
        self.stdout.write(f'  Banners: {Banner.objects.count()}')
        self.stdout.write(f'  Coupons: {Coupon.objects.count()}')
        
        # Show featured products
        featured_products = Product.objects.filter(is_featured=True, is_active=True)
        self.stdout.write(f'\n⭐ Featured Products ({featured_products.count()}):')
        for product in featured_products[:5]:
            self.stdout.write(f'  - {product.name} ({product.price:,} تومان)')
