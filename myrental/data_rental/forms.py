from django import forms
from django.contrib.auth.models import User
from .models import Profil
from .models import Reservasi

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-login rounded-4', 'placeholder': 'Username'}))
    nama_lengkap = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control custom-login rounded-4', 'placeholder': 'Nama Lengkap'}))
    no_hp = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control custom-login rounded-4', 'placeholder': 'No. HP'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control custom-login rounded-4', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control custom-login rounded-4', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['no_hp', 'tanggal_lahir', 'jenis_kelamin']
        widgets = {
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-select'}),
        }


class ReservasiForm(forms.ModelForm):
    class Meta:
        model = Reservasi
        fields = ['nama_lengkap', 'no_hp', 'lokasi_ambil', 'lokasi_kembali', 'metode_pembayaran', 'bukti_pembayaran']