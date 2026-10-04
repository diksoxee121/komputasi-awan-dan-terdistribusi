# Jurnal Proses — Tugas 2

**Tanggal:** [25 September 2026]

* **Opsi arsitektur yang dipertimbangkan:** Awalnya kami berdebat antara memakai murni SOA (semua pakai REST API) atau Pub-Sub. 
* **Kenapa akhirnya pilih Kombinasi SOA & Pub-Sub:** Kalau pakai SOA murni, Modul Pesanan tetap harus nge-*hit* API Modul Kurir. Kalau Modul Kurir lambat, Modul Pesanan ikut lambat (masih *tightly coupled*). Akhirnya disepakati alur pembayaran tetap SOA (biar aman dan pasti), sedangkan alur ke Resto dan Kurir pakai Pub-Sub via Message Broker biar aplikasi pelanggan tidak *loading* kelamaan.
* **Revisi diagram:** 
  * *Versi 1:* Client langsung tembak ke Modul Pesanan.
  * *Versi 2:* Ditambahkan komponen `API Gateway` di depan agar rapi, dan menambahkan tanda panah jelas membedakan mana jalur *publish* dan jalur *subscribe*.

---

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| :--- | :--- | :--- | :--- | :--- |
| 25 september | Gemini | *Gimana sih sintaks Mermaid Markdown buat bikin arsitektur sistem dari API Gateway ke microservices, lalu ke message broker?"* | AI memberikan kerangka dasar kode Mermaid dengan node `graph LR` beserta cara memberi panah teks. | Kode Mermaid disesuaikan sendiri. Node diganti menjadi Modul Pesanan, Pembayaran, Kurir, dan Resto sesuai skenario FoodGo. |
| 26 september | Gemini | *Apa aja sih kekurangan atau sisi negatif kalau kita pindah dari monolitik ke arsitektur pakai Message Broker / Pub-sub? Buat bahan brainstorming tugas."* | AI menjelaskan tentang kompleksitas *debugging*, biaya server bertambah, dan isu *eventual consistency*. | Poin tentang *debugging* yang susah dilacak dan *eventual consistency* kami saring, lalu bahasanya diubah agar nyambung dengan kasus keluhan pelanggan di FoodGo. |