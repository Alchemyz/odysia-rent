# Django template for a new django CMS 4 project

A Django template for a typical django CMS installation with no 
special bells or whistles. It is supposed as a starting point 
for new projects.

If you prefer a different set of template settings, feel free to 
create your own templates by cloning this repo.

To install django CMS 4 by hand type the following commands:

1. Create virtual environment and activate it
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install Django, django CMS and other required packages
   ```
   pip install django-cms
   ```
3. Create project `<<project_name>>` using this template
   ```
   djangocms <<project_name>>
   cd <<project_name>>
   ```
4. Run testserver
   ```
   ./manage.py runserver
   ```

Note: If you run into a problem of missing dependencies, please
update `pip` using `pip install -U pip` before running the 
`djangocms` command.

sudah bisa pindah ke halaman daftar rental tinggal cek apakah benar bisa memfilter kendaraan dan membuat  data search bar pada halaman utama dapat muncul pada search bar daftar rental

2/1/26
penjumlahan barang X durasi sewa pda halaman detail rental blum berhasil

3/1/26
daftar sudah bisa dan datanya kekirim ke profil.html(perlu edit desain)
login juga sudah bisa (perlu mengedit masuk dan daftar pda navbar)
perlu menaruh tombol logout dropdown pada logo user

4/1/26
selanjutnya kita akan membuat halaman booking dan mungkin sekalian mengkonfigurasikan metode pembayaran --->> halaman sukses booking --->> halaman profil

5/1/26 halaman booking sudah berhasil , selanjutnya metode payment ---->>>>halaman profil ---->>>>> halaman admin

6/1/26 halaman booking sudah fix selesai dari UI/UX dan datanya sudah terkirim lengkap, selanjutnya menambahkan metode pembayaran midtrans (doing your habbit bro)

8/1/26 pop up dari midtrans sudah muncul tapi saat kita mengklik metode pembayarannya langsung tertutup karena durasi pembayaraanya habis

9/1/26 pembayaran sudah bisa , sudah terkirim ke halama admin dan riwayat pesananan, tinggal bagaimana dia menuju riwayat pesanann saat menutup paymnet gateaway dan juga mendesain halaman sukses