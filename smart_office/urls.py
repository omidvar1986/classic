from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# URL patterns that should NOT be translated (like the main admin and language switcher)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('paymentslip/', include('paymentslip.urls', namespace='paymentslip')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

# URL patterns that SHOULD be translated
urlpatterns += i18n_patterns(
    path('', include('core.urls', namespace='core')),
    path('print/', include('print_service.urls', namespace='print_service')),
    path('typing/', include('typing_service.urls', namespace='typing_service')),
    path('admin-panel/', include('admin_dashboard.urls', namespace='admin_dashboard')),
    prefix_default_language=False,
)

# This is for serving media files in development and should be at the end
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)