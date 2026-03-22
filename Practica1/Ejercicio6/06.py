import requests
import threading
import time

#Ejemplo de archivos pequeños
archivos = [
    "https://www.gutenberg.org/cache/epub/11/pg11.txt",
    "https://www.gutenberg.org/cache/epub/84/pg84.txt",
    "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
]
def descargar_archivo(url, nombre_salida):
    respuesta = requests.get(url, stream=True, timeout=20)

    with open(nombre_salida, 'wb') as archivo:
        for chunk in respuesta.iter_content(chunk_size=1024):
            if chunk:
                archivo.write(chunk)
    print(f"Descargado: {nombre_salida}")

if __name__ == "__main__":
    #Secuencial
    inicio = time.time()
    for i, url in enumerate(archivos):
        descargar_archivo(url, f"archivo_{i}.txt")

    tiempo_secuencial = time.time() - inicio
    print(f"\nTiempo secuencial: {tiempo_secuencial}")

    #Concurrente
    hilos = []
    inicio2 = time.time()

    for i, url in enumerate(archivos):
        h = threading.Thread(
            target=descargar_archivo,
            args=(url, f"archivo_thread_{i}.txt")
        )
        hilos.append(h)
        h.start()

    for hilo in hilos:
        hilo.join()

    tiempo_concurrente = time.time() - inicio2
    print(f"\nTiempo concurrente: {tiempo_concurrente:.2f} segundos")