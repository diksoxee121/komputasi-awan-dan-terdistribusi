"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring telah dilengkapi.
"""

import hashlib

M_BITS = 8               
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        self.nodes: dict[int, str] = {}
        self.data: dict[int, tuple[str, str]] = {}  

    def find_successor(self, key_hash: int, exclude_node: int = None) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        active_nodes = [nid for nid in self.nodes.keys() if nid != exclude_node]
        if not active_nodes:
            raise Exception("Ring kosong, tidak ada node aktif!")
        
        active_nodes.sort()
        for nid in active_nodes:
            if nid >= key_hash:
                return nid
        return active_nodes[0]

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 
        old_successor = None
        if self.nodes:
            old_successor = self.find_successor(node_id)

        # TODO 
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # TODO 
        if old_successor is not None:
            keys_to_migrate = []
            for k_hash in list(self.data.keys()):
                pred_id = self.get_predecessor(node_id)
                if pred_id < node_id:
                    if pred_id < k_hash <= node_id:
                        keys_to_migrate.append(k_hash)
                else: 
                    if k_hash > pred_id or k_hash <= node_id:
                        keys_to_migrate.append(k_hash)
            
            for k_hash in keys_to_migrate:
                kurir_id, ip_kurir = self.data[k_hash]
                print(f"       -> Migrasi data {kurir_id} (hash={k_hash}) ke Node {node_id}")

    def get_predecessor(self, node_id: int) -> int:
        active_nodes = sorted(list(self.nodes.keys()))
        if len(active_nodes) <= 1:
            return node_id
        idx = active_nodes.index(node_id)
        return active_nodes[(idx - 1) % len(active_nodes)]

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)
        if node_id not in self.nodes:
            return

        successor_id = self.find_successor(node_id + 1)
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring. Data dialihkan ke successor Node {successor_id}")

        # TODO 

        # TODO 
        del self.nodes[node_id]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 
        target_node = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] Kurir {kurir_id} (hash={key_hash}) disimpan di Node ID {target_node}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 
        try:
            target_node = self.find_successor(key_hash)
        except Exception:
            return None

        if key_hash in self.data:
            kurir, ip = self.data[key_hash]
            return f"{ip} (diurus oleh Node ID {target_node})"
        return None


def main():
    ring = ChordRing()

    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()