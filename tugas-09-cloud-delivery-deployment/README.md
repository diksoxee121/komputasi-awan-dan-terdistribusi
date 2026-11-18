# Tugas 9 — Cloud Delivery & Deployment Model (Sistem Data Kependudukan)

## 1. Rekomendasi Deployment Model: Hybrid Cloud

Untuk Sistem Data Kependudukan yang memuat data sensitif warga negara (NIK, alamat, data biometrik) sesuai amanat UU Perlindungan Data Pribadi (UU PDP), melayani ribuan instansi (Dukcapil daerah, kepolisian, perbankan untuk KYC), serta menghadapi lonjakan trafik musiman (pemilu dan pendaftaran sekolah), **Hybrid Cloud** merupakan pilihan paling tepat.

Pendekatan ini memisahkan **zona privat / terkelola penuh oleh negara** (untuk penyimpanan basis data inti kependudukan dan biometrik dengan kendali akses ketat) dari **zona elastis / terdistribusi** (untuk menangani lonjakan beban antrean API verifikasi dan layanan non-sensitif).

Keterkaitan dengan **5 karakteristik esensial NIST (SP 800-145)**:
* **On-demand self-service:** Penyediaan instance komputasi atau antrean layanan verifikasi dapat dinaikkan secara mandiri oleh tim teknis saat musim pemilu atau PPDB tanpa menunggu proses pengadaan perangkat keras fisik yang berbulan-bulan.
* **Broad network access:** Ribuan instansi seperti Dukcapil daerah, kepolisian, dan bank dapat terhubung ke layanan verifikasi secara aman melalui jaringan terenkripsi dan standar API resmi dari berbagai lokasi.
* **Resource pooling:** Sumber daya komputasi dan penyimpanan di lapisan layanan/API dapat dibagi pakai secara efisien dengan isolasi antar-instansi (*tenant*) yang ketat, sementara basis data biometrik tetap berada pada pool privat khusus negara.
* **Rapid elasticity:** Saat terjadi lonjakan permintaan verifikasi secara tiba-tiba (misalnya saat masa pendaftaran sekolah atau hari pemungutan suara), kapasitas layanan dapat bertambah cepat dan kembali menyusut saat trafik normal agar tidak boros sumber daya.
* **Measured service:** Setiap panggilan API, volume kueri, dan penggunaan sumber daya oleh tiap instansi dapat diukur dan dicatat secara otomatis untuk keperluan *audit trail*, pembatasan kuota (*rate limiting*), serta akuntabilitas akses data kependudukan.

---

## 2. Rekomendasi Service Model per Komponen Sistem

Karena kebutuhan kontrol dan keamanan tiap bagian sistem berbeda, model layanan dipetakan per komponen:

* **Basis Data Inti Kependudukan & Biometrik -> IaaS (di lingkungan privat/terkontrol negara):** Data NIK dan biometrik bersifat sensitif dan permanen sehingga negara perlu memegang kendali penuh atas sistem operasi, konfigurasi jaringan, manajemen kunci enkripsi (*key management*), serta kebijakan retensi dan audit akses sesuai UU PDP.
* **API Gateway, Layanan Verifikasi (KYC/Status) & Portal Layanan -> PaaS:** Tim pengembang dapat fokus pada logika aplikasi, autentikasi instansi, *auto-scaling*, dan *load balancing* saat lonjakan trafik tanpa direpotkan oleh pemeliharaan OS dasar secara manual.
* **Layanan Pendukung Internal (Monitoring, Ticketing, Administrasi Operasional) -> SaaS (khusus data non-sensitif):** Untuk kebutuhan operasional internal yang tidak memuat data biometrik mentah maupun data pribadi sensitif warga, pemanfaatan SaaS dapat mempercepat operasional selama aksesnya dibatasi dan diawasi ketat.

---

## 3. Risiko Spesifik & Mitigasi

1. **Sinkronisasi & Inkonsistensi Data Antar Segmen (Privat vs Lapisan Layanan):**
   * **Risiko:** Jika terjadi pembaruan data kependudukan (misalnya perubahan status atau blokir/pemutakhiran data) di basis data inti privat namun replikasi/sinkronisasi ke lapisan layanan verifikasi terlambat, instansi pengguna seperti bank bisa menerima status data yang belum mutakhir saat proses KYC.
   * **Mitigasi:** Terapkan aliran sinkronisasi terkontrol berbasis *event* dengan penanda versi/*timestamp*, validasi kesegaran data pada titik verifikasi kritis, serta mekanisme *retry* dan *dead-letter queue* bila sinkronisasi tertunda.

2. **Kebocoran atau Penyalahgunaan Data Pribadi & Biometrik Lintas Integrasi Instansi:**
   * **Risiko:** Data biometrik dan identitas kependudukan tidak bisa diganti seperti kata sandi apabila bocor; celah konfigurasi API atau akses berlebih dari instansi pihak ketiga dapat memicu pelanggaran UU PDP dan kerugian sosial.
   * **Mitigasi:** Terapkan enkripsi *in-transit* (TLS) dan *at-rest*, prinsip *least privilege* per instansi, respons verifikasi minimal (misalnya cukup mengembalikan status cocok/tidak cocok atau token terverifikasi alih-alih mengekspos seluruh data mentah bila tidak diperlukan), serta pencatatan log audit yang tidak mudah diubah.

---

## 4. Perbandingan dengan Alternatif yang Ditolak

* **Alternatif yang ditolak: Public Cloud Murni.** Meski sangat unggul dalam elastisitas dan kemudahan skala saat lonjakan pemilu atau pendaftaran sekolah, menempatkan seluruh sistem dan basis data kependudukan/biometrik murni di infrastruktur publik berisiko dari sisi kedaulatan dan kendali penuh negara atas data sensitif warga serta kepatuhan ketat terhadap regulasi perlindungan data pribadi.

---

## 5. Skenario Tandingan

* **Skenario:** *Bagaimana jika sejumlah instansi daerah atau kantor layanan kecil tidak memiliki infrastruktur private cloud maupun koneksi jaringan khusus yang memadai untuk terhubung langsung ke simpul privat?*
* **Jawaban:** Instansi daerah tidak perlu membangun *private cloud* sendiri. Mereka dapat mengakses layanan melalui *API gateway* atau portal web resmi yang diamankan dengan *Mutual TLS (mTLS)*, *token/credential* berlapis, pembatasan IP/perangkat, serta *rate limiting* terpusat—sehingga tetap dapat terlayani secara merata tanpa menurunkan standar keamanan basis data inti di sisi pusat.
