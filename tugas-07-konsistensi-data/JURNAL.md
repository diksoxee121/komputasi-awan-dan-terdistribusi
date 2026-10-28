# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
* **Argumen yang dipertimbangkan:** Apakah sistem e-wallet memerlukan *Sequential Consistency* penuh secara global di semua pusat data? Kami mendiskusikan bahwa *Sequential Consistency* terlalu mahal dari sisi latensi jaringan karena setiap operasi tulis harus disinkronkan secara ketat ke seluruh node global sebelum dianggap selesai.
* **Kesimpulan akhir & alasan:** Untuk kasus lintas wilayah di Indonesia (Jakarta-Bandung), menerapkan *Eventual Consistency* murni berbahaya bagi transaksi finansial. Solusi terbaik adalah mempertahankan *Eventual Consistency* di tingkat backend antar server, namun dilapisi dengan **Client-Centric Consistency (Read-Your-Writes)** agar *user experience* klien tetap akurat tanpa mengorbankan performa sistem secara keseluruhan.

## Simulasi (Replikasi & Read-Your-Writes)
* **Hasil skenario naif vs Read-Your-Writes:** Pada simulasi naif, pembacaan saldo dari server Bandung langsung setelah *top-up* menghasilkan nilai `0.0` karena terkendala delay replikasi. Dengan menambahkan mekanisme pengecekan versi berbasis *threading* dan *polling* pada fungsi `baca_saldo_read_your_writes`, pembacaan dari Bandung berhasil menunggu atau menyesuaikan hingga data versi terbaru tiba, sehingga saldo yang terbaca akurat.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 28/10/2026 | Gemini | "Bantu jelaskan konsep implementasi version-tracking sederhana untuk Read-Your-Writes pada replikasi Python" | Menggunakan nomor versi (*version counter*) dan pelacakan versi per klien/transaksi | Diterapkan ke dalam kelas `Replica` dan `ReplicationSystem` di `src/replica_simulation.py` |