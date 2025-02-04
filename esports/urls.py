# File path: main urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('api.v1.products.urls')),
    path('api/v1/auth/', include('api.v1.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += (
         static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
