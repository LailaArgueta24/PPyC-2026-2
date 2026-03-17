import time
import threading

boletos_disponibles = 100
lock = threading.Lock()

def vender_boletos(cantidad):
    global boletos_disponibles
    with lock:
        temp = boletos_disponibles
        time.sleep(0.0001)
        boletos_disponibles = temp-cantidad
        print(f"Boletos disponibles: {boletos_disponibles}")

if __name__ == "__main__" :
    threads = []
    for _ in range(100):
        threads.append(
            threading.Thread(target=vender_boletos, args=(1,))
        )
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"FINAL:{boletos_disponibles}")
        
            