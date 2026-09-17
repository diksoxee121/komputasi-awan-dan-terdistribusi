# Tugas 1 — Analisis Pitfall FoodGo

# [Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]

| Nama                   | NIM            | Kontribusi                        |
| ---------------------- | -------------- | --------------------------------- |
| Dwi Surya Andika       | 103072400003   | saya mengerjakan pitfall bagian 1 |
| krisna wahyudi pratama | [103072400048] | [saya mengerjakn pitfall 2]       |
| [nama 3]               | [nim]          | [pitfall/bagian yang dikerjakan]  |

## Pitfall 1: The Network is Reliable — ditulis oleh Dwi Surya Andika

**Bukti di skenario:** Tim engineering FoodGo menulis asumsi eksplisit di kode mereka seperti # network is always reliable, no need for retry dan tidak menyediakan penanganan kegagalan koneksi antar-service.

**Kenapa ini keliru:** Jaringan fisik tidak pernah 100% andal. Dalam sistem terdistribusi, selalu ada risiko packet loss, gangguan kabel/WiFi, lonjakan trafik tiba-tiba (network congestion), network partition, hingga server tujuan yang sedang reboot singkat. Mengasumsikan jaringan selalu terhubung tanpa error adalah kesalahan fundamental.

**Dampak ke FoodGo:** Begitu terjadi koneksi terputus sesaat (transient failure) antara modul pesanan dan modul pembayaran saat jam makan siang, permintaan pesanan langsung gagal total atau error. Karena tidak ada mekanisme penanganan ganti/coba lagi, pengguna akan mendapati transaksi mereka gagal padahal masalah jaringan tersebut mungkin hanya berlangsung beberapa milidetik.

**Solusi desain awal:** Menerapkan **Retry Mechanism** otomatis yang dipadukan dengan **Exponential Backoff dan Jitter**. Jika panggilan antar-service gagal, sistem tidak langsung menyerah, melainkan mencoba ulang secara bertahap (misalnya memberi jeda 1 detik, lalu 2 detik, 4 detik) ditambah variasi waktu acak (_jitter_) agar permintaan ulang tidak menumpuk di detik yang sama persis.

**Trade-off:** Jika service tujuan ternyata mengalami _downtime_ total (mati permanen, bukan sekadar gangguan jaringan sesaat), mekanisme _retry_ otomatis dari ribuan pengguna secara bersamaan justru akan memicu **Retry Storm**. Hal ini malah memperberat beban server yang sedang bermasalah dan berisiko merembet ke service lain (_cascading failure_).

---

## Pitfall 2:— ditulis oleh [krisna wahyudi pratama]

- **Bukti di skenario:**
  Tim engineering FoodGo mendesain alur transaksi secara sekuensial/beruntun (_synchronous chaining_), di mana service pesanan harus menunggu balasan satu per satu dari service stok, service promo, hingga service pembayaran secara langsung sebelum memberi kepastian ke pengguna.

- **Kenapa ini keliru:**
  Pemanggilan fungsi di dalam memori satu komputer (_in-memory call_) memang terjadi dalam hitungan nanodetik. Namun, pemanggilan _service_ melalui jaringan selalu membutuhkan waktu transit (_network latency_ / _Round Trip Time_). Menganggap latensi jaringan itu nol ms adalah kekeliruan besar karena setiap pemanggilan jaringan tambahan akan terus menambah waktu tunggu secara kumulatif.
- **Dampak ke FoodGo:**
  Waktu respons aplikasi membengkak secara signifikan (_high response time_). Ketika trafik meningkat di jam makan siang, penumpukan latensi dari banyak _service_ menyebabkan aplikasi pengguna mengalami _loading_ sangat lama (_laggy_), bahkan memicu _request timeout_ pada aplikasi seluler pengguna padahal _server_ tidak dalam kondisi mati.

- **Solusi desain awal:**
  Mengubah arsitektur dari _synchronous/blocking_ menjadi **Asynchronous Communication** berbasis _Message Queue_ (seperti RabbitMQ atau Apache Kafka) untuk alur yang tidak membutuhkan jawaban instan (seperti pengiriman notifikasi dan kalkulasi poin). Selain itu, memanfaatkan **Caching** (seperti Redis) agar _service_ tidak perlu melakukan pemanggilan jaringan berulang untuk data yang jarang berubah seperti promo.

- **Trade-off:**
  Penerapan komunikasi _asynchronous_ mengubah sifat konsistensi data menjadi **Eventual Consistency** (data tidak langsung berbarui di seluruh _service_ pada milidetik yang sama). Hal ini juga meningkatkan kompleksitas arsitektur, sehingga proses _debugging_ dan penelusuran _error_ (_distributed tracing_) membutuhkan usaha ekstra.

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

Ringkasan: Berdasarkan analisis terhadap studi kasus FoodGo, kegagalan sistem saat jam sibuk bukan disebabkan oleh kesalahan logika bisnis, melainkan akibat mengabaikan realitas infrastruktur jaringan (_Fallacies of Distributed Computing_). Mengasumsikan jaringan selalu andal dan latensi bernilai nol menyebabkan arsitektur sistem menjadi sangat rapuh (_fragile_) terhadap gangguan minor.

### Rekomendasi Strategis untuk Tim FoodGo:

1. **Penerapan _Resilience Patterns_:** Wajib menerapkan _Retry Mechanism_ dengan _Exponential Backoff & Jitter_ serta _Circuit Breaker_ pada setiap pemanggilan antar-_service_ untuk mencegah _cascading failure_ dan _retry storm_.
2. **Migrasi ke _Asynchronous Architecture_:** Mengubah alur pemanggilan sekuensial yang saling menunggu (_blocking_) menjadi berbasis _event/message queue_ (seperti RabbitMQ/Kafka) untuk proses non-kritis seperti notifikasi dan sistem poin.
3. **Pemanfaatan _Caching_ & _Distributed Tracing_:** Menggunakan Redis untuk memangkas _network latency_ pada data yang sering diakses, serta memasang _Distributed Tracing_ (seperti Jaeger/Zipkin) agar titik kemacetan jaringan (_bottleneck_) dapat terdeteksi secara _real-time_.
