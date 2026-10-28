# Laporan Tugas 7 — Konsistensi Data (Data-Centric & Client-Centric)

## 1. Analisis Model Konsistensi pada Kasus Saldo E-Wallet FoodGo
* **Kenapa Eventual Consistency Saja Tidak Cukup?** 
  Eventual consistency hanya menjamin bahwa seluruh replika akan konvergen (menjadi sama) pada suatu saat di masa depan jika tidak ada update baru. Dalam konteks finansial/transaksi e-wallet FoodGo, jeda waktu sementara (*stale data*) berdampak langsung pada kegagalan bisnis (transaksi pesanan ditolak padahal pelanggan baru saja *top-up*). Hal ini merusak pengalaman pengguna (*user experience*) secara krusial.
* **Kebutuhan Pendekatan:** Oleh karena itu, dibutuhkan model **Client-Centric Consistency**, khususnya jaminan **Read-Your-Writes**, di mana setelah klien melakukan pembaruan (seperti *top-up* di server Jakarta), pembacaan berikutnya oleh klien yang sama (meskipun melalui server lain seperti Bandung) dijamin melihat hasil pembaruan tersebut atau versi yang lebih baru.

## 2. Skenario Tambahan (Diluar Studi Kasus Utama)
* **Kasus:** Aplikasi Ojek Online (Pemesanan Perjalanan & Update Titik Jemput).
* **Model Konsistensi yang Tepat:** *Monotonic Reads*. Jika penumpang mengubah titik penjemputan atau melihat posisi driver di peta dari satu layar ke layar lain, sistem harus menjamin bahwa penumpang tidak melihat versi data yang "mundur ke belakang" (menampilkan posisi driver yang lebih lama dari yang baru saja diterima).

## 3. Sequence Diagram (Mermaid)

### A. Skenario Tanpa Jaminan Konsistensi (Terjadi Bug Inconsistent Read)
```mermaid
sequenceDiagram
    autonumber
    participant Pelanggan
    participant Server Jakarta
    participant Server Bandung

    Pelanggan->>Server Jakarta: Top-up Saldo (+Rp50.000)
    Server Jakarta-->>Pelanggan: Konfirmasi Sukses
    Note over Server Jakarta,Server Bandung: Proses replikasi latar belakang (Delay 2 detik)
    Pelanggan->>Server Bandung: Pesan Makanan (Read Saldo)
    Server Bandung-->>Pelanggan: Saldo Masih Rp0 (Stale Data / Transaksi Gagal)