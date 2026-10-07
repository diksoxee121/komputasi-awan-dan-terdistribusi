"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: Buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    
    # TODO 2: Panggil proxy.cek_saldo("user1") dan ukur waktu tempuh
    saldo = proxy.cek_saldo("user1")
    duration = time.time() - start
    print(f"Hasil cek_saldo('user1'): Rp {saldo:,.0f} (Waktu tempuh: {duration:.4f} detik)")

    print("\nMemanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: Panggil proxy.proses_pembayaran("user1", 20000)
    hasil = proxy.proses_pembayaran("user1", 20000)
    print(f"Hasil proses_pembayaran: {hasil}")


if __name__ == "__main__":
    main()