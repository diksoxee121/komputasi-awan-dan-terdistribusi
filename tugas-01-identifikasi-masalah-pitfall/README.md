# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Dwi Surya Andika | 103072400003 |saya mengerjakan pitfall bagian 1  |
| [nama 2] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: The Network is Reliable — ditulis oleh Dwi Surya Andika

**Bukti di skenario:** Tim engineering FoodGo menulis asumsi eksplisit di kode mereka seperti # network is always reliable, no need for retry dan tidak menyediakan penanganan kegagalan koneksi antar-service.

**Kenapa ini keliru:** Jaringan fisik tidak pernah 100% andal. Dalam sistem terdistribusi, selalu ada risiko packet loss, gangguan kabel/WiFi, lonjakan trafik tiba-tiba (network congestion), network partition, hingga server tujuan yang sedang reboot singkat. Mengasumsikan jaringan selalu terhubung tanpa error adalah kesalahan fundamental.

**Dampak ke FoodGo:** Begitu terjadi koneksi terputus sesaat (transient failure) antara modul pesanan dan modul pembayaran saat jam makan siang, permintaan pesanan langsung gagal total atau error. Karena tidak ada mekanisme penanganan ganti/coba lagi, pengguna akan mendapati transaksi mereka gagal padahal masalah jaringan tersebut mungkin hanya berlangsung beberapa milidetik.

**Solusi desain awal:** Menerapkan **Retry Mechanism** otomatis yang dipadukan dengan **Exponential Backoff dan Jitter**. Jika panggilan antar-service gagal, sistem tidak langsung menyerah, melainkan mencoba ulang secara bertahap (misalnya memberi jeda 1 detik, lalu 2 detik, 4 detik) ditambah variasi waktu acak (*jitter*) agar permintaan ulang tidak menumpuk di detik yang sama persis.

**Trade-off:** Jika service tujuan ternyata mengalami *downtime* total (mati permanen, bukan sekadar gangguan jaringan sesaat), mekanisme *retry* otomatis dari ribuan pengguna secara bersamaan justru akan memicu **Retry Storm**. Hal ini malah memperberat beban server yang sedang bermasalah dan berisiko merembet ke service lain (*cascading failure*).

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
