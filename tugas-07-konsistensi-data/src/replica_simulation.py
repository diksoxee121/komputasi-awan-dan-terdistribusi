"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}

    def write(self, user_id: str, saldo_baru: float, version: int):
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)

    def get_version(self, user_id: str) -> int:
        return self.last_write_version.get(user_id, 0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float) -> int:
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_sekarang = self.jakarta.read(user_id)
        saldo_baru = saldo_sekarang + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        def delayed_replication():
            self.bandung.write(user_id, saldo_baru, version)

        timer = threading.Timer(REPLICATION_DELAY, delayed_replication)
        timer.start()
        print(f"[TODO] Replikasi ke Bandung akan tertunda {REPLICATION_DELAY} detik")
        
        return version

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """Implementasi Read-Your-Writes dengan polling versi replika."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        
        max_wait = 3.0
        start_time = time.time()
        while replica.get_version(user_id) < versi_minimal:
            if time.time() - start_time > max_wait:
                return self.jakarta.read(user_id)
            time.sleep(0.1)
            
        return replica.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  
    print("Baca saldo dari Bandung (naif):", system.baca_saldo_naif(user_id, "Bandung"))
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya bisa 0 (BUG)\n")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("=== Skenario dengan Read-Your-Writes ===")
    versi_topup = system.top_up(user_id, 20000)
    
    saldo_terkini = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_topup)
    print(f"Baca saldo dari Bandung (dengan Read-Your-Writes): {saldo_terkini}")
    print("-> Hasil terjamin benar dan konsisten meskipun replikasi latar belakang belum selesai!")


if __name__ == "__main__":
    main()