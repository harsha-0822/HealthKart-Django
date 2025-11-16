"""Ecommerce URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name="admin-site"),
    path('', include('shopee.urls')),  # 👈 Main homepage connects to your app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
