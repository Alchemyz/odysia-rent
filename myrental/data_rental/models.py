from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.
class TipeKendaraan(models.Model):
    nama_tipe = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama_tipe)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_tipe

class MerkKendaraan(models.Model):
    nama_merk = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama_merk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_merk

class ModelKendaraan(models.Model):
    nama_model = models.CharField(max_length=20, unique=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama_model)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_model

class TransmisiKendaraan(models.Model):
    nama_transmisi = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama_transmisi)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_transmisi

class BahanBakarKendaraan(models.Model):
    nama_bahan = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama_bahan)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_bahan

class Kendaraan(models.Model):
    STATUS_PILIHAN = [
        ('Tersedia', 'Tersedia'),
        ('Disewa', 'Sedang Disewa'),
        ('Perawatan', 'Dalam Perawatan'),
    ]
    kapasitas = models.IntegerField(null=True)
    slug = models.SlugField(unique=True, blank=True)
    model = models.ForeignKey(ModelKendaraan, on_delete=models.CASCADE)
    transmisi = models.ForeignKey(TransmisiKendaraan, on_delete=models.CASCADE, null=True)
    harga_per_hari = models.DecimalField(max_digits=10, decimal_places=2)
    tipe = models.ForeignKey(TipeKendaraan, on_delete=models.CASCADE)
    merk = models.ForeignKey(MerkKendaraan, on_delete=models.CASCADE)
    bahan_bakar = models.ForeignKey(BahanBakarKendaraan, on_delete=models.CASCADE, null=True)
    gambar = models.ImageField(upload_to= 'kendaraan/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_PILIHAN, default='Tersedia')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.model)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.merk} {self.model} {self.tipe}"
    

class Reservasi(models.Model):
    STATUS_RESERVASI = [
        ('Pending', 'Menunggu Konfirmasi'),
        ('Dikonfirmasi', 'Dikonfirmasi'),
        ('Selesai', 'Selesai'),
        ('Dibatalkan', 'Dibatalkan'),
    ]

    STATUS_BAYAR = [
        ('pending', 'Menunggu Pembayaran'),
        ('settlement', 'Lunas'),
        ('expire', 'Kedaluwarsa'),
        ('cancel', 'Dibatalkan'),
    ]

    # Menggunakan null=True agar migrasi lancar
    order_id = models.UUIDField(editable=False, unique=True, null=True, blank=True)
    
    kendaraan = models.ForeignKey('Kendaraan', on_delete=models.CASCADE)
    penyewa = models.ForeignKey(User, on_delete=models.CASCADE)
    
    nama_lengkap = models.CharField(max_length=150, blank=True)
    no_hp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    lokasi_ambil = models.CharField(max_length=255, default='Kantor Pusat')
    lokasi_kembali = models.CharField(max_length=255, default='Kantor Pusat')
    
    tanggal_mulai = models.DateTimeField()
    tanggal_selesai = models.DateTimeField()
    
    total_harga = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    metode_pembayaran = models.CharField(max_length=50, blank=True, null=True)
    status_pembayaran = models.CharField(max_length=20, choices=STATUS_BAYAR, default='pending')
    bukti_pembayaran = models.ImageField(upload_to='bukti_bayar/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_RESERVASI, default='Pending')
    tanggal_reservasi = models.DateTimeField(auto_now_add=True)

    def hitung_durasi(self):
        diff = self.tanggal_selesai - self.tanggal_mulai
        days = diff.days
        if diff.seconds > 0:
            days += 1
        return days if days > 0 else 1

    def save(self, *args, **kwargs):
        # JAMINAN UUID: Jika order_id kosong (terutama data lama), isi di sini
        if not self.order_id:
            self.order_id = uuid.uuid4()

        if self.penyewa:
            if not self.nama_lengkap:
                full_name = f"{self.penyewa.first_name} {self.penyewa.last_name}".strip()
                self.nama_lengkap = full_name if full_name else self.penyewa.username
            if not self.email:
                self.email = self.penyewa.email
            if not self.no_hp:
                try:
                    self.no_hp = self.penyewa.profil.no_hp
                except:
                    pass
            
        durasi = self.hitung_durasi()
        if self.kendaraan:
            self.total_harga = durasi * self.kendaraan.harga_per_hari
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"RSV-{str(self.order_id)[:8].upper()} - {self.nama_lengkap}"


class Profil(models.Model):
    JENIS_KELAMIN = [
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN, blank=True, null=True)

    def __str__(self):
        return f"Profil {self.user.username}"
    
    # Signal untuk otomatis buat profile saat User baru mendaftar
@receiver(post_save, sender=User)
def create_user_profil(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profil(sender, instance, **kwargs):
   if hasattr(instance, 'profil'):
        instance.profil.save()
   else:
        # Jika profil belum ada (seperti pada Superuser lama), buatkan baru
        Profil.objects.create(user=instance)