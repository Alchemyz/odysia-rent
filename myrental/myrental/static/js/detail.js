// Fungsi untuk menghitung total harga secara dinamis
function hitungTotal() {
    const hargaElem = document.getElementById('hargaPerHari');
    const durasiInput = document.getElementById('durasiInput');
    
    // Elemen target di halaman utama dan modal
    const totalUtama = document.getElementById('totalHargaUtama');
    const modalTotal = document.getElementById('modalTotalHarga');
    const modalDurasi = document.getElementById('modalDurasi'); // Elemen teks durasi di modal

    if (hargaElem && durasiInput) {
        // Ambil angka bersih untuk perhitungan
        const hargaDasar = parseInt(hargaElem.innerText.replace(/[^0-9]/g, ''));
        const jumlahHari = parseInt(durasiInput.value) || 1;

        if (!isNaN(hargaDasar)) {
            const total = hargaDasar * jumlahHari;
            const totalFormatted = total.toLocaleString('id-ID');

            // 1. Update harga di halaman detail utama
            if (totalUtama) totalUtama.innerText = totalFormatted;

            // 2. Update harga di dalam Pop-up Modal
            if (modalTotal) modalTotal.innerText = totalFormatted;
            
            // 3. Update TEKS DURASI di dalam Pop-up Modal (PENTING)
            if (modalDurasi) modalDurasi.innerText = jumlahHari;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // 1. Ambil data dari Session Storage (sinkronisasi dari halaman utama)
    const savedData = JSON.parse(sessionStorage.getItem('rentalSearch'));
    
    if (savedData) {
        const durasiInput = document.getElementById('durasiInput');
        const durasiText = document.getElementById('durasiText');
        
        if (durasiInput) {
            durasiInput.value = savedData.durasi;
            if (durasiText) durasiText.innerText = savedData.durasi + " Hari";
        }

        // Hitung total pertama kali saat halaman dimuat
        hitungTotal();
    }
});