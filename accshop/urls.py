from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('core.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/customers/', include('customers.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.exceptions.custom_404_handler"
