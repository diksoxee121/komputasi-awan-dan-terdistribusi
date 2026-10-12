# Jurnal Proses — Tugas 5

## Implementasi Bully
- **Kendala saat mengisi TODO 1-4:** Memastikan sinkronisasi thread menggunakan `threading.Event()` agar waktu tunggu balasan `"OK"` dalam `start_election()` berjalan akurat tanpa melakukan *blocking* permanen pada event handler socket server.

## Skenario 1: Start Normal
- **Leader yang terpilih:** Node 5 (Port 5005)
- **Log/Observasi:** Saat semua node dinyalakan, node ber-ID kecil mengirim pesan `ELECTION` ke node di atasnya. Node 5 tidak memiliki peer lebih tinggi, sehingga langsung mendeklarasikan diri sebagai `COORDINATOR` ke semua node.

## Skenario 2: Leader Dimatikan
- **Leader baru yang terpilih:** Node 4 (Port 5004)
- **Berapa lama waktu sampai leader baru terdeteksi:** Sekitar 3 hingga 5 detik (tergantung interval siklus `monitor_leader` dan timeout `ELECTION_TIMEOUT`).

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 12/10/2026 | Gemini | "Bantu berikan rancangan logika event-driven untuk sinkronisasi balasan OK pada Bully Algorithm di Python" | Menggunakan `threading.Event()` untuk menangkap sinyal OK dari `on_message` ke fungsi `start_election` | Disesuaikan dengan struktur kerangka kode `src/node.py` yang sudah disediakan |