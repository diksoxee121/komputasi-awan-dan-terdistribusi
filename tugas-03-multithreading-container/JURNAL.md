# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- **Hasil `processed_count` yang didapat:** 88 (nilainya berubah-ubah antara 80–95 setiap kali dijalankan).
- **Kenapa bisa meleset:** Terjadi *race condition* karena beberapa *thread* membaca dan mengubah nilai `processed_count` pada milidetik yang sama. Perubahan dari satu *thread* tertimpa oleh *thread* lain sebelum sempat tersimpan dengan benar di memori.

## Percobaan dengan Lock
- **Hasil `processed_count` setelah perbaikan:** 100 (selalu konsisten bernilai tepat 100).

## Kendala Docker
- **Error yang ditemui saat `docker build`/`docker run`:** 
  - Sempat terjadi kendala saat eksekusi karena perintah di `Dockerfile` mencari `python3`, padahal di *base image* `python:3.11-slim` perintah bawaannya adalah `python`.
  - **Cara memperbaiki:** Mengubah perintah perintah utama di `Dockerfile` menjadi `CMD ["python", "src/order_simulator.py"]`.

---

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 4 Oktober 2026 | Gemini | *"Bagaimana cara membagi daftar order ID menjadi beberapa bagian untuk dimasukkan ke fungsi Thread di Python?"* | AI memberikan contoh pola pembagian indeks *slice* `start` dan `end` pada perulangan. | Logika pembagian diterapkan secara manual pada fungsi `main()` dengan menghitung `chunk_size`. |
| 4 Oktober 2026 | Gemini | *"Apa beda konsumsi memori antara OS process fork dengan Python multithreading pada server request tinggi?"* | AI menjelaskan perbedaan *isolated memory space* pada *process* vs *shared memory* pada *thread*. | Penjelasan dirangkai kembali dengan kalimat sendiri untuk mengisi bagian analisis `README.md`. |