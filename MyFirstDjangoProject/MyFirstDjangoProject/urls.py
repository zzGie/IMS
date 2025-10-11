"""
URL configuration for MyFirstDjangoProject project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('user.urls')),  # All user app URLs
    path('admin/', admin.site.urls),  # Admin site
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
