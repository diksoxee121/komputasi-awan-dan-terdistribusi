"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) telah dilengkapi.
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()
        self.ok_received = threading.Event()


    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}")
        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_connection, args=(conn,), daemon=True).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                return
            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika node target tidak merespons (dianggap mati)."""
        try:
            with socket.create_connection(("localhost", target_port), timeout=1.0) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False


    def on_message(self, sender_id: int, msg_type: str):
        """Dipanggil setiap kali node ini menerima pesan dari node lain."""
        print(f"[Node {self.node_id}] Menerima pesan '{msg_type}' dari node {sender_id}")
        
        if msg_type == "ELECTION":
            if self.node_id > sender_id:
                sender_port = self.peers.get(sender_id)
                if sender_port:
                    self.send_message(sender_port, "OK")
                threading.Thread(target=self.start_election, daemon=True).start()
                
        elif msg_type == "OK":
            self.ok_received.set()
            
        elif msg_type == "COORDINATOR":
            with self.lock:
                self.leader_id = sender_id
            print(f"[Node {self.node_id}] Leader terkonfirmasi: Node {sender_id}")
            
        elif msg_type == "PING":
            pass

    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        self.ok_received.clear()
        higher_peers = {pid: port for pid, port in self.peers.items() if pid > self.node_id}
        
        print(f"[Node {self.node_id}] Memulai election ke peer lebih tinggi: {higher_peers}")
        
        if not higher_peers:
            self.declare_leader()
            return

        sent_any = False
        for pid, port in higher_peers.items():
            if self.send_message(port, "ELECTION"):
                sent_any = True

        if not sent_any:
            self.declare_leader()
            return

        received_ok = self.ok_received.wait(timeout=ELECTION_TIMEOUT)
        if not received_ok:
            self.declare_leader()

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        with self.lock:
            self.leader_id = self.node_id
        print(f"[Node {self.node_id}] Broadcast COORDINATOR, saya jadi leader!")
        for pid, port in self.peers.items():
            self.send_message(port, "COORDINATOR")

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            with self.lock:
                current_leader = self.leader_id
                
            if current_leader and current_leader != self.node_id:
                leader_port = self.peers.get(current_leader)
                if leader_port:
                    alive = self.send_message(leader_port, "PING")
                    if not alive:
                        print(f"[Node {self.node_id}] Leader (Node {current_leader}) mati! Memicu election baru...")
                        with self.lock:
                            if self.leader_id == current_leader:
                                self.leader_id = None
                        self.start_election()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True,
                         help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005")
    args = parser.parse_args()

    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    time.sleep(1)  
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()