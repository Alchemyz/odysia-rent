from django.shortcuts import render, get_object_or_404, redirect
from .models import Kendaraan, Reservasi
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, ProfilUpdateForm
from django.contrib import messages
from datetime import datetime, timedelta
import midtransclient
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import uuid
from django.http import HttpResponse
import json


# Create your views here.
def home(request):
    return render (request, "themes/homepage.html",{
        'is_home' : True,
    })

def daftar_rental(request):
    kendaraan = Kendaraan.objects.filter(status='Tersedia')

    # Filter Transmisi (Gunakan lookup ke field nama di model relasi)
    transmisi = request.GET.get('transmisi')
    if transmisi:
        # Kita gunakan __nama (asumsi field di model Transmisi bernama 'nama')
        kendaraan = kendaraan.filter(transmisi__nama_transmisi=transmisi)

    # Filter Kapasitas
    kapasitas_pilihan = request.GET.get('kapasitas')
    if kapasitas_pilihan == 'under_5':
        kendaraan = kendaraan.filter(kapasitas__lt=5)
    elif kapasitas_pilihan == '5_6':
        kendaraan = kendaraan.filter(kapasitas__range=(5, 6))
    elif kapasitas_pilihan == 'over_6':
        kendaraan = kendaraan.filter(kapasitas__gt=6)

    # Filter Harga
    harga_min = request.GET.get('min')
    harga_max = request.GET.get('max')
    if harga_min and harga_min.isdigit():
        kendaraan = kendaraan.filter(harga_per_hari__gte=harga_min)
    if harga_max and harga_max.isdigit():
        kendaraan = kendaraan.filter(harga_per_hari__lte=harga_max)

    # Urutkan
    urutkan = request.GET.get('urutkan')
    if urutkan == 'rendah':
        kendaraan = kendaraan.order_by('harga_per_hari')
    elif urutkan == 'tinggi':
        kendaraan = kendaraan.order_by('-harga_per_hari')

    return render(request, "themes/daftar_rental.html", {'kendaraan': kendaraan})

def detail_rental(request,slug_kendaraan2):
    kendaraan2  = get_object_or_404(Kendaraan, slug=slug_kendaraan2)
    return render (request, "themes/detail_rental.html",{
        'kendaraan2':kendaraan2,
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['nama_lengkap']
            user.save()
            
            # Update No HP di profil yang otomatis terbuat
            user.profil.no_hp = form.cleaned_data['no_hp']
            user.profil.save()
            
            login(request, user)
            messages.success(request, "Registrasi Berhasil!")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'themes/daftar.html', {'form': form})

@login_required
def profil(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilUpdateForm(request.POST, instance=request.user.profil)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profil berhasil diperbarui!")
            return redirect('profil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilUpdateForm(instance=request.user.profil)

    # AMBIL DATA PESANAN:
    # Mengambil semua data booking milik user yang sedang login, diurutkan dari yang terbaru
    daftar_pesanan = Reservasi.objects.filter(penyewa=request.user).order_by('-id')

    return render(request, 'themes/profil.html', {
        'u_form': u_form,
        'p_form': p_form,
        'daftar_pesanan': daftar_pesanan ,
        'client_key': settings.MIDTRANS_CLIENT_KEY
    })
@login_required
def proses_booking(request, booking_id):
    booking = get_object_or_404(Kendaraan, id=booking_id)
    user_profil = getattr(request.user, 'profil', None)

    if request.method == 'POST':
        # ... (ambil data form tetap sama) ...
        tgl_mulai_raw = request.POST.get('tanggal_mulai') 
        durasi = int(request.POST.get('durasi', 1))

        try:
            # PERBAIKAN TIMEZONE: Buat datetime menjadi 'aware'
            naive_datetime = datetime.strptime(tgl_mulai_raw, '%Y-%m-%d %H:%M')
            tgl_mulai = timezone.make_aware(naive_datetime) # <--- Solusi RuntimeWarning
            tgl_selesai = tgl_mulai + timedelta(days=durasi)

            # Simpan ke Database
            reservasi = Reservasi.objects.create(
                kendaraan=booking,
                penyewa=request.user,
                nama_lengkap=request.POST.get('nama_lengkap'),
                no_hp=request.POST.get('no_hp'),
                lokasi_ambil=request.POST.get('lokasi_ambil'),
                lokasi_kembali=request.POST.get('lokasi_kembali'),
                tanggal_mulai=tgl_mulai,
                tanggal_selesai=tgl_selesai,
                metode_pembayaran=request.POST.get('metode_pembayaran'),
                status='Pending',
                status_pembayaran='pending'
            )

            # Inisialisasi Midtrans
            snap = midtransclient.Snap(
                is_production=False, 
                server_key=settings.MIDTRANS_SERVER_KEY 
            )

            # PERBAIKAN ORDER ID: Tambahkan UUID pendek agar benar-benar unik
            unique_suffix = str(uuid.uuid4())[:4]
            order_id_unik = f"{reservasi.order_id}-{unique_suffix}"

            params = {
                "transaction_details": {
                    "order_id": order_id_unik,
                    "gross_amount": int(reservasi.total_harga),
                },
                "customer_details": {
                    "first_name": str(reservasi.nama_lengkap),
                    "email": str(request.user.email),
                    "phone": str(reservasi.no_hp),
                },
                "item_details": [{
                    "id": str(booking.id),
                    "price": int(booking.harga_per_hari),
                    "quantity": durasi,
                    "name": str(booking.model)[:50],
                }],
                "expiry": {
                "unit": "minutes",
                "duration": 120 # Set durasi ke 60 menit agar tidak cepat expired
                },
                "callbacks": {
                "finish": "http://127.0.0.1:8000/booking/sukses/"
                }
            }

            transaction = snap.create_transaction(params)
            snap_token = transaction['token']

            return render(request, 'themes/booking.html', {
                'booking': booking,
                'user_profil': user_profil,
                'snap_token': snap_token,
                'client_key': settings.MIDTRANS_CLIENT_KEY 
            })

        except Exception as e:
            print(f"Error Midtrans: {e}")
            messages.error(request, f"Gagal memproses booking: {e}")

    return render(request, 'themes/booking.html', {
        'booking': booking,
        'user_profil': user_profil,
        'client_key': settings.MIDTRANS_CLIENT_KEY
    })
    print(f"DEBUG: Token yang dihasilkan adalah {snap_token}")
def halaman_sukses(request):
    return render(request, 'themes/halaman_sukses.html')


@csrf_exempt
def midtrans_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id_midtrans = data.get('order_id')
            
            # Abaikan jika ini hanya data "Tes" dari dashboard Midtrans
            if "payment_notif_test" in order_id_midtrans:
                return HttpResponse(status=200)

            # Logika mengambil UUID (8-4-4-4-12)
            parts = order_id_midtrans.split('-')
            if len(parts) >= 5:
                order_id_asli = "-".join(parts[:5])
            else:
                order_id_asli = order_id_midtrans

            status_transaksi = data.get('transaction_status')

            # Update Database
            reservasi = Reservasi.objects.get(order_id=order_id_asli)
            
            if  status_transaksi in ['settlement', 'capture']:
                # Gunakan key 'settlement', bukan label 'Lunas'
                reservasi.status_pembayaran = 'settlement' 
                reservasi.status = 'Dikonfirmasi'
            elif status_transaksi in ['deny', 'expire', 'cancel']:
                # Gunakan key 'cancel' atau 'expire'
                reservasi.status_pembayaran = 'cancel'
                reservasi.status = 'Dibatalkan'
                
            reservasi.save()
            print(f"Sukses Update Order: {order_id_asli}")
            return HttpResponse(status=200)
            
        except Reservasi.DoesNotExist:
            print(f"Order ID {order_id_asli} tidak ditemukan di database.")
            return HttpResponse(status=200) # Tetap beri 200 agar Midtrans berhenti kirim
        except Exception as e:
            print(f"Error Webhook: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=400)


@login_required
def riwayat_pesanan(request):
    # Mengambil semua reservasi milik user yang sedang login, diurutkan dari yang terbaru
    daftar_riwayat = Reservasi.objects.filter(penyewa=request.user).order_id('-created_at')
    
    # Kita perlu mengirimkan Client Key agar jika ada tombol 'Bayar Lagi', Snap bisa jalan
    return render(request, 'themes/riwayat.html', {
        'daftar_riwayat': daftar_riwayat,
        'client_key': settings.MIDTRANS_CLIENT_KEY
    })