# Tugas 3 — Efisiensi Proses & Kontainer FoodGo

**Kelompok:** [Isi Nama Kelompok]  
**Anggota:**  
1. Dwi Surya Andika (103072400003) - [Bagian Pengerjaan mencoba menguji data di docker dan juga di vscode apakah berhasil atau tidak]  
2. Krisna Wahyudi Pratama (103072400048) - [## 1. Analisis Race Condition & Solusi Lock]  
3. [Nama Teman 2] ([NIM]) - [Bagian Pengerjaan]  

---

## 1. Analisis Race Condition & Solusi Lock

### Masalah Race Condition (Tanpa Lock)
Ketika 100 pesanan diproses oleh 10 *thread* secara bersamaan tanpa proteksi, terjadi fenomena **Race Condition** pada variabel global `processed_count`. 

Di tingkat prosesor, operasi `processed_count += 1` terdiri dari 3 langkah:
1. Membaca nilai `processed_count` saat ini dari memori.
2. Menambahkan nilai tersebut dengan 1.
3. Menyimpan kembali nilai baru ke memori.

Tanpa adanya sinkronisasi, dua atau lebih *thread* bisa membaca nilai yang sama secara serentak (misalnya nilai 20). Kedua *thread* memproses pesanannya masing-masing, lalu sama-sama menyimpan nilai 21 ke memori. Akibatnya, terjadi *lost update* (satu hitungan hilang), sehingga hasil akhir pesanan yang terhitung sering bernilai di bawah 100 (misalnya 88 atau 93).

### Solusi Sinkronisasi (`threading.Lock()`)
Untuk membenahi masalah ini, kami menggunakan objek `threading.Lock()` dengan blok `with lock:`. Mekanisme ini menjamin **Mutual Exclusion**, yaitu aturan di mana hanya ada 1 *thread* yang boleh mengeksekusi operasi penambahan angka pada satu waktu. *Thread* lain yang ingin mengakses variabel harus mengantre hingga *thread* sebelumnya melepaskan kunci. Hasilnya, perhitungan selalu konsisten bernilai tepat **100**.

---

## 2. Mengapa Multithreading, Bukan Proses OS / Multiprocessing?

Pada studi kasus FoodGo, server mengalami *out of memory* karena setiap pesanan baru diproses dengan **membuat proses OS penuh (misalnya `fork()`)**.

* **Proses OS (Multiprocessing):** Setiap proses memiliki ruang memori terpisah (*isolated memory*). Jika ada 100 pesanan masuk bersamaan, sistem harus mengalokasikan RAM dan *overhead* CPU baru sebanyak 100 kali. Hal ini sangat boros sumber daya.
* **Multithreading:** Semua *thread* berjalan di dalam **satu proses yang sama** dan berbagi ruang memori (*shared memory*). Membuat 100 *thread* jauh lebih ringan (*lightweight*) daripada 100 proses OS, sehingga konsumsi RAM server FoodGo tetap hemat dan tidak berisiko *crash*.

---

## 3. Cara Menjalankan Aplikasi

### Menjalankan Langsung di Laptop
```bash
python3 src/order_simulator.py