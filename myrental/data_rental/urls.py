from django.contrib import admin
from django.urls import path
from data_rental import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('kendaraan/', views.daftar_rental, name='daftar_rental'),
    path('kendaraan2/<slug:slug_kendaraan2>/', views.detail_rental, name='detail_rental'),
    path('booking/<int:booking_id>/', views.proses_booking, name='proses_booking'),
    path('booking/sukses/', views.halaman_sukses, name='halaman_sukses'),
    path('midtrans-webhook/', views.midtrans_webhook, name='midtrans_webhook'),
    path('daftar/', views.register, name='register'),
    path('profil/', views.profil, name='profil'),
    path('login/', auth_views.LoginView.as_view(template_name='themes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

