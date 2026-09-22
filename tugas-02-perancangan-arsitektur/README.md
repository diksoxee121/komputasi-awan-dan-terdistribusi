# Tugas 2 — Perancangan Arsitektur FoodGo
**Anggota:**
1. Dwi Surya Andika (103072400003) - : Merancang Diagram & Skenario
2. [Nama Teman 1] ([NIM]) - : Analisis Trade-off
3. [Nama Teman 2] ([NIM]) - : Justifikasi Arsitektur

---

## 1. Pemilihan Gaya Arsitektur & Justifikasi
Kami memilih menggunakan **Kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub)**. 

**Justifikasinya:** 
Tidak semua proses di FoodGo harus ditunggu secara langsung (sinkron). Proses krusial seperti pembuatan pesanan dan pengecekan pembayaran butuh kepastian instan, sehingga lebih cocok memakai gaya **SOA** (komunikasi sinkron lewat HTTP/REST). Namun, untuk urusan meneruskan informasi ke pihak resto dan mencari kurir, pelanggan tidak perlu menunggu *loading* di aplikasi sampai kurir didapat. Oleh karena itu, kami memisahkan modul Kurir dan Resto menggunakan gaya **Pub-Sub** (komunikasi asinkron lewat Message Broker) agar sistem benar-benar *decoupled* (terpisah dan tidak saling mengunci).

---

## 2. Diagram Arsitektur FoodGo

```mermaid
graph LR
    Client[Aplikasi Pelanggan] -->|HTTP Request| API[API Gateway]
    
    API -->|1. Create Order| OrderSvc[Modul Pesanan]
    OrderSvc -->|2. Cek Bayar| PaySvc[Modul Pembayaran]
    
    OrderSvc -->|3. Publish Event: 'Order_Paid'| Broker[(Message Broker / RabbitMQ)]
    
    Broker -->|4. Subscribe| RestoSvc[Modul Katalog Resto]
    Broker -->|4. Subscribe| CourierSvc[Modul Kurir & Notifikasi]
    
    classDef core fill:#f9f,stroke:#333,stroke-width:2px;
    classDef async fill:#bbf,stroke:#333,stroke-width:2px;
    
    class OrderSvc,PaySvc core;
    class RestoSvc,CourierSvc async;
 ```

 ---

## 3. Penjelasan Skenario End-to-End
Berdasarkan diagram di atas, berikut adalah alur ketika pelanggan memesan makanan:

1. **Membuat Pesanan (Sinkron):** Pelanggan menekan tombol "Pesan". Aplikasi mengirim HTTP Request ke *API Gateway*, yang meneruskannya ke **Modul Pesanan**. 
2. **Pembayaran (Sinkron):** Modul Pesanan langsung nge-*hit* API **Modul Pembayaran** untuk memotong saldo (*Request-Response*). Jika sukses, status pesanan menjadi "Dibayar".
3. **Publish Event (Asinkron):** Setelah dibayar, Modul Pesanan menerbitkan *event* `Order_Paid` ke **Message Broker**. Aplikasi pelanggan sudah bisa menampilkan layar "Pesanan diproses" tanpa *loading* lama.
4. **Subscribe & Eksekusi (Asinkron):** 
   - **Modul Katalog Resto** menangkap event tersebut dan memunculkan notifikasi di resto untuk mulai memasak.
   - **Modul Kurir** juga menangkap event itu dan mulai mencari *driver* terdekat secara otomatis di latar belakang.

---

## 4. Analisis Trade-Off

**Mengatasi Masalah Coupling (Tugas 1):**
Sekarang tim bisa melakukan *deploy* ulang atau perbaikan pada Modul Kurir tanpa takut merusak fitur Pesanan. Jika Modul Kurir *down*, event `Order_Paid` tetap aman tersimpan di dalam Message Broker.

**Kelemahan & Kompleksitas Baru (Trade-off):**
1. **Debugging Lebih Kompleks:** Karena alur terputus oleh Message Broker (non-linear), jika ada masalah, pelacakan log harus dilakukan di tiga tempat berbeda (Modul Pesanan, Broker, dan Modul Resto).
2. **Eventual Consistency:** Ada potensi jeda waktu (delay). Status di pelanggan mungkin sudah "Dibayar", tapi tablet resto baru berbunyi beberapa detik kemudian karena antrean Message Broker.





    
