# Jurnal Proses — Tugas 4

## Jalur yang Dipilih
- **Jalur A (RPC) & Jalur B (Message Queue)**
- **Alasan:** Mengeksplorasi kedua mekanisme komunikasi (sinkron dan asinkron) secara penuh untuk memahami kelebihan dan risiko penerapannya pada arsitektur microservices FoodGo.

## Kendala Teknis
- Memastikan port `5672` dan `15672` pada Docker Container RabbitMQ tidak terblokir firewall lokal.
- Penyesuaian skema serialisasi JSON saat mengirim payload data dictionary dari Publisher ke Consumer.

## Uji "Pesan Tidak Hilang" (Khusus Jalur B)
- **Langkah Uji:**
  1. Hentikan `consumer.py` (Ctrl+C).
  2. Jalankan `python publisher.py` di terminal.
  3. Buka dashboard RabbitMQ (`http://localhost:15672`) untuk melihat status antrean (terdapat 3 pesan *Unacked/Ready*).
  4. Jalankan `python consumer.py`.
- **Hasil yang Diamati:** Consumer secara otomatis menarik (*consume*) 3 pesan yang tertunda dalam antrean, memprosesnya berturut-turut, lalu mengirimkan ACK sehingga antrean kembali kosong.

## Analisis Kegagalan Komponen
- **Jika Server RPC Mati di Tengah Proses:** Client akan menerima exception `ConnectionRefusedError` atau `socket.error` karena koneksi TCP terputus sebelum respons diterima (*blocking timeout*).
- **Tempat Penyimpanan Pesan Saat Consumer MQ Mati:** Pesan disimpan pada RAM/Disk node RabbitMQ (karena opsi `durable=True` dan `delivery_mode=Persistent`), sehingga aman dan tidak hilang meskipun Consumer mati atau restart.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 07/10/2026 | Gemini | "Bantu berikan struktur ide analisis kelebihan RPC vs Message Queue dan alur pengujian asynchronous decoupling" | Menjelaskan konsep synchronous blocking vs event-driven architecture | Dibuat analisis kustom untuk kasus studi FoodGo dan ditulis ulang secara mandiri pada README.md |