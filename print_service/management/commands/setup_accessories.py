from django.core.management.base import BaseCommand
from print_service.models import Accessory

class Command(BaseCommand):
    help = 'Create sample accessories for print and typing services'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample accessories...')
        
        # Clear existing accessories
        Accessory.objects.all().delete()
        
        accessories_data = [
            # Binding Options
            {
                'name': 'صحافی فنری',
                'description': 'صحافی فنری برای اسناد و کتاب‌ها - مناسب برای اسناد ضخیم',
                'base_price': 15000,
                'category': 'binding',
                'service_type': 'both',
                'is_featured': True,
                'color': '#28a745',
                'sort_order': 1
            },
            {
                'name': 'صحافی چسبی',
                'description': 'صحافی چسبی حرفه‌ای - مناسب برای کتاب‌ها و مجلات',
                'base_price': 25000,
                'category': 'binding',
                'service_type': 'both',
                'is_featured': True,
                'color': '#17a2b8',
                'sort_order': 2
            },
            {
                'name': 'منگنه',
                'description': 'منگنه معمولی برای اسناد ساده',
                'base_price': 5000,
                'category': 'binding',
                'service_type': 'both',
                'is_featured': False,
                'color': '#6c757d',
                'sort_order': 3
            },
            
            # Finishing Options
            {
                'name': 'لمینت',
                'description': 'لمینت حرفه‌ای برای محافظت از اسناد',
                'base_price': 8000,
                'category': 'finishing',
                'service_type': 'both',
                'is_featured': True,
                'color': '#ffc107',
                'sort_order': 4
            },
            {
                'name': 'برش حرفه‌ای',
                'description': 'برش دقیق و حرفه‌ای اسناد',
                'base_price': 3000,
                'category': 'finishing',
                'service_type': 'both',
                'is_featured': False,
                'color': '#dc3545',
                'sort_order': 5
            },
            {
                'name': 'سوراخ کاری',
                'description': 'سوراخ کاری برای پوشه‌ها و کلاسورها',
                'base_price': 2000,
                'category': 'finishing',
                'service_type': 'both',
                'is_featured': False,
                'color': '#6f42c1',
                'sort_order': 6
            },
            
            # Paper Options
            {
                'name': 'کاغذ گلاسه',
                'description': 'کاغذ گلاسه با کیفیت بالا برای چاپ رنگی',
                'base_price': 12000,
                'category': 'paper',
                'service_type': 'print',
                'is_featured': True,
                'color': '#fd7e14',
                'sort_order': 7
            },
            {
                'name': 'کاغذ کاهی',
                'description': 'کاغذ کاهی طبیعی و دوستدار محیط زیست',
                'base_price': 8000,
                'category': 'paper',
                'service_type': 'both',
                'is_featured': False,
                'color': '#20c997',
                'sort_order': 8
            },
            {
                'name': 'کاغذ رنگی',
                'description': 'کاغذ رنگی در رنگ‌های مختلف',
                'base_price': 10000,
                'category': 'paper',
                'service_type': 'print',
                'is_featured': False,
                'color': '#e83e8c',
                'sort_order': 9
            },
            
            # Packaging
            {
                'name': 'پاکت پلاستیکی',
                'description': 'پاکت پلاستیکی شفاف برای محافظت',
                'base_price': 2000,
                'category': 'packaging',
                'service_type': 'both',
                'is_featured': False,
                'color': '#6c757d',
                'sort_order': 10
            },
            {
                'name': 'پوشه مقوایی',
                'description': 'پوشه مقوایی محکم و زیبا',
                'base_price': 5000,
                'category': 'packaging',
                'service_type': 'both',
                'is_featured': True,
                'color': '#28a745',
                'sort_order': 11
            },
            {
                'name': 'جعبه مقوایی',
                'description': 'جعبه مقوایی برای بسته‌بندی حرفه‌ای',
                'base_price': 8000,
                'category': 'packaging',
                'service_type': 'both',
                'is_featured': False,
                'color': '#fd7e14',
                'sort_order': 12
            },
            
            # Delivery
            {
                'name': 'ارسال فوری',
                'description': 'ارسال در همان روز (فقط تهران)',
                'base_price': 50000,
                'category': 'delivery',
                'service_type': 'both',
                'is_featured': True,
                'color': '#dc3545',
                'sort_order': 13
            },
            {
                'name': 'ارسال استاندارد',
                'description': 'ارسال در 2-3 روز کاری',
                'base_price': 25000,
                'category': 'delivery',
                'service_type': 'both',
                'is_featured': False,
                'color': '#17a2b8',
                'sort_order': 14
            },
            {
                'name': 'ارسال رایگان',
                'description': 'ارسال رایگان برای سفارشات بالای 200,000 تومان',
                'base_price': 0,
                'category': 'delivery',
                'service_type': 'both',
                'is_featured': True,
                'color': '#28a745',
                'sort_order': 15
            },
            
            # Priority
            {
                'name': 'تایپ فوری',
                'description': 'تایپ در 24 ساعت - فقط برای سرویس تایپ',
                'base_price': 100000,
                'category': 'priority',
                'service_type': 'typing',
                'is_featured': True,
                'color': '#dc3545',
                'sort_order': 16
            },
            {
                'name': 'پرینت فوری',
                'description': 'پرینت در 2 ساعت - فقط برای سرویس پرینت',
                'base_price': 30000,
                'category': 'priority',
                'service_type': 'print',
                'is_featured': True,
                'color': '#ffc107',
                'sort_order': 17
            },
            {
                'name': 'بازبینی اضافی',
                'description': 'بازبینی و ویرایش اضافی توسط متخصص',
                'base_price': 50000,
                'category': 'priority',
                'service_type': 'typing',
                'is_featured': False,
                'color': '#6f42c1',
                'sort_order': 18
            }
        ]
        
        for data in accessories_data:
            accessory = Accessory.objects.create(**data)
            self.stdout.write(f'Created accessory: {accessory.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(accessories_data)} accessories!')
        ) 