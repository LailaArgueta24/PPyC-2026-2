import time
import random
import requests
import threading
from bs4 import BeautifulSoup
import queue
from sqlalchemy import create_engine, text

user="postgres"
password="supersecret"
host ="localhost"
port="5432"
database="postgres"

cola_symbols = queue.Queue()

cola_precios = queue.Queue()

def get_connection(user, password, host, port, database):
    return create_engine(
        url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )

def insert_price(symbol, price):
    try:
        with get_connection(user, password, host, port, database).begin() as connector:
            connector.execute(text(f"INSERT INTO inversiones(symbol,price) VALUES ('{symbol}', {price})"))
    except Exception as e:
        print("ERROR AL INSERTAR:", e)
#Scrapping
def obtener_precio_stock():

    while True:
        try:
            symbol = cola_symbols.get_nowait()
        except queue.Empty:
            break

        URL = f"https://finance.yahoo.com/quote/{symbol}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        while True:
            time.sleep(3 * random.random())

            response = requests.get(URL, headers=headers)

            if response.status_code == 200:

                soup = BeautifulSoup(response.text, "html.parser")

                valor = soup.find("span", {"data-testid": "qsp-price"})

                if valor:
                    precio = float(valor.text.replace(",", ""))
                    print(f"[SCRAPING] {symbol} -> {precio}")
                    # se guarda en cola para insertar luego
                    cola_precios.put((symbol, precio))

                break

        cola_symbols.task_done()

#Inserciones
def insertar_precios():
    while True:
        try:
            symbol, precio = cola_precios.get(timeout=5)
        except queue.Empty:
            print("[Base] Cola vacía, terminando thread")
            break

        print(f"[Base] Insertando {symbol} -> {precio}")
        insert_price(symbol, precio)

        cola_precios.task_done()

if __name__ == "__main__":

    with open("./symbols.txt", "r") as f:
        lista_symbolos = [line.strip() for line in f if line.strip()]

    # cargar cola de scraping
    for symbol in lista_symbolos:
        cola_symbols.put(symbol)

    threads_scraping = []
    threads_db = []
#Thr3ad scrapping
    for _ in range(8):
        t = threading.Thread(target=obtener_precio_stock)
        t.start()
        threads_scraping.append(t)

    for t in threads_scraping:
        t.join()

#Thread inserción
    for _ in range(4):
        t = threading.Thread(target=insertar_precios)
        t.start()
        threads_db.append(t)

    for t in threads_db:
        t.join()

    print("Proceso terminado")