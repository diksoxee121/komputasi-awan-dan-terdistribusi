"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # TODO 1: Kembalikan saldo dari dict `saldo_user`. Jika tidak ada, return 0.0.
    return float(saldo_user.get(user_id, 0.0))


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    # TODO 2: Validasi saldo dan update nilai saldo_user
    if user_id not in saldo_user:
        return {"status": "gagal", "pesan": "User tidak ditemukan", "saldo_akhir": 0.0}
    
    if saldo_user[user_id] < jumlah:
        return {"status": "gagal", "pesan": "Saldo tidak mencukupi", "saldo_akhir": saldo_user[user_id]}
    
    saldo_user[user_id] -= jumlah
    return {"status": "sukses", "pesan": "Pembayaran berhasil", "saldo_akhir": saldo_user[user_id]}


def main():
    # TODO 3: Buat SimpleXMLRPCServer di localhost port 8000 & daftarkan fungsi
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    
    print("RPC server modul Pembayaran berjalan di port 8000...")
    server.serve_forever()


if __name__ == "__main__":
    main()