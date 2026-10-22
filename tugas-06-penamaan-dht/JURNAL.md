# Jurnal Proses — Tugas 6

## Implementasi find_successor
* **Kesalahan pertama yang ditemui:** Lupa memperhitungkan kondisi *wrap-around* ketika nilai `key_hash` lebih besar daripada seluruh `node_id` yang tersedia di dalam ring (misal key bernilai 250 tapi ID node maksimum hanya sampai 210).
* **Cara memperbaikinya:** Menambahkan pengecekan logika kondisi: jika tidak ada node yang nilainya $\ge key\_hash$, fungsi langsung mengembalikan elemen pertama dari daftar node aktif yang sudah diurutkan (mengarah kembali ke node terkecil di awal ring).

## Skenario Join / Leave
* **Hasil sebelum & sesudah node baru bergabung:** Saat `node-medan-1` bergabung, rentang hash tanggung jawab terbagi ulang, dan beberapa kunci data kurir dimigrasikan ke node baru tersebut tanpa mengganggu ketersediaan lookup.
* **Hasil sebelum & sesudah node keluar:** Saat `node-jakarta-1` dikeluarkan via `leave()`, pemetaan kurir yang sebelumnya dipegang berhasil dialihkan ke node successor tanpa ada data yang hilang (*query lookup* tetap mengembalikan nilai IP dengan benar).

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19/10/2026 | Gemini | "Bantu jelaskan logika perbandingan wrap-around dan pencarian successor pada struktur data Chord DHT di Python" | Menggunakan pengurutan list node aktif dan iterasi pengecekan kondisi $\ge$ dengan fallback indeks pertama | Disesuaikan ke dalam method `find_successor` pada `src/chord_simulation.py` |