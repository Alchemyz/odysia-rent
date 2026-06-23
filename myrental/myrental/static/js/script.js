document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    
    filterForm.addEventListener('submit', function() {
        // Logika saat form dikirim
        const modalElement = document.getElementById('filterModal');
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
       
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const myModal = document.getElementById('filterModal');
    const myForm = document.getElementById('filterForm');

    // Reset form setiap kali modal DITUTUP
    myModal.addEventListener('hidden.bs.modal', function () {
        myForm.reset();
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const listContainer = document.getElementById('listDurasi');
    const durasiInput = document.getElementById('durasiInput');
    const durasiText = document.getElementById('durasiText');

    // 1. Generate pilihan 1 sampai 30
    for (let i = 1; i <= 30; i++) {
        const item = document.createElement('button');
        item.type = 'button';
        item.className = 'list-group-item list-group-item-action border-0 py-3 rounded-3 mb-1';
        item.innerHTML = `
            <div class="fw-bold">${i} Hari</div>
            <div class="text-muted small">Selesai : <span class="tgl-selesai" data-hari="${i}">-</span></div>
        `;
        
        item.onclick = function() {
            // Update nilai input dan tampilan teks
            durasiInput.value = i;
            durasiText.innerText = i + " Hari";
            
            // Tutup modal secara otomatis (menggunakan instance Bootstrap)
            const modalElem = document.getElementById('durasiModal');
            const modalInstance = bootstrap.Modal.getInstance(modalElem);
            modalInstance.hide();
            
            // Simpan ke session storage (fungsi yang Anda punya sebelumnya)
            
            saveToSession();
        };
        
        listContainer.appendChild(item);
    }
});

//kalender
document.addEventListener('DOMContentLoaded', function() {
    // Ambil data session di awal
    const savedData = JSON.parse(sessionStorage.getItem('rentalSearch'));
    const tglAwal = (savedData && savedData.tanggal) ? savedData.tanggal : "today";

    flatpickr("#tanggal", {
        locale: "id",
        altInput: true,
        altFormat: "j F Y",
        dateFormat: "Y-m-d",
        minDate: "today",
        defaultDate: tglAwal, // MEMAKSA FLATPICKR MENGGUNAKAN DATA SESSION
        disableMobile: "true",
        onChange: function(selectedDates, dateStr, instance) {
            saveToSession();
            updateEstimasiSelesai();
        },
        onReady: function() {
            // Langsung jalankan estimasi saat kalender siap
            updateEstimasiSelesai();
        }
    });
});

// logika waktu
let jamSekarang = 5;
let menitSekarang = 0;

function changeTime(type, value) {
    if (type === 'jam') {
        jamSekarang = (jamSekarang + value + 24) % 24;
        document.getElementById('displayJam').innerText = jamSekarang.toString().padStart(2, '0');
    } else {
        // Menit kita buat lompatan 15 menit agar lebih cepat
        menitSekarang = (menitSekarang + value + 60) % 60;
        document.getElementById('displayMenit').innerText = menitSekarang.toString().padStart(2, '0');
    }
}

function simpanWaktu() {
    const jamStr = jamSekarang.toString().padStart(2, '0');
    const menitStr = menitSekarang.toString().padStart(2, '0');
    const waktuLengkap = `${jamStr}:${menitStr}`;

    // Update tampilan di form dan input hidden
    document.getElementById('waktuText').innerText = waktuLengkap;
    document.getElementById('waktu').value = waktuLengkap;

    // Tutup Modal
    const modalElem = document.getElementById('waktuModal');
    const modalInstance = bootstrap.Modal.getInstance(modalElem);
    modalInstance.hide();
    
    // Simpan ke session storage
    saveToSession();
}

// Fungsi tambahan untuk menghitung tanggal selesai secara real-time di dalam modal
function updateEstimasiSelesai() {
    const tglMulai = document.getElementById('tanggal').value;
    const listTglSelesai = document.querySelectorAll('.tgl-selesai');
    
    if (tglMulai) {
        listTglSelesai.forEach(span => {
            const hari = parseInt(span.getAttribute('data-hari'));
            let date = new Date(tglMulai);
            date.setDate(date.getDate() + hari);
            
            const opsi = { day: 'numeric', month: 'long', year: 'numeric' };
            span.innerText = date.toLocaleDateString('id-ID', opsi);
        });
    }
}
// Jalankan estimasi saat tanggal jemput diubah
document.getElementById('tanggal').addEventListener('change', updateEstimasiSelesai);

// Simpan data saat klik "Cari"
function saveToSession() {
    const data = {
        tanggal: document.getElementById('tanggal').value,
        waktu: document.getElementById('waktu').value,
        durasi: document.getElementById('durasiInput').value
    };
    // Menyimpan objek data dalam bentuk string JSON
    sessionStorage.setItem('rentalSearch', JSON.stringify(data));
}


// Jalankan fungsi ini otomatis saat halaman dimuat
function loadFromSession() {
    const savedData = JSON.parse(sessionStorage.getItem('rentalSearch'));
    
    if (savedData) {
        // 1. Sinkronisasi Tanggal
        const tglElem = document.getElementById('tanggal');
        if(tglElem) tglElem.value = savedData.tanggal;
        
        // 2. Sinkronisasi Waktu
        const waktuInput = document.getElementById('waktu');
        const waktuText = document.getElementById('waktuText');
        if(waktuInput) {
            waktuInput.value = savedData.waktu;
            if(waktuText) waktuText.innerText = savedData.waktu;
            
            // Update variabel global jam & menit agar scroller modal sinkron
            const splitWaktu = savedData.waktu.split(':');
            jamSekarang = parseInt(splitWaktu[0]);
            menitSekarang = parseInt(splitWaktu[1]);
        }
        
        // 3. Sinkronisasi Durasi
        const durasiInput = document.getElementById('durasiInput');
        const durasiText = document.getElementById('durasiText');
        if(durasiInput) {
            durasiInput.value = savedData.durasi;
            if(durasiText) durasiText.innerText = savedData.durasi + " Hari";
        }

        // 4. Update Tampilan Booking (Jika ada)
        const displayElem = document.getElementById('durasiDisplay');
        if(displayElem) displayElem.innerText = savedData.durasi + " Hari";

        // Jalankan estimasi tanggal selesai agar list di modal durasi terupdate
        updateEstimasiSelesai();
    }
}
// Pastikan fungsi simpan dipanggil saat klik cari
document.querySelector('form').addEventListener('submit', function() {
    saveToSession();
});

// Jalankan load saat halaman siap
window.addEventListener('load', loadFromSession);