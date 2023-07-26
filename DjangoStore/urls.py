from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('user/', include('users.urls')),
    path('product/', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
