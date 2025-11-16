from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Redirect root URL to main shop
def root_redirect(request):
    return redirect('/healthkart/')

urlpatterns = [
    path('', root_redirect),  # Redirect homepage to /healthkart/
    path('healthkart/', include('shopee.urls')),  
    path('admin/', admin.site.urls),
]

# Media files (works on localhost)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
