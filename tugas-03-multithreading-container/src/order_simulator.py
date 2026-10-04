"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading
"""

import threading
import random
import time

NUM_ORDERS = 100        
NUM_WORKERS = 10        

processed_count = 0

# TODO 1: Objek Lock untuk melindungi `processed_count`.
lock = threading.Lock()


def process_order(order_id: int) -> None:
    global processed_count
    time.sleep(random.uniform(0.001, 0.01))
    with lock:
        processed_count += 1




def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 
    threads = []
    chunk_size = len(order_ids) // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < NUM_WORKERS - 1 else len(order_ids)
        chunk = order_ids[start_idx:end_idx]

        t = threading.Thread(target=worker, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!")


if __name__ == "__main__":
    main()