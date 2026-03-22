import urllib.request
from collections import Counter
import re
import threading

libros = [
    ("https://www.gutenberg.org/cache/epub/1342/pg1342.txt", "Orgullo y Prejuicio"),
    ("https://www.gutenberg.org/cache/epub/84/pg84.txt", "Frankenstein"),
    ("https://www.gutenberg.org/cache/epub/11/pg11.txt", "Alicia en el pais de las maravillas")
]

resultados = []

lock = threading.Lock()

def contar_palabras(url):
    respuesta = urllib.request.urlopen(url)
    texto = respuesta.read().decode('utf-8').lower()
    palabras = re.findall(r'\b\w+\b', texto)
    return Counter(palabras)

def worker(url, nombre):
    print(f"Procesando: {nombre}")
    
    contador = contar_palabras(url)
    
    # Sección crítica (lista compartida)
    with lock:
        resultados.append(contador)

# MAP (Ejecución paralela)
hilos = []

for url, nombre in libros:
    hilo = threading.Thread(target=worker, args=(url, nombre))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

# REDUCE (Combinación)
resultado_final = Counter()

for contador in resultados:
    resultado_final.update(contador)

# Mostrar top 20 palabras
print("\nTop 20 palabras más frecuentes:\n")
for palabra, frecuencia in resultado_final.most_common(20):
    print(f"{palabra}: {frecuencia}")