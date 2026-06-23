"""
URL configuration for myrental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog
# Import views dari aplikasi data_rental secara spesifik
from data_rental.views import midtrans_webhook 

# 1. Masukkan webhook di luar i18n_patterns (agar Midtrans tidak bingung dengan bahasa /en/)
urlpatterns = [
    path('midtrans-webhook/', midtrans_webhook, name='midtrans_webhook'),
]

# 2. Gabungkan sisanya menggunakan += agar tidak menimpa variabel sebelumnya
urlpatterns += i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('admin/', admin.site.urls),
    path('filer/', include('filer.urls')),
    path('', include('data_rental.urls')), # Memuat URL aplikasi data_rental
    path('', include('cms.urls')),         # Django-CMS biasanya diletakkan paling bawah
)

# 3. Tambahkan konfigurasi media untuk file bukti_pembayaran/foto
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

