import socket
import time

def attendre_kafka(host="localhost", port=9092, timeout=30):
    start_time = time.time()
    print(f"🕵️  En attente de Kafka sur {host}:{port}...")
    
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"✅ Kafka est en ligne ! (Temps: {time.time() - start_time:.1f}s)")
                return True
        except (socket.timeout, ConnectionRefusedError):
            pass
        
        if time.time() - start_time > timeout:
            print("❌ Timeout : Kafka ne répond pas.")
            return False
            
        time.sleep(1)

if __name__ == "__main__":
    attendre_kafka()