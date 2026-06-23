from django.contrib import admin
from .models import TipeKendaraan, MerkKendaraan, Reservasi, Kendaraan, ModelKendaraan, TransmisiKendaraan, BahanBakarKendaraan, Reservasi
# Register your models here.

@admin.register(TipeKendaraan)
class TipeKendaraan (admin.ModelAdmin):
    list_display = ('nama_tipe',)

@admin.register(MerkKendaraan)
class MerkKendaraan (admin.ModelAdmin):
    list_display = ('nama_merk',)

@admin.register(ModelKendaraan)
class modelKendaraan(admin.ModelAdmin):
    list_display = ('nama_model',)

@admin.register(Kendaraan)
class KendaraanAdmin (admin.ModelAdmin):
    list_display = ('merk','model','tipe', 'kapasitas','harga_per_hari','status',)

@admin.register(TransmisiKendaraan)
class TransmisiAdmin (admin.ModelAdmin):
    list_display = ('nama_transmisi',)

@admin.register(BahanBakarKendaraan)
class BahanBakarAdmin (admin.ModelAdmin):
    list_display = ('nama_bahan',)

@admin.register(Reservasi)
class ReservasiAdmin (admin.ModelAdmin):
    list_display = ('nama_lengkap','status_pembayaran','status',)
    list_filter = ('status_pembayaran', 'tanggal_mulai')