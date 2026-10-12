# Laporan Tugas 5 — Koordinasi & Konsensus (Bully Algorithm)

## 1. Kenapa Sistem Membutuhkan Leader?
Dalam arsitektur terdistribusi seperti FoodGo, pemrosesan pesanan membutuhkan satu pengelola terpusat (*Node Leader*) untuk mengatur urutan antrean transaksi secara konsisten. Jika tidak ada leader, beberapa server dapat mencatat konflik urutan waktu atau melakukan pemrosesan ganda (*double processing*) pada pesanan yang sama.

## 2. Mengapa Bully Algorithm Selalu Memilih Node Ber-ID Tertinggi?
Bully Algorithm menggunakan pendekatan deterministik berbasis prioritas ID. Setiap node yang memicu pemilihan (*election*) wajib menantang seluruh node lain yang memiliki ID lebih besar darinya. Jika node ber-ID lebih besar tersebut merespons, mereka mengambil alih proses pemilihan. Proses ini berjenjang hingga node dengan ID tertinggi yang masih aktif menyatakan dirinya sebagai pemimpin tunggal (*Coordinator*).

## 3. Analisis Trade-off: Bully vs Raft
* **Bully Algorithm:** 
  * *Kelebihan:* Sangat sederhana diimplementasikan dan cepat dalam menentukan leader jika node tertinggi aktif.
  * *Kelemahan:* Menghasilkan lonjakan trafik pesan (*message overhead*) yang tinggi saat pemilihan terjadi, serta rentan mengalami *single point of failure* atau pemilihan berulang jika node tertinggi mengalami *flapping* (hidup-mati berulang kali).
* **Raft Consensus:** 
  * *Kelebihan:* Menggunakan pemilihan acak (*randomized timeouts*) untuk menghindari bentrok pemilihan, serta mampu mengelola replikasi log data secara aman di samping pemilihan leader.
  * *Kelemahan:* Kompleksitas kode dan implementasi jauh lebih tinggi dibanding Bully.

## 4. Hasil Pengujian Skenario
* **Skenario 1 (Start Normal):** Ketika node 1 sampai 5 dinyalakan bersamaan, seluruh node memicu election dan node dengan ID tertinggi (`Node 5`) sukses terpilih sebagai leader secara otomatis.
* **Skenario 2 (Leader Mati):** Saat proses `Node 5` dimatikan (`Ctrl+C`), node lain mendeteksi kegagalan ping setelah ~3 detik, memicu pemilihan ulang (*re-election*), dan `Node 4` terpilih sebagai leader baru dengan mulus.