# Jurnal Proses — Tugas 9

## Diskusi deployment model
* **Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu:** Kami membandingkan Public Cloud murni, Private Cloud murni, dan Hybrid Cloud. Public Cloud murni dinilai kurang tepat untuk memegang kendali penuh atas data kependudukan dan biometrik yang sensitif, sementara Private Cloud murni berpotensi menghadapi tantangan biaya serta kecepatan adaptasi saat lonjakan trafik musiman seperti pemilu dan pendaftaran sekolah. Akhirnya kami memilih **Hybrid Cloud** agar data inti tetap berada di bawah kendali ketat namun komponen layanan/akses tetap elastis.

## Diskusi service model per komponen
* Kami memisahkan **IaaS** untuk basis data inti dan biometrik agar kendali keamanan dan enkripsi tetap di tangan pengelola negara, **PaaS** untuk layanan API dan portal verifikasi agar skala serta deployment aplikasi lebih lincah, dan **SaaS** hanya untuk fungsi pendukung internal non-sensitif.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18/11/2026 | Gemini | Diskusi karakteristik NIST, deployment/service model, risiko data kependudukan, dan skenario tandingan | Kerangka pemetaan NIST SP 800-145, pembagian IaaS/PaaS/SaaS per komponen, serta ide risiko sinkronisasi & skenario instansi daerah | Disusun ulang dan disesuaikan dengan konteks studi kasus data kependudukan, UU PDP, dan catatan diskusi kelompok di `README.md` |