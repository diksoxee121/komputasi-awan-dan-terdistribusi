# Laporan Tugas 4 — Komunikasi Antar Komponen (RPC & Message Queue)

**Kelompok:** [Isi Nama Kelompok]  
**Anggota:**  
1. Dwi Surya Andika (103072400003) - [implementasi dan pengujian RPC.]  
2. Krisna Wahyudi Pratama (103072400048) - [analisis konsep dan alasan pemilihan pola komunikasi]  
3. Rizqi Rahmatullah (103072400018) - [implementasi RabbitMQ dan pembuktian bahwa pesan tidak hilang saat consumer mati.]  

## 1. Analisis Pola Komunikasi
* **Jalur A (RPC - Sinkron):** Cocok untuk operasi `cek_saldo` dan `proses_pembayaran` karena modul Pesanan memerlukan respons seketika (*real-time*) untuk memastikan transaksi valid sebelum melanjutkan alur pesanan.
* **Jalur B (Message Queue - Asinkron):** Cocok untuk notifikasi modul Kurir. Modul Pembayaran hanya mengirimkan event `pembayaran_berhasil` ke antrean tanpa harus menunggu modul Kurir selesai memprosesnya.

## 2. Dampak Salah Pola Komunikasi
* **Jika RPC dipakai untuk Notifikasi Kurir:** Modul Pembayaran akan mengalami *blocking*. Apabila server/modul Kurir lambat atau *down*, proses pembayaran pelanggan ikut tertahan atau *timeout*.
* **Jika Message Queue dipakai untuk Cek Saldo:** Modul Pesanan tidak bisa langsung mendapatkan status saldo secara *real-time* karena sifat MQ yang *asynchronous*, sehingga alur *checkout* pengguna menjadi terhambat.

## 3. Bukti Asynchronous Decoupling (Uji Pesan Tidak Hilang)
Saat `consumer.py` dimatikan dan `publisher.py` dijalankan, 3 event berhasil dikirim dan tersimpan dengan aman di antrean RabbitMQ (`durable=True`). Ketika `consumer.py` dinyalakan kembali, seluruh event langsung diproses tanpa ada data yang hilang.